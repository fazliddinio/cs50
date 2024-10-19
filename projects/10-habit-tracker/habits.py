#!/usr/bin/env python3
"""
Habit Tracker - Track your daily habits
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from collections import defaultdict


HABITS_FILE = Path.home() / ".habit_tracker.json"


def load_data() -> Dict:
    """Load habits data."""
    if not HABITS_FILE.exists():
        return {"habits": {}, "log": {}}
    with open(HABITS_FILE, "r") as f:
        return json.load(f)


def save_data(data: Dict) -> None:
    """Save habits data."""
    with open(HABITS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_habit(name: str, frequency: str = "daily", goal: int = 1) -> None:
    """Add a new habit to track."""
    data = load_data()
    
    habit_id = name.lower().replace(" ", "_")
    
    if habit_id in data["habits"]:
        print(f"❌ Habit '{name}' already exists")
        return
    
    data["habits"][habit_id] = {
        "name": name,
        "frequency": frequency,
        "goal": goal,
        "created_at": date.today().isoformat(),
        "streak": 0,
        "best_streak": 0,
    }
    
    save_data(data)
    print(f"✅ Added habit: {name}")


def log_habit(habit_name: str, count: int = 1) -> None:
    """Log habit completion."""
    data = load_data()
    habit_id = habit_name.lower().replace(" ", "_")
    
    if habit_id not in data["habits"]:
        print(f"❌ Habit '{habit_name}' not found")
        return
    
    today = date.today().isoformat()
    
    if today not in data["log"]:
        data["log"][today] = {}
    
    if habit_id not in data["log"][today]:
        data["log"][today][habit_id] = 0
    
    data["log"][today][habit_id] += count
    
    # Update streak
    habit = data["habits"][habit_id]
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    if yesterday in data["log"] and habit_id in data["log"][yesterday]:
        habit["streak"] += 1
    else:
        habit["streak"] = 1
    
    habit["best_streak"] = max(habit["streak"], habit["best_streak"])
    
    save_data(data)
    print(f"✅ Logged: {habit['name']} ({data['log'][today][habit_id]}x today)")
    print(f"🔥 Current streak: {habit['streak']} days")


def show_habits() -> None:
    """Show all habits and today's progress."""
    data = load_data()
    
    if not data["habits"]:
        print("📭 No habits yet! Add one with: habit add 'habit name'")
        return
    
    today = date.today().isoformat()
    today_log = data["log"].get(today, {})
    
    print(f"\n📊 Habit Tracker - {today}")
    print("=" * 50)
    print(f"{'Habit':<20} {'Today':>8} {'Goal':>6} {'Streak':>8}")
    print("-" * 50)
    
    for habit_id, habit in data["habits"].items():
        done = today_log.get(habit_id, 0)
        goal = habit["goal"]
        status = "✅" if done >= goal else "⬜"
        
        print(f"{status} {habit['name']:<17} {done:>6} / {goal:<4} {habit['streak']:>6}🔥")
    
    print("-" * 50)


def show_stats(habit_name: Optional[str] = None, days: int = 7) -> None:
    """Show habit statistics."""
    data = load_data()
    
    if habit_name:
        habit_id = habit_name.lower().replace(" ", "_")
        if habit_id not in data["habits"]:
            print(f"❌ Habit '{habit_name}' not found")
            return
        habits_to_show = {habit_id: data["habits"][habit_id]}
    else:
        habits_to_show = data["habits"]
    
    print(f"\n📈 Statistics (Last {days} days)")
    print("=" * 50)
    
    for habit_id, habit in habits_to_show.items():
        print(f"\n{habit['name']}")
        print("-" * 30)
        
        # Last N days
        total = 0
        calendar = []
        
        for i in range(days - 1, -1, -1):
            day = (date.today() - timedelta(days=i)).isoformat()
            count = data["log"].get(day, {}).get(habit_id, 0)
            total += count
            calendar.append("█" if count >= habit["goal"] else "░")
        
        print(f"Calendar: {''.join(calendar)}")
        print(f"Completed: {sum(1 for c in calendar if c == '█')}/{days} days")
        print(f"Total count: {total}")
        print(f"Current streak: {habit['streak']} days")
        print(f"Best streak: {habit['best_streak']} days")


def delete_habit(habit_name: str) -> None:
    """Delete a habit."""
    data = load_data()
    habit_id = habit_name.lower().replace(" ", "_")
    
    if habit_id in data["habits"]:
        del data["habits"][habit_id]
        save_data(data)
        print(f"🗑️  Deleted: {habit_name}")
    else:
        print(f"❌ Habit '{habit_name}' not found")


def main():
    parser = argparse.ArgumentParser(description="Habit Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add = subparsers.add_parser("add", help="Add a new habit")
    add.add_argument("name", help="Habit name")
    add.add_argument("-f", "--frequency", default="daily", 
                    choices=["daily", "weekly"], help="Frequency")
    add.add_argument("-g", "--goal", type=int, default=1, help="Daily goal")
    
    # Log command
    log = subparsers.add_parser("log", help="Log habit completion")
    log.add_argument("habit", help="Habit name")
    log.add_argument("-c", "--count", type=int, default=1, help="Count")
    
    # List command
    subparsers.add_parser("list", help="Show all habits")
    
    # Stats command
    stats = subparsers.add_parser("stats", help="Show statistics")
    stats.add_argument("habit", nargs="?", help="Habit name (optional)")
    stats.add_argument("-d", "--days", type=int, default=7, help="Number of days")
    
    # Delete command
    delete = subparsers.add_parser("delete", help="Delete a habit")
    delete.add_argument("habit", help="Habit name")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_habit(args.name, args.frequency, args.goal)
    elif args.command == "log":
        log_habit(args.habit, args.count)
    elif args.command == "list":
        show_habits()
    elif args.command == "stats":
        show_stats(args.habit, args.days)
    elif args.command == "delete":
        delete_habit(args.habit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# streak test
