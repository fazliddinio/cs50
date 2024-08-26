#!/usr/bin/env python3
"""Expense Tracker"""
import json
from pathlib import Path
from datetime import date

EXPENSES_FILE = Path.home() / ".expense_tracker.json"

def load_expenses():
    if not EXPENSES_FILE.exists(): return []
    with open(EXPENSES_FILE) as f: return json.load(f)

def add_expense(amount, category):
    expenses = load_expenses()
    expenses.append({"amount": amount, "category": category, "date": date.today().isoformat()})
    print(f"Added: ${amount:.2f} for {category}")

# list summary
