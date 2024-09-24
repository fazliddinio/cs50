#!/usr/bin/env python3
"""URL Shortener"""
import hashlib
import json
from pathlib import Path

DB_FILE = Path.home() / ".url_shortener.json"

def shorten(url):
    code = hashlib.md5(url.encode()).hexdigest()[:6]
    print(f"Short: https://short.url/{code}")
    return code

# persistence
