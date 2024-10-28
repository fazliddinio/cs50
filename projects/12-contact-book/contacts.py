#!/usr/bin/env python3
"""Contact Book"""
import json
from pathlib import Path

CONTACTS_FILE = Path.home() / ".contacts_book.json"

def load_contacts():
    if not CONTACTS_FILE.exists(): return []
    with open(CONTACTS_FILE) as f: return json.load(f)

def add_contact(name, phone="", email=""):
    contacts = load_contacts()
    contacts.append({"name": name, "phone": phone, "email": email})
    print(f"Added: {name}")

# search view
