#!/usr/bin/env python3
"""
Todo CLI - A simple command-line todo application
"""
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional


TODO_FILE = Path.home() / ".todo_cli.json"


def load_todos() -> List[dict]:
    """Load todos from file."""
    if not TODO_FILE.exists():
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def save_todos(todos: List[dict]) -> None:
    """Save todos to file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def add_todo(title: str, priority: str = "medium") -> None:
    """Add a new todo item."""
    todos = load_todos()
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"✅ Added: {title}")


def list_todos(show_all: bool = False) -> None:
    """List all todos."""
    todos = load_todos()
    if not todos:
        print("📭 No todos yet!")
        return
    
    priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    
    print("\n📋 Your Todos:")
    print("-" * 50)
    for todo in todos:
        if not show_all and todo["completed"]:
            continue
        status = "✅" if todo["completed"] else "⬜"
        priority = priority_colors.get(todo["priority"], "⚪")
        print(f"{status} [{todo['id']}] {priority} {todo['title']}")
    print("-" * 50)


def complete_todo(todo_id: int) -> None:
    """Mark a todo as completed."""
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            save_todos(todos)
            print(f"✅ Completed: {todo['title']}")
            return
    print(f"❌ Todo #{todo_id} not found")


def delete_todo(todo_id: int) -> None:
    """Delete a todo."""
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"🗑️  Deleted: {removed['title']}")
            return
    print(f"❌ Todo #{todo_id} not found")


def clear_completed() -> None:
    """Clear all completed todos."""
    todos = load_todos()
    remaining = [t for t in todos if not t["completed"]]
    cleared = len(todos) - len(remaining)
    save_todos(remaining)
    print(f"🧹 Cleared {cleared} completed todos")


def main():
    parser = argparse.ArgumentParser(description="Todo CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", help="Todo title")
    add_parser.add_argument("-p", "--priority", 
                           choices=["high", "medium", "low"],
                           default="medium", help="Priority level")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List todos")
    list_parser.add_argument("-a", "--all", action="store_true",
                            help="Show completed todos too")
    
    # Complete command
    complete_parser = subparsers.add_parser("done", help="Mark todo as done")
    complete_parser.add_argument("id", type=int, help="Todo ID")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="Todo ID")
    
    # Clear command
    subparsers.add_parser("clear", help="Clear completed todos")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_todo(args.title, args.priority)
    elif args.command == "list":
        list_todos(args.all)
    elif args.command == "done":
        complete_todo(args.id)
    elif args.command == "delete":
        delete_todo(args.id)
    elif args.command == "clear":
        clear_completed()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# edge cases

# reviewed

# better errors

# id fix
