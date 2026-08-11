#!/usr/bin/env python3
"""
send_email.py - Reusable email notification tool for AI Assistant & Automated Workflows.

Usage:
    python3 send_email.py --subject "Task Finished" --body "Your build passed!" --to "user@example.com"
    python3 send_email.py --subject "Daily Report" --body "<h1>Report</h1>" --attach "./report.pdf" --html
"""

import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

def load_env_file(filepath="~/.env"):
    """Load key-value pairs from a .env file into os.environ if not already present."""
    env_path = Path(os.path.expanduser(filepath))
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    os.environ.setdefault(key, val)

def send_email(subject, body, to_email=None, attachments=None, is_html=True):
    # Load .env variables
    load_env_file("~/.env")
    load_env_file(".env")

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    default_recipient = os.getenv("RECIPIENT_EMAIL", "fernando8cfo@gmail.com")

    target_email = to_email or default_recipient

    if not smtp_user or not smtp_pass:
        raise ValueError("Missing SMTP_USER or SMTP_PASS. Please configure them in ~/.env")
    if not target_email:
        raise ValueError("Missing recipient email address.")

    # Create message container
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"Antigravity Assistant <{smtp_user}>"
    msg["To"] = target_email

    # Attach text/html body
    content_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body, content_type, "utf-8"))

    # Attach files if provided
    if attachments:
        for filepath in attachments:
            path = Path(filepath)
            if not path.exists():
                print(f"Warning: Attachment '{filepath}' not found. Skipping.", file=sys.stderr)
                continue
            with open(path, "rb") as f:
                part = MIMEApplication(f.read(), Name=path.name)
                part.add_header("Content-Disposition", "attachment", filename=path.name)
                msg.attach(part)

    # Send email
    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20)
    else:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=20)
        server.starttls()

    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, [target_email], msg.as_string())
    server.quit()

    print(f"Successfully sent email to {target_email} with subject: '{subject}'")

def main():
    parser = argparse.ArgumentParser(description="Send emails using SMTP configuration.")
    parser.add_argument("-s", "--subject", required=True, help="Email subject line")
    parser.add_argument("-b", "--body", help="Email body text or HTML (reads stdin if omitted)")
    parser.add_argument("-t", "--to", help="Recipient email address (defaults to RECIPIENT_EMAIL in env)")
    parser.add_argument("-a", "--attach", action="append", help="File paths to attach (can be used multiple times)")
    parser.add_argument("--text-only", action="store_true", help="Send body as plain text instead of HTML")

    args = parser.parse_args()

    body_content = args.body
    if not body_content:
        if not sys.stdin.isatty():
            body_content = sys.stdin.read()
        else:
            print("Error: Body text must be provided via --body or piped stdin.", file=sys.stderr)
            sys.exit(1)

    try:
        send_email(
            subject=args.subject,
            body=body_content,
            to_email=args.to,
            attachments=args.attach,
            is_html=not args.text_only
        )
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
