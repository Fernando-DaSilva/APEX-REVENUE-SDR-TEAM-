#!/usr/bin/env python3
"""
Monitor script for capturing WhatsApp responses from:
- Renato (+5515981270383)
- Leandro (+5515991627233)
"""

import sys
import os
import asyncio
import time
import json
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.zapi_service import ZAPIService
from app.services.message_store import get_all_stored_messages

TARGET_PHONES = {
    "37063900500": "Fernando",
    "5515981270383": "Renato",
    "5515991627233": "Leandro"
}

async def monitor():
    zapi = ZAPIService()
    print("==========================================================================")
    print(" MONITORING WHATSAPP RESPONSES FOR FERNANDO, RENATO & LEANDRO")
    print("==========================================================================")
    print(f"Target Numbers: {list(TARGET_PHONES.keys())}")
    print("Checking Z-API Instance Connection & Message Queue...\n")

    status = await zapi.check_status()
    print(f"Z-API Status: {json.dumps(status, ensure_ascii=False)}")

    # Check Queue
    url = f"{zapi.base_url}/queue"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url, headers=zapi.headers)
            if r.status_code == 200:
                queue_items = r.json()
                print(f"Outbound Queue Count: {len(queue_items)}")
                for item in queue_items:
                    phone = item.get("Phone")
                    name = TARGET_PHONES.get(phone, "Unknown")
                    print(f" - Queued for {name} ({phone}): ZaapID={item.get('ZaapId')}")
        except Exception as e:
            print(f"Error checking queue: {e}")

    print("\nReading persisted & live captured messages from disk storage...")
    stored_messages = get_all_stored_messages()
    found = False
    for hook in stored_messages:
        phone = str(hook.get("phone", "")).replace("+", "").strip()
        if phone in TARGET_PHONES:
            name = TARGET_PHONES[phone]
            direction = "OUTBOUND" if hook.get("fromMe") else "INBOUND RESPONSE"
            print(f"✔ [{direction}] {name} ({phone}) at {hook.get('timestamp')}: \"{hook.get('message')}\" (Status: {hook.get('status')})")
            found = True

    if not found:
        print("No inbound responses or messages stored for target numbers yet.")

if __name__ == "__main__":
    asyncio.run(monitor())
