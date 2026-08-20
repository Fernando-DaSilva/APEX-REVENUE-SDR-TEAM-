"""
Z-API WhatsApp Service Module
Handles outgoing text messages, audio notes, interactive buttons, and instance status checks.
"""
import os
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger("app.services.zapi")

class ZAPIService:
    def __init__(
        self,
        instance_id: Optional[str] = None,
        client_token: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.instance_id = instance_id or os.getenv("ZAPI_INSTANCE_ID", "3F7CDA470843917372BC9E4132DEE0C8")
        self.client_token = client_token or os.getenv("ZAPI_CLIENT_TOKEN", "C571A30E8ECCEB315903627F")
        
        default_base = f"https://api.z-api.io/instances/{self.instance_id}/token/{self.client_token}"
        self.base_url = (base_url or os.getenv("ZAPI_BASE_URL", default_base)).rstrip('/')
        
        self.headers = {
            "Client-Token": self.client_token,
            "Content-Type": "application/json"
        }

    def _clean_phone(self, phone: str) -> str:
        """Sanitize phone number to international E.164 format (e.g. 5511999999999, 37063900500)"""
        phone_str = str(phone).strip()
        is_explicit_intl = phone_str.startswith("+")
        digits = "".join([c for c in phone_str if c.isdigit()])
        
        if is_explicit_intl:
            return digits
        
        if (len(digits) == 10 or len(digits) == 11) and not (digits.startswith("55") or digits.startswith("370")):
            digits = "55" + digits
        return digits

    async def check_status(self) -> Dict[str, Any]:
        """Check connection status of the Z-API WhatsApp instance"""
        url = f"{self.base_url}/status"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Failed to fetch Z-API instance status: {e}")
                return {"connected": False, "error": str(e)}

    async def send_text(self, phone: str, message: str) -> Dict[str, Any]:
        """Send text message to a WhatsApp number"""
        clean_phone = self._clean_phone(phone)
        url = f"{self.base_url}/send-text"
        payload = {
            "phone": clean_phone,
            "message": message
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                msg_id = data.get('zaapId') or data.get('messageId') or f"OUT_{int(time.time())}"
                logger.info(f"Message sent to {clean_phone}: Z-API ID {msg_id}")
                
                try:
                    from app.services.message_store import append_message_to_store
                    import time
                    outbound_entry = {
                        "id": f"out_{int(time.time() * 1000)}",
                        "timestamp": time.strftime("%H:%M:%S"),
                        "date": time.strftime("%Y-%m-%d"),
                        "instanceId": self.instance_id,
                        "messageId": msg_id,
                        "phone": clean_phone,
                        "senderName": "APEX SDR OS (Outbound)",
                        "message": message,
                        "fromMe": True,
                        "status": "outbound_sent",
                        "latency_ms": 0.0,
                        "raw_payload": payload
                    }
                    append_message_to_store(outbound_entry)
                except Exception as err:
                    logger.warning(f"Could not persist outbound message to store: {err}")

                return {"success": True, "data": data}
            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP error sending text to {clean_phone}: {exc.response.text}")
                return {"success": False, "error": exc.response.text, "status_code": exc.response.status_code}
            except Exception as e:
                logger.error(f"Error sending text message to {clean_phone}: {e}")
                return {"success": False, "error": str(e)}

    async def send_audio(self, phone: str, audio_url: str) -> Dict[str, Any]:
        """Send voice note / audio file to a WhatsApp number"""
        clean_phone = self._clean_phone(phone)
        url = f"{self.base_url}/send-audio"
        payload = {
            "phone": clean_phone,
            "audio": audio_url
        }
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
            except Exception as e:
                logger.error(f"Failed to send audio to {clean_phone}: {e}")
                return {"success": False, "error": str(e)}

    async def send_button_list(self, phone: str, title: str, button_label: str, choices: list) -> Dict[str, Any]:
        """Send interactive option list/buttons to a WhatsApp number"""
        clean_phone = self._clean_phone(phone)
        url = f"{self.base_url}/send-button-list"
        payload = {
            "phone": clean_phone,
            "message": title,
            "buttonText": button_label,
            "options": [{"id": str(i), "title": choice} for i, choice in enumerate(choices, 1)]
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
            except Exception as e:
                logger.error(f"Failed to send button list to {clean_phone}: {e}")
                return {"success": False, "error": str(e)}
