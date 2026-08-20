# TASK BACKLOG & DELIVERABLES — Nimbus (Cloud & VPS Infrastructure Engineer)

| Task ID | Task Description | Target Sprint | Status | Deliverable Artifact |
|---|---|---|---|---|
| T11.1 | Onboard Nimbus (Cloud Infra Agent) via Helena (`10_HR_AI_Specialist`) | Sprint 01 | [COMPLETED] | `11_Cloud_Infrastructure_Engineer/MANIFEST.md` |
| T11.2 | Provision Hostinger VPS (`1767287`) & Nginx / SSL Let's Encrypt stack | Sprint 01 | [ACTIVE] | `scripts/deploy_vps.sh` & Nginx config |
| T11.3 | Bind Z-API Instance (`3F7CDA470843917372BC9E4132DEE0C8`) Webhooks to Hostinger VPS Endpoint | Sprint 01 | [ACTIVE] | Webhook URL Configuration & Signature Verification |
| T11.4 | Setup systemd unit service for FastAPI app server & Taskiq async worker | Sprint 01 | [PLANNED] | `/etc/systemd/system/apex-sdr.service` |
| T11.5 | Configure UFW Firewall & Fail2ban on Hostinger VPS | Sprint 01 | [PLANNED] | Security Audit Report |
