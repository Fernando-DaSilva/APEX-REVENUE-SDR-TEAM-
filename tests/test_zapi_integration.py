"""
Unit & Integration Tests for Z-API WhatsApp Webhook, Service & Sandbox UI
Pure Python unittest runner (zero external test dependencies).
"""
import unittest
import asyncio
from typing import Dict, Any

from app.services.zapi_service import ZAPIService
from app.routers.webhook import process_whatsapp_message_async, CAPTURED_WEBHOOKS, record_captured_webhook
from app.routers.sandbox_ui import serve_sandbox_ui, simulate_webhook, get_webhook_logs, clear_webhook_logs, WebhookSimulationRequest

class TestZAPIIntegration(unittest.TestCase):

    def setUp(self):
        self.service = ZAPIService(
            instance_id="3F7CDA470843917372BC9E4132DEE0C8",
            client_token="C571A30E8ECCEB315903627F"
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(clear_webhook_logs())

    def test_phone_sanitization_e164(self):
        """Verify phone number is sanitized to international format"""
        self.assertEqual(self.service._clean_phone("(11) 99999-9999"), "5511999999999")
        self.assertEqual(self.service._clean_phone("11988887777"), "5511988887777")
        self.assertEqual(self.service._clean_phone("5511999999999"), "5511999999999")

    def test_zapi_headers_and_base_url(self):
        """Verify headers and API endpoints match Z-API specs"""
        self.assertEqual(self.service.client_token, "C571A30E8ECCEB315903627F")
        self.assertIn("3F7CDA470843917372BC9E4132DEE0C8", self.service.base_url)
        self.assertEqual(self.service.headers["Client-Token"], "C571A30E8ECCEB315903627F")

    def test_async_message_processing_worker(self):
        """Verify async message consumer completes execution without error"""
        mock_payload = {
            "instanceId": "3F7CDA470843917372BC9E4132DEE0C8",
            "messageId": "TEST_MSG_1001",
            "phone": "5511999999999",
            "fromMe": False,
            "text": {"message": "Quero conhecer a plataforma APEX SDR"},
            "senderName": "Test Lead"
        }
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_whatsapp_message_async(mock_payload))

    def test_sandbox_ui_serving_and_live_webhook_capturing(self):
        """Verify Webhook UI dashboard serves HTML and captures simulated lead webhooks"""
        loop = asyncio.get_event_loop()
        
        # 1. Test HTML Dashboard Serving
        html_response = loop.run_until_complete(serve_sandbox_ui())
        self.assertIn(b"APEX Revenue SDR OS", html_response.body)
        self.assertIn(b"Live Webhook Monitor", html_response.body)
        self.assertIn(b"3F7CDA470843917372BC9E4132DEE0C8", html_response.body)
        
        # 2. Test Webhook Simulation & Live Capture
        sim_req = WebhookSimulationRequest(
            phone="5511988887777",
            sender_name="Fernando UI Test Lead",
            message="Test capturing text back in Sandbox UI"
        )
        sim_result = loop.run_until_complete(simulate_webhook(sim_req))
        self.assertEqual(sim_result["status"], "accepted")
        self.assertEqual(sim_result["entry"]["message"], "Test capturing text back in Sandbox UI")
        
        # 3. Test Logs Query
        logs_result = loop.run_until_complete(get_webhook_logs())
        self.assertEqual(logs_result["count"], 1)
        self.assertEqual(logs_result["logs"][0]["senderName"], "Fernando UI Test Lead")

if __name__ == "__main__":
    unittest.main()
