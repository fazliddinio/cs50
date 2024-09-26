#!/usr/bin/env python3
"""
URL Shortener - Simple URL shortening service
"""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional


DB_FILE = Path.home() / ".url_shortener.json"


def load_db() -> dict:
    """Load URL database."""
    if not DB_FILE.exists():
        return {"urls": {}, "stats": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db: dict) -> None:
    """Save URL database."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


def generate_short_code(url: str, length: int = 6) -> str:
    """Generate short code for URL."""
    hash_obj = hashlib.md5(url.encode())
    return hash_obj.hexdigest()[:length]


def shorten_url(url: str, custom_code: Optional[str] = None) -> str:
    """Create shortened URL."""
    db = load_db()
    
    # Check if URL already exists
    for code, data in db["urls"].items():
        if data["url"] == url:
            return code
    
    # Generate or use custom code
    code = custom_code if custom_code else generate_short_code(url)
    
    # Handle collision
    while code in db["urls"] and not custom_code:
        code = generate_short_code(url + str(datetime.now()))
    
    db["urls"][code] = {
        "url": url,
        "created_at": datetime.now().isoformat(),
        "clicks": 0,
    }
    db["stats"][code] = []
    
    save_db(db)
    return code


def expand_url(code: str) -> Optional[str]:
    """Get original URL from short code."""
    db = load_db()
    
    if code in db["urls"]:
        # Track click
        db["urls"][code]["clicks"] += 1
        db["stats"][code].append(datetime.now().isoformat())
        save_db(db)
        return db["urls"][code]["url"]
    
    return None


def list_urls() -> None:
    """List all shortened URLs."""
    db = load_db()
    
    if not db["urls"]:
        print("📭 No URLs yet!")
        return
    
    print("\n🔗 Shortened URLs:")
    print("-" * 70)
    print(f"{'Code':<10} {'Clicks':>8} {'URL'}")
    print("-" * 70)
    
    for code, data in db["urls"].items():
        url_display = data["url"][:45] + "..." if len(data["url"]) > 45 else data["url"]
        print(f"{code:<10} {data['clicks']:>8} {url_display}")
    
    print("-" * 70)


def get_stats(code: str) -> None:
    """Get statistics for a short URL."""
    db = load_db()
    
    if code not in db["urls"]:
        print(f"❌ Code '{code}' not found")
        return
    
    data = db["urls"][code]
    clicks = db["stats"].get(code, [])
    
    print(f"\n📊 Stats for: {code}")
    print("-" * 40)
    print(f"URL: {data['url']}")
    print(f"Created: {data['created_at']}")
    print(f"Total clicks: {data['clicks']}")
    
    if clicks:
        print(f"\nRecent clicks:")
        for click in clicks[-5:]:
            print(f"  - {click}")


def delete_url(code: str) -> None:
    """Delete a shortened URL."""
    db = load_db()
    
    if code in db["urls"]:
        del db["urls"][code]
        if code in db["stats"]:
            del db["stats"][code]
        save_db(db)
        print(f"🗑️  Deleted: {code}")
    else:
        print(f"❌ Code '{code}' not found")


def main():
    parser = argparse.ArgumentParser(description="URL Shortener")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Shorten command
    shorten = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten.add_argument("url", help="URL to shorten")
    shorten.add_argument("-c", "--custom", help="Custom short code")
    
    # Expand command
    expand = subparsers.add_parser("expand", help="Expand a short URL")
    expand.add_argument("code", help="Short code")
    
    # List command
    subparsers.add_parser("list", help="List all URLs")
    
    # Stats command
    stats = subparsers.add_parser("stats", help="Get URL statistics")
    stats.add_argument("code", help="Short code")
    
    # Delete command
    delete = subparsers.add_parser("delete", help="Delete a URL")
    delete.add_argument("code", help="Short code")
    
    args = parser.parse_args()
    
    if args.command == "shorten":
        code = shorten_url(args.url, args.custom)
        print(f"🔗 Short URL: https://short.url/{code}")
    
    elif args.command == "expand":
        url = expand_url(args.code)
        if url:
            print(f"🔗 Original URL: {url}")
        else:
            print(f"❌ Code '{args.code}' not found")
    
    elif args.command == "list":
        list_urls()
    
    elif args.command == "stats":
        get_stats(args.code)
    
    elif args.command == "delete":
        delete_url(args.code)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# long url test
