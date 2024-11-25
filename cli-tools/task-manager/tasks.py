#!/usr/bin/env python3
"""Task Manager"""
import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path.home() / ".task_manager.json"

def load_data():
    if not TASKS_FILE.exists(): return {"projects": {}, "tasks": []}
    with open(TASKS_FILE) as f: return json.load(f)

# project task
