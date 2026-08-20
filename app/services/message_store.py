"""
Persistent Message Store Utility for WhatsApp Inbound & Outbound Messages
Saves all inbound webhooks, outbound messages, and test sandbox logs to disk.
File Location: data/whatsapp_messages_log.json
"""
import os
import json
import time
from typing import Dict, Any, List

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
LOG_FILE_PATH = os.path.join(DATA_DIR, "whatsapp_messages_log.json")

def ensure_data_dir():
    """Ensure data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def append_message_to_store(entry: Dict[str, Any]):
    """Append message entry to persistent disk storage (JSON file)"""
    ensure_data_dir()
    messages = get_all_stored_messages()
    
    # Deduplicate by id if present
    entry_id = entry.get("id") or entry.get("messageId")
    if entry_id:
        messages = [m for m in messages if (m.get("id") != entry_id and m.get("messageId") != entry_id)]
    
    messages.insert(0, entry)
    
    # Limit max 500 records on disk
    if len(messages) > 500:
        messages = messages[:500]
        
    try:
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error persisting message to file {LOG_FILE_PATH}: {e}")

def get_all_stored_messages() -> List[Dict[str, Any]]:
    """Retrieve all messages stored on disk"""
    ensure_data_dir()
    if not os.path.exists(LOG_FILE_PATH):
        return []
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading message store file {LOG_FILE_PATH}: {e}")
        return []

def clear_message_store():
    """Clear message store file"""
    ensure_data_dir()
    try:
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
    except Exception:
        pass
