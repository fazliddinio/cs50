#!/usr/bin/env python3
"""
Task Manager CLI - Manage projects and tasks
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional
from enum import Enum


TASKS_FILE = Path.home() / ".task_manager.json"


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


def load_data() -> Dict:
    """Load tasks data."""
    if not TASKS_FILE.exists():
        return {"projects": {}, "tasks": []}
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_data(data: Dict) -> None:
    """Save tasks data."""
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_project(name: str, description: str = "") -> None:
    """Add a new project."""
    data = load_data()
    
    project_id = name.lower().replace(" ", "_")
    
    if project_id in data["projects"]:
        print(f"❌ Project '{name}' already exists")
        return
    
    data["projects"][project_id] = {
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat(),
    }
    
    save_data(data)
    print(f"✅ Created project: {name}")


def add_task(
    title: str,
    project: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> None:
    """Add a new task."""
    data = load_data()
    
    task_id = len(data["tasks"]) + 1
    
    task = {
        "id": task_id,
        "title": title,
        "project": project.lower().replace(" ", "_") if project else None,
        "priority": priority,
        "status": "todo",
        "due_date": due_date,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
    }
    
    data["tasks"].append(task)
    save_data(data)
    print(f"✅ Added task #{task_id}: {title}")


def list_tasks(
    project: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    show_all: bool = False,
) -> None:
    """List tasks with filters."""
    data = load_data()
    
    tasks = data["tasks"]
    
    # Apply filters
    if project:
        project_id = project.lower().replace(" ", "_")
        tasks = [t for t in tasks if t["project"] == project_id]
    
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    elif not show_all:
        tasks = [t for t in tasks if t["status"] != "done"]
    
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    
    if not tasks:
        print("📭 No tasks found!")
        return
    
    # Group by project
    by_project = {}
    for task in tasks:
        proj = task["project"] or "No Project"
        if proj not in by_project:
            by_project[proj] = []
        by_project[proj].append(task)
    
    priority_icons = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
    status_icons = {"todo": "⬜", "in_progress": "🔄", "done": "✅"}
    
    print("\n📋 Tasks")
    print("=" * 60)
    
    for proj_name, proj_tasks in by_project.items():
        print(f"\n📁 {proj_name}")
        print("-" * 50)
        
        for task in sorted(proj_tasks, key=lambda x: (
            {"urgent": 0, "high": 1, "medium": 2, "low": 3}[x["priority"]],
            x["due_date"] or "9999"
        )):
            p_icon = priority_icons.get(task["priority"], "⚪")
            s_icon = status_icons.get(task["status"], "⬜")
            due = f" 📅{task['due_date']}" if task["due_date"] else ""
            
            print(f"  {s_icon} [{task['id']:03d}] {p_icon} {task['title']}{due}")


def update_task(task_id: int, status: Optional[str] = None, priority: Optional[str] = None) -> None:
    """Update task status or priority."""
    data = load_data()
    
    for task in data["tasks"]:
        if task["id"] == task_id:
            if status:
                task["status"] = status
                if status == "done":
                    task["completed_at"] = datetime.now().isoformat()
                print(f"✅ Task #{task_id} status -> {status}")
            
            if priority:
                task["priority"] = priority
                print(f"✅ Task #{task_id} priority -> {priority}")
            
            save_data(data)
            return
    
    print(f"❌ Task #{task_id} not found")


def delete_task(task_id: int) -> None:
    """Delete a task."""
    data = load_data()
    
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            del data["tasks"][i]
            save_data(data)
            print(f"🗑️  Deleted task #{task_id}")
            return
    
    print(f"❌ Task #{task_id} not found")


def show_summary() -> None:
    """Show task summary."""
    data = load_data()
    
    total = len(data["tasks"])
    by_status = {"todo": 0, "in_progress": 0, "done": 0}
    by_priority = {"low": 0, "medium": 0, "high": 0, "urgent": 0}
    
    for task in data["tasks"]:
        by_status[task["status"]] = by_status.get(task["status"], 0) + 1
        by_priority[task["priority"]] = by_priority.get(task["priority"], 0) + 1
    
    print("\n📊 Task Summary")
    print("=" * 40)
    print(f"Total tasks: {total}")
    print(f"Projects: {len(data['projects'])}")
    print()
    print("By Status:")
    print(f"  ⬜ Todo:        {by_status['todo']}")
    print(f"  🔄 In Progress: {by_status['in_progress']}")
    print(f"  ✅ Done:        {by_status['done']}")
    print()
    print("By Priority:")
    print(f"  🟢 Low:    {by_priority['low']}")
    print(f"  🟡 Medium: {by_priority['medium']}")
    print(f"  🟠 High:   {by_priority['high']}")
    print(f"  🔴 Urgent: {by_priority['urgent']}")


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add project
    add_proj = subparsers.add_parser("project", help="Add project")
    add_proj.add_argument("name", help="Project name")
    add_proj.add_argument("-d", "--description", default="", help="Description")
    
    # Add task
    add = subparsers.add_parser("add", help="Add task")
    add.add_argument("title", help="Task title")
    add.add_argument("-p", "--project", help="Project name")
    add.add_argument("--priority", default="medium",
                    choices=["low", "medium", "high", "urgent"])
    add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    
    # List tasks
    list_cmd = subparsers.add_parser("list", help="List tasks")
    list_cmd.add_argument("-p", "--project", help="Filter by project")
    list_cmd.add_argument("-s", "--status", choices=["todo", "in_progress", "done"])
    list_cmd.add_argument("--priority", choices=["low", "medium", "high", "urgent"])
    list_cmd.add_argument("-a", "--all", action="store_true", help="Show completed")
    
    # Update task
    update = subparsers.add_parser("update", help="Update task")
    update.add_argument("id", type=int, help="Task ID")
    update.add_argument("-s", "--status", choices=["todo", "in_progress", "done"])
    update.add_argument("-p", "--priority", choices=["low", "medium", "high", "urgent"])
    
    # Done shortcut
    done = subparsers.add_parser("done", help="Mark task as done")
    done.add_argument("id", type=int, help="Task ID")
    
    # Delete task
    delete = subparsers.add_parser("delete", help="Delete task")
    delete.add_argument("id", type=int, help="Task ID")
    
    # Summary
    subparsers.add_parser("summary", help="Show summary")
    
    args = parser.parse_args()
    
    if args.command == "project":
        add_project(args.name, args.description)
    elif args.command == "add":
        add_task(args.title, args.project, args.priority, args.due)
    elif args.command == "list":
        list_tasks(args.project, args.status, args.priority, args.all)
    elif args.command == "update":
        update_task(args.id, args.status, args.priority)
    elif args.command == "done":
        update_task(args.id, status="done")
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "summary":
        show_summary()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
