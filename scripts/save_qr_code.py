import asyncio
import base64
import json
import httpx

INSTANCE_ID = "3F7CDA470843917372BC9E4132DEE0C8"
CLIENT_TOKEN = "C571A30E8ECCEB315903627F"
BASE_URL = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{CLIENT_TOKEN}"
HEADERS = {"Client-Token": CLIENT_TOKEN, "Content-Type": "application/json"}

async def save_qr():
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/qr-code/image", headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            val = data.get("value", "")
            if val.startswith("data:image/png;base64,"):
                b64_str = val.replace("data:image/png;base64,", "")
                img_data = base64.b64decode(b64_str)
                artifact_path = "/Users/fernandodasilva/.gemini/antigravity/brain/121a52db-0b99-40fe-a095-79c5aa10c7f1/zapi_qr_code.png"
                with open(artifact_path, "wb") as f:
                    f.write(img_data)
                print(f"QR code image saved successfully to {artifact_path}")
            else:
                print("No base64 image data found")
        else:
            print(f"HTTP {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    asyncio.run(save_qr())
