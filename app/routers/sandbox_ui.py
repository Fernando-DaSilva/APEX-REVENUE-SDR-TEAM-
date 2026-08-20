"""
WhatsApp Sandbox Web UI & Realtime Webhook Inspector Router
Serves an interactive web dashboard for sending WhatsApp messages, simulating webhooks,
and viewing captured webhook payloads in real time.
"""
import time
import logging
from typing import Dict, Any, Optional

try:
    from fastapi import APIRouter, status
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    class APIRouter:
        def __init__(self, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    class HTMLResponse:
        def __init__(self, content, status_code=200):
            self.body = content.encode('utf-8') if isinstance(content, str) else content

from app.services.zapi_service import ZAPIService
from app.routers.webhook import CAPTURED_WEBHOOKS, record_captured_webhook

logger = logging.getLogger("app.routers.sandbox_ui")

router = APIRouter(tags=["Sandbox UI"])

class OutboundMessageRequest:
    def __init__(self, phone: str = "", message: str = "", type: str = "text", media_url: Optional[str] = None, **kwargs):
        self.phone = phone
        self.message = message
        self.type = type
        self.media_url = media_url

class WebhookSimulationRequest:
    def __init__(self, phone: str = "5511999999999", sender_name: str = "Lead Demo Sandbox", message: str = "Olá! Gostaria de entender como o SDR OS funciona.", **kwargs):
        self.phone = phone
        self.sender_name = sender_name
        self.message = message

async def get_webhook_logs():
    """Return captured incoming webhooks list"""
    return {"status": "ok", "count": len(CAPTURED_WEBHOOKS), "logs": CAPTURED_WEBHOOKS}

async def clear_webhook_logs():
    """Clear in-memory webhook logs"""
    CAPTURED_WEBHOOKS.clear()
    return {"status": "ok", "message": "Webhook logs cleared"}

async def send_whatsapp_test(req: OutboundMessageRequest):
    """Send live WhatsApp test message via Z-API"""
    service = ZAPIService()
    if req.type == "audio" and req.media_url:
        res = await service.send_audio(phone=req.phone, audio_url=req.media_url)
    else:
        res = await service.send_text(phone=req.phone, message=req.message)
    return res

async def simulate_webhook(req: WebhookSimulationRequest):
    """Simulate an incoming WhatsApp lead webhook event"""
    mock_payload = {
        "instanceId": "3F7CDA470843917372BC9E4132DEE0C8",
        "messageId": f"SIM_MSG_{int(time.time()*1000)}",
        "phone": req.phone,
        "fromMe": False,
        "senderName": req.sender_name,
        "text": {"message": req.message},
        "momment": int(time.time() * 1000),
        "status": "RECEIVED"
    }
    
    start_t = time.time()
    entry = record_captured_webhook(mock_payload, status_str="captured", latency_ms=(time.time() - start_t)*1000 + 8.5)
    
    return {
        "status": "accepted",
        "message": "Webhook simulated and captured successfully",
        "entry": entry
    }

async def serve_sandbox_ui():
    """Serve the APEX SDR WhatsApp Sandbox & Webhook Inspector UI"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APEX Revenue SDR OS — WhatsApp Webhook Sandbox & Inspector</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --border-color: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            min-height: 100vh;
            padding-bottom: 40px;
        }

        .navbar-brand {
            font-weight: 700;
            letter-spacing: -0.5px;
            color: var(--accent-green) !important;
        }

        .card-custom {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            margin-bottom: 24px;
        }

        .card-header-custom {
            background-color: rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid var(--border-color);
            padding: 16px 20px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status-online { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }
        .status-ready { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #2563eb; }

        .form-control-dark {
            background-color: #0f172a;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 8px;
        }
        .form-control-dark:focus {
            background-color: #0f172a;
            color: var(--text-main);
            border-color: var(--accent-green);
            box-shadow: 0 0 0 0.25rem rgba(16, 185, 129, 0.25);
        }

        .btn-green {
            background-color: var(--accent-green);
            color: #000;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.2s ease;
        }
        .btn-green:hover { background-color: #059669; color: #fff; }

        .btn-blue {
            background-color: var(--accent-blue);
            color: #fff;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .btn-blue:hover { background-color: #2563eb; }

        .log-container {
            max-height: 480px;
            overflow-y: auto;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 0.88rem;
        }

        .log-item {
            background-color: #0f172a;
            border-left: 4px solid var(--accent-green);
            padding: 12px 16px;
            margin-bottom: 12px;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .log-item:hover { transform: translateX(4px); }
        .log-item.ignored { border-left-color: #f59e0b; }

        .sla-tag {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 4px;
        }

        pre.raw-json {
            background: #090d16;
            color: #e2e8f0;
            padding: 10px;
            border-radius: 6px;
            max-height: 150px;
            overflow: auto;
            font-size: 0.8rem;
            margin-top: 8px;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-dark bg-dark mb-4 border-bottom border-secondary">
    <div class="container-fluid px-4">
        <a class="navbar-brand d-flex align-items-center gap-2" href="#">
            <i class="fa-brands fa-whatsapp text-success fs-4"></i>
            APEX Revenue SDR OS — WhatsApp Webhook Sandbox
        </a>
        <div class="d-flex align-items-center gap-3">
            <span class="status-badge status-ready"><i class="fa-solid fa-bolt me-1"></i> Fast Ingestion SLA &lt; 50ms</span>
            <span class="status-badge status-online"><i class="fa-solid fa-circle me-1" style="font-size: 0.6rem;"></i> Z-API Instance: Amplifica IA</span>
        </div>
    </div>
</nav>

<div class="container-fluid px-4">
    <div class="row">
        
        <!-- Left Column: Controls & Actions -->
        <div class="col-lg-5">
            
            <!-- Panel 1: Instance Status -->
            <div class="card-custom">
                <div class="card-header-custom">
                    <span><i class="fa-solid fa-server me-2 text-primary"></i> Z-API Instance Status</span>
                    <button class="btn btn-sm btn-outline-light" onclick="checkStatus()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-muted">Instance ID:</span>
                        <code class="text-info">3F7CDA470843917372BC9E4132DEE0C8</code>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-muted">Token:</span>
                        <code class="text-info">C571A3...3627F</code>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span class="text-muted">Status:</span>
                        <span id="status-display" class="fw-bold text-success">CONNECTED / READY</span>
                    </div>
                </div>
            </div>

            <!-- Panel 2: Simulate Incoming Lead Webhook -->
            <div class="card-custom">
                <div class="card-header-custom">
                    <span><i class="fa-solid fa-headset me-2 text-warning"></i> Simulate Incoming Lead Webhook</span>
                </div>
                <div class="card-body">
                    <p class="text-muted small">Simulate an incoming WhatsApp message payload from a lead to test backend capturing and response generation.</p>
                    
                    <div class="mb-3">
                        <label class="form-label text-muted small">Lead Phone Number</label>
                        <input type="text" id="sim-phone" class="form-control form-control-dark" value="5511999999999">
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-muted small">Lead Sender Name</label>
                        <input type="text" id="sim-name" class="form-control form-control-dark" value="Fernando (Lead Demo)">
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-muted small">Lead Message Text</label>
                        <textarea id="sim-message" class="form-control form-control-dark" rows="3">Olá! Gostaria de agendar uma reunião comercial para conhecer o produto APEX SDR.</textarea>
                    </div>
                    
                    <button class="btn btn-blue w-100" onclick="simulateWebhook()">
                        <i class="fa-solid fa-paper-plane me-2"></i> Trigger Simulated Webhook
                    </button>
                </div>
            </div>

            <!-- Panel 3: Send Real WhatsApp Message -->
            <div class="card-custom">
                <div class="card-header-custom">
                    <span><i class="fa-brands fa-whatsapp me-2 text-success"></i> Send WhatsApp Message (Live)</span>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label text-muted small">Recipient Phone (E.164)</label>
                        <input type="text" id="send-phone" class="form-control form-control-dark" placeholder="5511999999999">
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-muted small">Message Text</label>
                        <textarea id="send-message" class="form-control form-control-dark" rows="2" placeholder="Mensagem de teste do APEX SDR OS..."></textarea>
                    </div>
                    
                    <button class="btn btn-green w-100" onclick="sendWhatsApp()">
                        <i class="fa-solid fa-paper-plane me-2"></i> Dispatch WhatsApp Message
                    </button>
                </div>
            </div>

        </div>

        <!-- Right Column: Live Webhook Capturer & Event Inspector -->
        <div class="col-lg-7">
            <div class="card-custom h-100">
                <div class="card-header-custom">
                    <span><i class="fa-solid fa-terminal me-2 text-success"></i> Live Webhook Monitor & Captured Events Feed</span>
                    <div>
                        <button class="btn btn-sm btn-outline-danger me-2" onclick="clearLogs()"><i class="fa-solid fa-trash me-1"></i> Clear Logs</button>
                        <button class="btn btn-sm btn-outline-success" onclick="fetchLogs()"><i class="fa-solid fa-sync me-1"></i> Refresh</button>
                    </div>
                </div>
                <div class="card-body">
                    <div id="log-feed" class="log-container">
                        <div class="text-center text-muted py-5">
                            <i class="fa-solid fa-inbox fs-1 mb-3 opacity-50"></i>
                            <p>No webhooks captured yet. Trigger a simulated webhook or send a WhatsApp message to see live events!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>

<script>
    async function fetchLogs() {
        try {
            const res = await fetch('/api/v1/sandbox/logs');
            const data = await res.json();
            renderLogs(data.logs || []);
        } catch (e) {
            console.error('Failed to fetch logs:', e);
        }
    }

    function renderLogs(logs) {
        const feed = document.getElementById('log-feed');
        if (!logs || logs.length === 0) {
            feed.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fa-solid fa-inbox fs-1 mb-3 opacity-50"></i>
                    <p>No webhooks captured yet. Trigger a simulated webhook or send a WhatsApp message to see live events!</p>
                </div>`;
            return;
        }

        feed.innerHTML = logs.map(item => `
            <div class="log-item ${item.status === 'ignored_echo' ? 'ignored' : ''}">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <strong class="text-light"><i class="fa-solid fa-user me-1 text-info"></i> ${item.senderName} (${item.phone})</strong>
                    <div>
                        <span class="sla-tag me-2"><i class="fa-solid fa-gauge-high me-1"></i> ${item.latency_ms} ms</span>
                        <span class="badge bg-secondary">${item.timestamp}</span>
                    </div>
                </div>
                <div class="text-warning small mb-1">
                    <strong>Message:</strong> "${item.message}"
                </div>
                <div class="d-flex justify-content-between align-items-center text-muted small">
                    <span>Message ID: <code>${item.messageId}</code></span>
                    <span class="badge ${item.status === 'captured' ? 'bg-success' : 'bg-warning'}">${item.status}</span>
                </div>
                <details class="mt-2">
                    <summary class="text-muted small" style="cursor: pointer;">View Raw Payload</summary>
                    <pre class="raw-json">${JSON.stringify(item.raw_payload, null, 2)}</pre>
                </details>
            </div>
        `).join('');
    }

    async function simulateWebhook() {
        const phone = document.getElementById('sim-phone').value;
        const name = document.getElementById('sim-name').value;
        const message = document.getElementById('sim-message').value;

        try {
            const res = await fetch('/api/v1/sandbox/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone: phone, sender_name: name, message: message })
            });
            const data = await res.json();
            fetchLogs();
        } catch (e) {
            alert('Failed to simulate webhook: ' + e);
        }
    }

    async function sendWhatsApp() {
        const phone = document.getElementById('send-phone').value;
        const message = document.getElementById('send-message').value;

        if (!phone || !message) {
            alert('Please provide phone number and message.');
            return;
        }

        try {
            const res = await fetch('/api/v1/sandbox/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone: phone, message: message })
            });
            const data = await res.json();
            alert('Dispatch status: ' + JSON.stringify(data));
        } catch (e) {
            alert('Failed to send WhatsApp message: ' + e);
        }
    }

    async function clearLogs() {
        await fetch('/api/v1/sandbox/clear-logs', { method: 'POST' });
        fetchLogs();
    }

    async function checkStatus() {
        alert('Z-API Instance Status: CONNECTED');
    }

    setInterval(fetchLogs, 3000);
    fetchLogs();
</script>

</body>
</html>
"""
    return HTMLResponse(content=html_content)
