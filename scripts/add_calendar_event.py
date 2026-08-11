#!/usr/bin/env python3
"""
add_calendar_event.py - Reusable Calendar Event Creation & Email Invite Tool for Selena (Team Secretary).

Supports:
1. Native macOS Calendar app event creation via AppleScript.
2. Generating .ics iCalendar file and emailing calendar invites to fernando8cfo@gmail.com.

Usage:
    python3 scripts/add_calendar_event.py \
        --title "APEX SDR Milestone Review" \
        --start "2026-08-12 15:00" \
        --duration 40 \
        --description "Review sprint deliverables and team alignment." \
        --location "Google Meet" \
        --send-invite
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path to import send_email if needed
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

try:
    from send_email import send_email, load_env_file
except ImportError:
    send_email = None

def parse_datetime(dt_str):
    """Parse various datetime string formats into a datetime object."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unable to parse datetime string '{dt_str}'. Use format 'YYYY-MM-DD HH:MM'.")

def create_macos_calendar_event(title, start_dt, end_dt, description="", location="", calendar_name="Calendar"):
    """Create an event in the native macOS Calendar application using AppleScript."""
    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    # Escape quotes for AppleScript
    title_clean = title.replace('"', '\\"')
    desc_clean = (description or "").replace('"', '\\"')
    loc_clean = (location or "").replace('"', '\\"')
    cal_clean = (calendar_name or "Calendar").replace('"', '\\"')

    applescript = f'''
    tell application "Calendar"
        set targetCal to missing value
        try
            set targetCal to first calendar whose name is "{cal_clean}"
        on error
            set targetCal to first calendar
        end try
        tell targetCal
            make new event with properties {{summary:"{title_clean}", start date:date "{start_str}", end date:date "{end_str}", description:"{desc_clean}", location:"{loc_clean}"}}
        end tell
        reload calendars
    end tell
    '''

    try:
        res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
        print(f"Successfully created event '{title}' in macOS Calendar app!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"macOS Calendar notice: {e.stderr.strip() or e}", file=sys.stderr)
        return False

def generate_ics_file(title, start_dt, end_dt, description="", location="", output_path="/tmp/event.ics"):
    """Generate an iCalendar (.ics) file."""
    start_ics = start_dt.strftime("%Y%m%dT%H%M%SZ")
    end_ics = end_dt.strftime("%Y%m%dT%H%M%SZ")
    now_ics = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Antigravity AI Assistant//Selena Secretary//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:event-{now_ics}@antigravity.ai
DTSTAMP:{now_ics}
DTSTART:{start_ics}
DTEND:{end_ics}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""

    path = Path(output_path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ics_content.strip())
    
    return str(path)

def send_calendar_invite_email(title, start_dt, end_dt, description="", location="", recipient=None):
    """Send an .ics calendar invite attachment via send_email.py."""
    if not send_email:
        print("Warning: send_email module unavailable. Cannot send email invite.", file=sys.stderr)
        return False

    load_env_file("~/.env")
    load_env_file(".env")
    target_recipient = recipient or os.getenv("RECIPIENT_EMAIL", "fernando8cfo@gmail.com")

    ics_path = generate_ics_file(title, start_dt, end_dt, description, location)

    start_formatted = start_dt.strftime("%A, %B %d, %Y at %I:%M %p")
    end_formatted = end_dt.strftime("%I:%M %p")

    body_html = f"""\
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #4f46e5;">📅 Calendar Invitation: {title}</h2>
        <p>Selena has scheduled an event for you.</p>
        <div style="background: #f8fafc; padding: 15px; border-left: 4px solid #4f46e5; margin: 15px 0;">
          <p><strong>Event:</strong> {title}</p>
          <p><strong>When:</strong> {start_formatted} - {end_formatted}</p>
          <p><strong>Location:</strong> {location or 'N/A'}</p>
          <p><strong>Details:</strong> {description or 'N/A'}</p>
        </div>
        <p><i>An <code>.ics</code> calendar invite is attached. Open the attachment to add it to your calendar automatically.</i></p>
      </body>
    </html>
    """

    subject = f"📅 Calendar Invite: {title} ({start_formatted})"
    send_email(
        subject=subject,
        body=body_html,
        to_email=target_recipient,
        attachments=[ics_path],
        is_html=True
    )
    print(f"Successfully emailed calendar invite for '{title}' to {target_recipient}!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Add calendar events locally or send .ics invitations.")
    parser.add_argument("-t", "--title", required=True, help="Event title/summary")
    parser.add_argument("-s", "--start", required=True, help="Start date & time (e.g. '2026-08-12 15:00')")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Duration in minutes (default: 30)")
    parser.add_argument("-e", "--end", help="Explicit end date & time (overrides duration)")
    parser.add_argument("-desc", "--description", default="", help="Event description")
    parser.add_argument("-l", "--location", default="", help="Event location or meeting link")
    parser.add_argument("-c", "--calendar", default="Calendar", help="Name of macOS Calendar")
    parser.add_argument("--send-invite", "--email", action="store_true", help="Send an .ics email invite to Fernando")
    parser.add_argument("--no-mac-calendar", action="store_true", help="Skip creating event in local macOS Calendar app")

    args = parser.parse_args()

    try:
        start_dt = parse_datetime(args.start)
        if args.end:
            end_dt = parse_datetime(args.end)
        else:
            end_dt = start_dt + timedelta(minutes=args.duration)
    except ValueError as err:
        print(f"Error parsing dates: {err}", file=sys.stderr)
        sys.exit(1)

    success_mac = False
    if not args.no_mac_calendar:
        success_mac = create_macos_calendar_event(
            title=args.title,
            start_dt=start_dt,
            end_dt=end_dt,
            description=args.description,
            location=args.location,
            calendar_name=args.calendar
        )

    if args.send_invite:
        send_calendar_invite_email(
            title=args.title,
            start_dt=start_dt,
            end_dt=end_dt,
            description=args.description,
            location=args.location
        )
    elif not success_mac:
        print("Tip: Use --send-invite to dispatch an .ics email invitation to your inbox.")

if __name__ == "__main__":
    main()
