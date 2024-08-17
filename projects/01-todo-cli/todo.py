#!/usr/bin/env python3
"""Todo CLI"""
import json
from pathlib import Path

TODO_FILE = Path.home() / ".todo_cli.json"

def load_todos():
    if not TODO_FILE.exists(): return []
    with open(TODO_FILE) as f: return json.load(f)

def save_todos(todos):
    with open(TODO_FILE, "w") as f: json.dump(todos, f, indent=2)

def add_todo(title):
    todos = load_todos()
    todos.append({"id": len(todos)+1, "title": title, "completed": False})
    save_todos(todos)
    print(f"Added: {title}")
