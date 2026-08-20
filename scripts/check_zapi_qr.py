import asyncio
import json
import httpx

INSTANCE_ID = "3F7CDA470843917372BC9E4132DEE0C8"
CLIENT_TOKEN = "C571A30E8ECCEB315903627F"
BASE_URL = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{CLIENT_TOKEN}"

HEADERS = {
    "Client-Token": CLIENT_TOKEN,
    "Content-Type": "application/json"
}

endpoints_to_test = [
    "qr-code",
    "qr-code/image",
    "phone-code",
    "restart",
    "disconnect",
    "queue"
]

async def test_all():
    async with httpx.AsyncClient(timeout=10.0) as client:
        for ep in endpoints_to_test:
            url = f"{BASE_URL}/{ep}"
            try:
                r = await client.get(url, headers=HEADERS)
                print(f"GET {ep:30s} -> Status: {r.status_code}")
                if r.status_code in (200, 201):
                    print(f"   Response: {r.text[:300]}")
            except Exception as e:
                print(f"GET {ep:30s} -> Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_all())
