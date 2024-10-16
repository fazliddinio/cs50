#!/usr/bin/env python3
"""Habit Tracker"""
import json
from pathlib import Path
from datetime import date, timedelta

HABITS_FILE = Path.home() / ".habit_tracker.json"

def load_data():
    if not HABITS_FILE.exists(): return {"habits": {}, "log": {}}
    with open(HABITS_FILE) as f: return json.load(f)

# streaks
