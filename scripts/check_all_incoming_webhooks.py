import sys
import os
import asyncio
import json
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.zapi_service import ZAPIService
from app.routers.webhook import CAPTURED_WEBHOOKS

async def check():
    zapi = ZAPIService()
    status = await zapi.check_status()
    print("=== Z-API INSTANCE STATUS ===")
    print(json.dumps(status, indent=2, ensure_ascii=False))

    print("\n=== CAPTURED WEBHOOKS IN MEMORY ===")
    print(f"Total captured: {len(CAPTURED_WEBHOOKS)}")
    for hook in CAPTURED_WEBHOOKS:
        print(f"[{hook.get('timestamp')}] From: {hook.get('phone')} ({hook.get('senderName')}) -> '{hook.get('message')}' (Status: {hook.get('status')})")

    # Check Z-API QR Code URL if disconnected
    if not status.get("connected"):
        url = f"{zapi.base_url}/qr-code"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                r = await client.get(url, headers=zapi.headers)
                if r.status_code == 200:
                    print("\n=== CURRENT Z-API QR CODE LINK ===")
                    print(r.json().get("value"))
            except Exception as e:
                print(f"Error fetching QR: {e}")

if __name__ == "__main__":
    asyncio.run(check())
