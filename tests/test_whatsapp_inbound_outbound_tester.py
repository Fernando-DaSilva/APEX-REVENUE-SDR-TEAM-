"""
WhatsApp Inbound & Outbound Tester Agent Suite
Executed by Quinn (QA Director) & Automated Tester Agent
Validates full end-to-end Z-API WhatsApp message flows:
- Inbound Webhook Ingestion (<50ms SLA, async worker, echo filter)
- Outbound Message Dispatch (send_text, send_audio, send_button_list, E.164 phone sanitization)
- Live Webhook Sandbox UI simulation & log capture
"""
import unittest
import asyncio
import time
from unittest.mock import MagicMock, patch

from app.services.zapi_service import ZAPIService
from app.routers.webhook import (
    receive_zapi_webhook,
    process_whatsapp_message_async,
    CAPTURED_WEBHOOKS,
    record_captured_webhook,
    BackgroundTasks
)
from app.routers.sandbox_ui import (
    serve_sandbox_ui,
    simulate_webhook,
    get_webhook_logs,
    clear_webhook_logs,
    WebhookSimulationRequest
)

class TestWhatsAppInboundOutboundTesterAgent(unittest.TestCase):

    def setUp(self):
        self.service = ZAPIService(
            instance_id="3F7CDA470843917372BC9E4132DEE0C8",
            client_token="C571A30E8ECCEB315903627F"
        )
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(clear_webhook_logs())

    # -------------------------------------------------------------------------
    # INBOUND TESTS (Webhook ingestion, SLA, Echo filtering, Payload extraction)
    # -------------------------------------------------------------------------
    def test_inbound_webhook_ingestion_sla_and_processing(self):
        """Tester Agent: Verify inbound WhatsApp lead webhook ingests under 50ms SLA"""
        mock_payload = {
            "instanceId": "3F7CDA470843917372BC9E4132DEE0C8",
            "messageId": "INBOUND_TEST_9901",
            "phone": "5511988889999",
            "fromMe": False,
            "text": {"message": "Olá! Gostaria de agendar uma demonstração do SDR OS."},
            "senderName": "Carlos Silva - Lead Target"
        }
        
        bg_tasks = BackgroundTasks()
        start_time = time.time()
        res = self.loop.run_until_complete(
            receive_zapi_webhook(payload=mock_payload, background_tasks=bg_tasks)
        )
        elapsed_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(res["status"], "accepted")
        self.assertEqual(res["message_id"], "INBOUND_TEST_9901")
        self.assertLess(elapsed_ms, 50.0, f"Inbound webhook SLA breached: {elapsed_ms:.2f}ms >= 50ms")

    def test_inbound_echo_filtering(self):
        """Tester Agent: Verify outbound message echoes (fromMe=True) are ignored to prevent loops"""
        mock_echo_payload = {
            "instanceId": "3F7CDA470843917372BC9E4132DEE0C8",
            "messageId": "ECHO_TEST_001",
            "phone": "5511988889999",
            "fromMe": True,
            "text": {"message": "Resposta automática do SDR Agent."},
            "senderName": "APEX SDR Agent"
        }
        
        bg_tasks = BackgroundTasks()
        res = self.loop.run_until_complete(
            receive_zapi_webhook(payload=mock_echo_payload, background_tasks=bg_tasks)
        )
        self.assertEqual(res["status"], "ignored")
        self.assertEqual(res["reason"], "outbound_echo")

    def test_inbound_async_worker_execution(self):
        """Tester Agent: Verify async worker processes inbound message cleanly"""
        mock_payload = {
            "phone": "5511977776666",
            "text": {"message": "Qual é o valor do plano Enterprise?"}
        }
        with patch("app.routers.webhook.logger") as mock_logger:
            self.loop.run_until_complete(process_whatsapp_message_async(mock_payload))
            mock_logger.info.assert_any_call("[ASYNC AGENT WORKER] Processing message from 5511977776666: 'Qual é o valor do plano Enterprise?'")

    # -------------------------------------------------------------------------
    # OUTBOUND TESTS (Phone sanitization, Text, Audio, Interactive Buttons)
    # -------------------------------------------------------------------------
    def test_outbound_phone_sanitization(self):
        """Tester Agent: Verify phone numbers are correctly converted to international E.164 format"""
        test_cases = [
            ("(11) 98888-7777", "5511988887777"),
            ("11988887777", "5511988887777"),
            ("+55 11 98888-7777", "5511988887777"),
            ("5511988887777", "5511988887777"),
            ("+37063900500", "37063900500"),
            ("37063900500", "37063900500")
        ]
        for raw_input, expected in test_cases:
            self.assertEqual(self.service._clean_phone(raw_input), expected)

    def test_anti_bulk_spam_dynamic_content_variation(self):
        """Tester Agent: Verify ADR-038 anti-bulk spam engine produces 100% unique messages for different recipients"""
        from app.services.anti_spam import generate_dynamic_variation
        
        base_msg = "Esta é uma mensagem de teste do sistema APEX Revenue SDR OS para validação."
        msg_renato = generate_dynamic_variation(base_msg, lead_name="Renato")
        msg_leandro = generate_dynamic_variation(base_msg, lead_name="Leandro")
        msg_fernando = generate_dynamic_variation(base_msg, lead_name="Fernando")

        # 1. Assert messages are personalized with lead name
        self.assertIn("Renato", msg_renato)
        self.assertIn("Leandro", msg_leandro)
        self.assertIn("Fernando", msg_fernando)

        # 2. Assert messages are strictly distinct across all recipients
        self.assertNotEqual(msg_renato, msg_leandro)
        self.assertNotEqual(msg_renato, msg_fernando)
        self.assertNotEqual(msg_leandro, msg_fernando)

    @patch("httpx.AsyncClient.post")
    def test_outbound_send_text_dispatch(self, mock_post):
        """Tester Agent: Verify ZAPIService.send_text builds valid Z-API request payload"""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={"zaapId": "ZAAP_MSG_5501", "status": "PENDING"})
        
        # AsyncClient.post is async, so its return value when awaited is mock_response
        async def _mock_post(*args, **kwargs):
            return mock_response
        mock_post.side_effect = _mock_post

        res = self.loop.run_until_complete(
            self.service.send_text(phone="(11) 91111-2222", message="Olá Carlos, agendado para amanhã às 14h.")
        )
        
        self.assertTrue(res["success"])
        self.assertEqual(res["data"]["zaapId"], "ZAAP_MSG_5501")
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["json"]["phone"], "5511911112222")
        self.assertEqual(call_kwargs["json"]["message"], "Olá Carlos, agendado para amanhã às 14h.")
        self.assertEqual(call_kwargs["headers"]["Client-Token"], "C571A30E8ECCEB315903627F")

    @patch("httpx.AsyncClient.post")
    def test_outbound_send_audio_dispatch(self, mock_post):
        """Tester Agent: Verify ZAPIService.send_audio builds valid audio payload"""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={"zaapId": "AUDIO_MSG_102", "status": "PENDING"})
        
        async def _mock_post(*args, **kwargs):
            return mock_response
        mock_post.side_effect = _mock_post

        res = self.loop.run_until_complete(
            self.service.send_audio(phone="5511988887777", audio_url="https://sdr-media.apex.io/audio_note.ogg")
        )
        
        self.assertTrue(res["success"])
        self.assertEqual(res["data"]["zaapId"], "AUDIO_MSG_102")

    @patch("httpx.AsyncClient.post")
    def test_outbound_send_button_list_dispatch(self, mock_post):
        """Tester Agent: Verify ZAPIService.send_button_list builds interactive button list payload"""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={"zaapId": "BTN_MSG_301", "status": "PENDING"})
        
        async def _mock_post(*args, **kwargs):
            return mock_response
        mock_post.side_effect = _mock_post

        choices = ["Amanhã 10:00", "Amanhã 15:00", "Sexta 11:00"]
        res = self.loop.run_until_complete(
            self.service.send_button_list(
                phone="5511988887777",
                title="Escolha o melhor horário:",
                button_label="Ver Horários",
                choices=choices
            )
        )

        self.assertTrue(res["success"])
        call_kwargs = mock_post.call_args.kwargs
        options = call_kwargs["json"]["options"]
        self.assertEqual(len(options), 3)
        self.assertEqual(options[0]["title"], "Amanhã 10:00")

    # -------------------------------------------------------------------------
    # INTEGRATION / SANDBOX UI SIMULATION TEST
    # -------------------------------------------------------------------------
    def test_sandbox_ui_end_to_end_lead_simulation(self):
        """Tester Agent: Simulate full inbound lead message via Sandbox UI and verify captured log registry"""
        sim_req = WebhookSimulationRequest(
            phone="5511933334444",
            sender_name="Dra. Renata Mello",
            message="Quero solicitar uma proposta comercial para minha clínica."
        )
        sim_res = self.loop.run_until_complete(simulate_webhook(sim_req))
        
        self.assertEqual(sim_res["status"], "accepted")
        self.assertEqual(sim_res["entry"]["senderName"], "Dra. Renata Mello")
        
        logs = self.loop.run_until_complete(get_webhook_logs())
        self.assertGreaterEqual(logs["count"], 1)
        latest = logs["logs"][0]
        self.assertEqual(latest["phone"], "5511933334444")
        self.assertEqual(latest["message"], "Quero solicitar uma proposta comercial para minha clínica.")

if __name__ == "__main__":
    unittest.main()
