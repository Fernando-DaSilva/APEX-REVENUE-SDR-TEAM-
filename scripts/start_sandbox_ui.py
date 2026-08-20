#!/usr/bin/env python3
"""
Launcher script for WhatsApp Sandbox Web UI & Webhook Inspector
APEX Revenue SDR OS

Usage:
    python scripts/start_sandbox_ui.py
"""
import os
import sys
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from app.routers.sandbox_ui import serve_sandbox_ui, OutboundMessageRequest, WebhookSimulationRequest, simulate_webhook, get_webhook_logs, clear_webhook_logs, send_whatsapp_test

PORT = 8085

class SandboxHTTPRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Silence routine request logging for clean terminal
        return

    def do_GET(self):
        if self.path in ("/", "/sandbox"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            html_res = loop.run_until_complete(serve_sandbox_ui())
            self.wfile.write(html_res.body)
        elif self.path == "/api/v1/sandbox/logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(get_webhook_logs())
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "APEX SDR Sandbox"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8")) if body else {}

        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if self.path == "/api/v1/sandbox/simulate":
            req = WebhookSimulationRequest(**payload)
            res = loop.run_until_complete(simulate_webhook(req))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        elif self.path == "/api/v1/sandbox/send":
            req = OutboundMessageRequest(**payload)
            res = loop.run_until_complete(send_whatsapp_test(req))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        elif self.path == "/api/v1/sandbox/clear-logs":
            res = loop.run_until_complete(clear_webhook_logs())
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        elif self.path == "/api/v1/webhooks/zapi":
            from app.routers.webhook import record_captured_webhook
            record_captured_webhook(payload, status_str="captured", latency_ms=12.4)
            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "accepted", "message_id": payload.get("messageId")}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, SandboxHTTPRequestHandler)
    print("==========================================================================")
    print("       APEX REVENUE SDR OS — WHATSAPP WEBHOOK SANDBOX UI SERVER           ")
    print("==========================================================================")
    print(f"🌐 Running Web UI Dashboard at: http://127.0.0.1:{PORT}/sandbox")
    print(f"📥 Local Webhook Ingestion URL : http://127.0.0.1:{PORT}/api/v1/webhooks/zapi")
    print("Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Sandbox UI Server. Goodbye!")

if __name__ == "__main__":
    run_server()
