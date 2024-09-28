#!/usr/bin/env python3
"""Markdown to HTML"""
import re

def convert_headers(text):
    for i in range(6, 0, -1):
        pattern = r"^#{" + str(i) + r"}\s+(.+)$"
        text = re.sub(pattern, f"<h{i}>\\1</h{i}>", text, flags=re.MULTILINE)
    return text

# formatting
