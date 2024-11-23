#!/usr/bin/env python3
"""
Git Helper - Simplify common Git operations
"""
import argparse
import subprocess
import os
from datetime import datetime


def run_git(args: list, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=False
    )
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    return result


def status_pretty() -> None:
    """Show a pretty status."""
    result = run_git(["status", "-sb"])
    if result.returncode == 0:
        lines = result.stdout.strip().split("\n")
        
        print("\n📊 Git Status")
        print("=" * 40)
        
        # Branch info
        if lines:
            print(f"🌿 {lines[0]}")
        
        # Changed files
        staged = []
        modified = []
        untracked = []
        
        for line in lines[1:]:
            if line.startswith("A"):
                staged.append(line[3:])
            elif line.startswith("M"):
                modified.append(line[3:])
            elif line.startswith("??"):
                untracked.append(line[3:])
        
        if staged:
            print(f"\n✅ Staged ({len(staged)}):")
            for f in staged[:5]:
                print(f"   + {f}")
        
        if modified:
            print(f"\n📝 Modified ({len(modified)}):")
            for f in modified[:5]:
                print(f"   ~ {f}")
        
        if untracked:
            print(f"\n❓ Untracked ({len(untracked)}):")
            for f in untracked[:5]:
                print(f"   ? {f}")
        
        if not (staged or modified or untracked):
            print("\n✨ Working tree clean!")


def log_pretty(count: int = 10) -> None:
    """Show pretty log."""
    result = run_git([
        "log", 
        f"-{count}",
        "--pretty=format:%h|%s|%cr|%an",
        "--abbrev-commit"
    ])
    
    if result.returncode == 0:
        print("\n📜 Recent Commits")
        print("=" * 60)
        
        for line in result.stdout.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 4:
                hash_val, msg, time, author = parts[:4]
                msg = msg[:40] + "..." if len(msg) > 40 else msg
                print(f"  {hash_val} {msg:<43} ({time})")


def quick_commit(message: str) -> None:
    """Stage all and commit."""
    run_git(["add", "-A"])
    result = run_git(["commit", "-m", message])
    
    if result.returncode == 0:
        print(f"✅ Committed: {message}")
    else:
        print("❌ Nothing to commit or error occurred")


def create_branch(name: str) -> None:
    """Create and switch to new branch."""
    result = run_git(["checkout", "-b", name])
    
    if result.returncode == 0:
        print(f"✅ Created and switched to: {name}")


def sync() -> None:
    """Pull then push."""
    print("⬇️  Pulling...")
    pull = run_git(["pull"])
    
    if pull.returncode == 0:
        print("⬆️  Pushing...")
        push = run_git(["push"])
        if push.returncode == 0:
            print("✅ Synced!")


def undo_last() -> None:
    """Undo last commit but keep changes."""
    result = run_git(["reset", "--soft", "HEAD~1"])
    
    if result.returncode == 0:
        print("✅ Last commit undone (changes preserved)")


def stash_work(message: str = None) -> None:
    """Stash current work."""
    args = ["stash", "push"]
    if message:
        args.extend(["-m", message])
    
    result = run_git(args)
    if result.returncode == 0:
        print("✅ Work stashed!")


def list_branches() -> None:
    """List all branches."""
    result = run_git(["branch", "-a", "-v"])
    
    if result.returncode == 0:
        print("\n🌿 Branches")
        print("=" * 50)
        print(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Git Helper CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status
    subparsers.add_parser("status", aliases=["st"], help="Pretty status")
    
    # Log
    log = subparsers.add_parser("log", aliases=["lg"], help="Pretty log")
    log.add_argument("-n", "--count", type=int, default=10, help="Number of commits")
    
    # Quick commit
    commit = subparsers.add_parser("commit", aliases=["cm"], help="Quick commit")
    commit.add_argument("message", help="Commit message")
    
    # Branch
    branch = subparsers.add_parser("branch", aliases=["br"], help="Create branch")
    branch.add_argument("name", nargs="?", help="Branch name")
    
    # Sync
    subparsers.add_parser("sync", help="Pull then push")
    
    # Undo
    subparsers.add_parser("undo", help="Undo last commit")
    
    # Stash
    stash = subparsers.add_parser("stash", help="Stash work")
    stash.add_argument("-m", "--message", help="Stash message")
    
    args = parser.parse_args()
    
    if args.command in ["status", "st"]:
        status_pretty()
    elif args.command in ["log", "lg"]:
        log_pretty(args.count)
    elif args.command in ["commit", "cm"]:
        quick_commit(args.message)
    elif args.command in ["branch", "br"]:
        if args.name:
            create_branch(args.name)
        else:
            list_branches()
    elif args.command == "sync":
        sync()
    elif args.command == "undo":
        undo_last()
    elif args.command == "stash":
        stash_work(args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# test states
