import os
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

PHONES = {
    "5515981270383": "Renato",
    "5515991627233": "Leandro"
}

async def fetch_messages(phone: str, name: str):
    print(f"\n--- Checking messages for {name} ({phone}) ---")
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Try various Z-API message endpoints
        endpoints = [
            f"{BASE_URL}/chat-messages/{phone}",
            f"{BASE_URL}/messages/{phone}",
            f"{BASE_URL}/chats"
        ]
        for url in endpoints:
            try:
                resp = await client.get(url, headers=HEADERS)
                print(f"GET {url.split('/')[-2]}/{url.split('/')[-1]} -> Status: {resp.status_code}")
                if resp.status_code == 200:
                    data = resp.json()
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                    return data
            except Exception as e:
                print(f"Error querying {url}: {e}")

async def main():
    for phone, name in PHONES.items():
        await fetch_messages(phone, name)

if __name__ == "__main__":
    asyncio.run(main())
