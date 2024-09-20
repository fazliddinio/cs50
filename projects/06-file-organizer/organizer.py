#!/usr/bin/env python3
"""File Organizer"""
from pathlib import Path
import shutil

FILE_TYPES = {
    "Images": [".jpg",".png",".gif"],
    "Documents": [".pdf",".doc",".txt"],
    "Code": [".py",".js",".c"],
}

def get_category(ext):
    for cat, exts in FILE_TYPES.items():
        if ext.lower() in exts: return cat
    return "Other"

# more file types
