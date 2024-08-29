#!/usr/bin/env python3
"""
Expense Tracker CLI - Track your daily expenses
"""
import argparse
import json
import csv
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional
from collections import defaultdict


EXPENSES_FILE = Path.home() / ".expense_tracker.json"


def load_expenses() -> List[dict]:
    """Load expenses from file."""
    if not EXPENSES_FILE.exists():
        return []
    with open(EXPENSES_FILE, "r") as f:
        return json.load(f)


def save_expenses(expenses: List[dict]) -> None:
    """Save expenses to file."""
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount: float, category: str, description: str = "") -> None:
    """Add a new expense."""
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category.lower(),
        "description": description,
        "date": date.today().isoformat(),
        "timestamp": datetime.now().isoformat(),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"💸 Added: ${amount:.2f} for {category}")


def list_expenses(limit: int = 10, category: Optional[str] = None) -> None:
    """List recent expenses."""
    expenses = load_expenses()
    
    if category:
        expenses = [e for e in expenses if e["category"] == category.lower()]
    
    if not expenses:
        print("📭 No expenses found!")
        return
    
    recent = expenses[-limit:][::-1]
    
    print("\n💰 Recent Expenses:")
    print("-" * 60)
    print(f"{'Date':<12} {'Category':<12} {'Amount':>10} {'Description'}")
    print("-" * 60)
    
    for exp in recent:
        desc = exp.get("description", "")[:20]
        print(f"{exp['date']:<12} {exp['category']:<12} ${exp['amount']:>9.2f} {desc}")
    
    print("-" * 60)
    total = sum(e["amount"] for e in recent)
    print(f"{'Total:':<24} ${total:>9.2f}")


def summary(month: Optional[str] = None) -> None:
    """Show expense summary by category."""
    expenses = load_expenses()
    
    if month:
        expenses = [e for e in expenses if e["date"].startswith(month)]
    
    if not expenses:
        print("📭 No expenses found!")
        return
    
    by_category = defaultdict(float)
    for exp in expenses:
        by_category[exp["category"]] += exp["amount"]
    
    total = sum(by_category.values())
    
    print("\n📊 Expense Summary:")
    print("-" * 40)
    
    for cat, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = (amount / total) * 100
        bar = "█" * int(pct / 5)
        print(f"{cat:<12} ${amount:>9.2f} ({pct:>5.1f}%) {bar}")
    
    print("-" * 40)
    print(f"{'TOTAL':<12} ${total:>9.2f}")


def export_csv(filename: str) -> None:
    """Export expenses to CSV."""
    expenses = load_expenses()
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
        writer.writeheader()
        for exp in expenses:
            writer.writerow({
                "date": exp["date"],
                "category": exp["category"],
                "amount": exp["amount"],
                "description": exp.get("description", ""),
            })
    
    print(f"📁 Exported {len(expenses)} expenses to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("amount", type=float, help="Amount spent")
    add_parser.add_argument("category", help="Expense category")
    add_parser.add_argument("-d", "--description", default="", help="Description")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("-n", "--limit", type=int, default=10, help="Number to show")
    list_parser.add_argument("-c", "--category", help="Filter by category")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show summary")
    summary_parser.add_argument("-m", "--month", help="Month (YYYY-MM)")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("filename", help="Output filename")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_expense(args.amount, args.category, args.description)
    elif args.command == "list":
        list_expenses(args.limit, args.category)
    elif args.command == "summary":
        summary(args.month)
    elif args.command == "export":
        export_csv(args.filename)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# test monthly

# fixed percentages
