#!/usr/bin/env python3
"""
Contact Book CLI - Manage your contacts
"""
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


CONTACTS_FILE = Path.home() / ".contacts_book.json"


def load_contacts() -> List[Dict]:
    """Load contacts from file."""
    if not CONTACTS_FILE.exists():
        return []
    with open(CONTACTS_FILE, "r") as f:
        return json.load(f)


def save_contacts(contacts: List[Dict]) -> None:
    """Save contacts to file."""
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


def add_contact(name: str, phone: str = "", email: str = "", 
                notes: str = "") -> None:
    """Add a new contact."""
    contacts = load_contacts()
    
    # Check for duplicate
    for c in contacts:
        if c["name"].lower() == name.lower():
            print(f"Contact '{name}' already exists. Use 'update' to modify.")
            return
    
    contact = {
        "id": len(contacts) + 1,
        "name": name,
        "phone": phone,
        "email": email,
        "notes": notes,
        "created_at": datetime.now().isoformat(),
    }
    
    contacts.append(contact)
    save_contacts(contacts)
    print(f"Added contact: {name}")


def list_contacts(search: Optional[str] = None) -> None:
    """List all contacts or search."""
    contacts = load_contacts()
    
    if search:
        query = search.lower()
        contacts = [
            c for c in contacts
            if query in c["name"].lower() 
            or query in c.get("phone", "")
            or query in c.get("email", "").lower()
        ]
    
    if not contacts:
        print("No contacts found.")
        return
    
    print(f"\nContacts ({len(contacts)}):")
    print("-" * 60)
    print(f"{'ID':<5} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 60)
    
    for c in sorted(contacts, key=lambda x: x["name"]):
        print(f"{c['id']:<5} {c['name']:<20} {c.get('phone', ''):<15} {c.get('email', '')}")
    
    print("-" * 60)


def show_contact(name: str) -> None:
    """Show detailed contact information."""
    contacts = load_contacts()
    
    for c in contacts:
        if c["name"].lower() == name.lower():
            print(f"\nContact Details:")
            print("=" * 40)
            print(f"  Name:    {c['name']}")
            print(f"  Phone:   {c.get('phone', 'N/A')}")
            print(f"  Email:   {c.get('email', 'N/A')}")
            print(f"  Notes:   {c.get('notes', 'N/A')}")
            print(f"  Added:   {c['created_at'][:10]}")
            print("=" * 40)
            return
    
    print(f"Contact '{name}' not found.")


def update_contact(name: str, phone: str = None, email: str = None,
                   notes: str = None) -> None:
    """Update an existing contact."""
    contacts = load_contacts()
    
    for c in contacts:
        if c["name"].lower() == name.lower():
            if phone is not None:
                c["phone"] = phone
            if email is not None:
                c["email"] = email
            if notes is not None:
                c["notes"] = notes
            
            save_contacts(contacts)
            print(f"Updated contact: {c['name']}")
            return
    
    print(f"Contact '{name}' not found.")


def delete_contact(name: str) -> None:
    """Delete a contact."""
    contacts = load_contacts()
    
    for i, c in enumerate(contacts):
        if c["name"].lower() == name.lower():
            removed = contacts.pop(i)
            save_contacts(contacts)
            print(f"Deleted contact: {removed['name']}")
            return
    
    print(f"Contact '{name}' not found.")


def export_contacts(filename: str) -> None:
    """Export contacts to a file."""
    import csv
    contacts = load_contacts()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "phone", "email", "notes"]
        )
        writer.writeheader()
        for c in contacts:
            writer.writerow({
                "name": c["name"],
                "phone": c.get("phone", ""),
                "email": c.get("email", ""),
                "notes": c.get("notes", ""),
            })
    
    print(f"Exported {len(contacts)} contacts to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Contact Book CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add contact
    add_cmd = subparsers.add_parser("add", help="Add a contact")
    add_cmd.add_argument("name", help="Contact name")
    add_cmd.add_argument("-p", "--phone", default="", help="Phone number")
    add_cmd.add_argument("-e", "--email", default="", help="Email address")
    add_cmd.add_argument("-n", "--notes", default="", help="Notes")
    
    # List contacts
    list_cmd = subparsers.add_parser("list", help="List contacts")
    list_cmd.add_argument("-s", "--search", help="Search query")
    
    # Show contact
    show_cmd = subparsers.add_parser("show", help="Show contact details")
    show_cmd.add_argument("name", help="Contact name")
    
    # Update contact
    update_cmd = subparsers.add_parser("update", help="Update a contact")
    update_cmd.add_argument("name", help="Contact name")
    update_cmd.add_argument("-p", "--phone", help="New phone")
    update_cmd.add_argument("-e", "--email", help="New email")
    update_cmd.add_argument("-n", "--notes", help="New notes")
    
    # Delete contact
    del_cmd = subparsers.add_parser("delete", help="Delete a contact")
    del_cmd.add_argument("name", help="Contact name")
    
    # Export
    export_cmd = subparsers.add_parser("export", help="Export contacts")
    export_cmd.add_argument("filename", help="Output CSV file")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_contact(args.name, args.phone, args.email, args.notes)
    elif args.command == "list":
        list_contacts(args.search)
    elif args.command == "show":
        show_contact(args.name)
    elif args.command == "update":
        update_contact(args.name, args.phone, args.email, args.notes)
    elif args.command == "delete":
        delete_contact(args.name)
    elif args.command == "export":
        export_contacts(args.filename)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# csv export
