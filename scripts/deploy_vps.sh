#!/usr/bin/env bash
# ==============================================================================
# Hostinger VPS Automated Deployment & Webhook Setup Script
# Managed by Nimbus (11_Cloud_Infrastructure_Engineer) & Sentinel (05_Security_DevSecOps_Engineer)
# Project: APEX Revenue SDR OS (Amplifica IA WhatsApp Integration)
# ==============================================================================

set -euo pipefail

echo "🚀 Starting APEX SDR OS Deployment on Hostinger VPS..."

# 1. Update OS Packages & Dependencies
echo "📦 [1/6] Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx ufw fail2ban git curl

# 2. Setup Application Directory
APP_DIR="/opt/apex-revenue-sdr"
echo "📁 [2/6] Configuring application directory at $APP_DIR..."
sudo mkdir -p "$APP_DIR"
sudo chown -R $USER:$USER "$APP_DIR"

# 3. Create Python Virtual Environment & Install Dependencies
echo "🐍 [3/6] Setting up Python virtual environment..."
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
fi
"$APP_DIR/venv/bin/pip" install --upgrade pip
if [ -f "$APP_DIR/requirements.txt" ]; then
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
else
    "$APP_DIR/venv/bin/pip" install fastapi uvicorn httpx pydantic taskiq structlog python-dotenv
fi

# 4. Configure systemd Service for FastAPI Server
echo "⚙ [4/6] Setting up systemd service (apex-sdr.service)..."
cat << 'EOF' | sudo tee /etc/systemd/system/apex-sdr.service
[Unit]
Description=APEX Revenue SDR OS FastAPI Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/apex-revenue-sdr
EnvironmentFile=/opt/apex-revenue-sdr/.env
ExecStart=/opt/apex-revenue-sdr/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable apex-sdr.service
sudo systemctl restart apex-sdr.service

# 5. Configure Nginx Reverse Proxy
echo "🌐 [5/6] Configuring Nginx reverse proxy..."
cat << 'EOF' | sudo tee /etc/nginx/sites-available/apex-sdr
server {
    listen 80;
    server_name sdr.amplifica.ai;  # Replace with actual VPS domain / sub-domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/v1/webhooks/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_read_timeout 10s;
        proxy_connect_timeout 5s;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/apex-sdr /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 6. Configure UFW Firewall
echo "🛡 [6/6] Securing Hostinger VPS with UFW Firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable

echo "=========================================================================="
echo "✔ Hostinger VPS Deployment Complete!"
echo "📍 FastAPI Service Running at: http://127.0.0.1:8000"
echo "📍 Z-API Webhook Endpoint: https://sdr.amplifica.ai/api/v1/webhooks/zapi"
echo "🔒 Run 'sudo certbot --nginx' to enable SSL/TLS certificate"
echo "=========================================================================="
