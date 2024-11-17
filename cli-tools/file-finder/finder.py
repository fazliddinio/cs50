#!/usr/bin/env python3
"""File Finder"""
from pathlib import Path

def find_files(directory, pattern="*", recursive=True):
    glob_pat = f"**/{pattern}" if recursive else pattern
    for f in Path(directory).glob(glob_pat):
        if f.is_file(): yield f

# size date filters
