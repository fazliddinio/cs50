#!/usr/bin/env python3
"""
Pomodoro Timer - Focus and productivity timer
"""
import argparse
import time
import sys
from datetime import datetime, timedelta


def format_time(seconds: int) -> str:
    """Format seconds as MM:SS."""
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


def notify(message: str) -> None:
    """Send notification (cross-platform)."""
    print(f"\n🔔 {message}")
    # Try to make a sound
    try:
        print("\a")  # Terminal bell
    except:
        pass


def run_timer(duration_minutes: int, label: str = "Timer") -> None:
    """Run a countdown timer."""
    total_seconds = duration_minutes * 60
    remaining = total_seconds
    
    print(f"\n⏱️  {label}: {duration_minutes} minutes")
    print("-" * 30)
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    try:
        while remaining > 0:
            # Progress bar
            progress = (total_seconds - remaining) / total_seconds
            bar_width = 20
            filled = int(bar_width * progress)
            bar = "█" * filled + "░" * (bar_width - filled)
            
            # Display
            sys.stdout.write(f"\r[{bar}] {format_time(remaining)} remaining")
            sys.stdout.flush()
            
            time.sleep(1)
            remaining -= 1
        
        print()
        notify(f"{label} completed!")
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Timer paused")
        return False
    
    return True


def pomodoro_session(
    work_minutes: int = 25,
    short_break: int = 5,
    long_break: int = 15,
    sessions: int = 4,
) -> None:
    """Run a full Pomodoro session."""
    completed = 0
    
    print("\n🍅 Pomodoro Timer")
    print("=" * 40)
    print(f"Work: {work_minutes} min | Short break: {short_break} min")
    print(f"Long break: {long_break} min | Sessions: {sessions}")
    print("=" * 40)
    
    try:
        for i in range(sessions):
            # Work session
            print(f"\n📍 Session {i + 1}/{sessions}")
            if not run_timer(work_minutes, "🔴 Focus Time"):
                break
            
            completed += 1
            
            # Break
            if i < sessions - 1:
                if (i + 1) % 4 == 0:
                    run_timer(long_break, "🟢 Long Break")
                else:
                    run_timer(short_break, "🟡 Short Break")
        
        print("\n" + "=" * 40)
        print(f"🎉 Completed {completed}/{sessions} sessions!")
        print(f"⏱️  Total focus time: {completed * work_minutes} minutes")
        
    except KeyboardInterrupt:
        print(f"\n\n📊 Completed {completed} sessions before stopping")


def main():
    parser = argparse.ArgumentParser(description="Pomodoro Timer")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Start command
    start = subparsers.add_parser("start", help="Start Pomodoro session")
    start.add_argument("-w", "--work", type=int, default=25, help="Work minutes")
    start.add_argument("-s", "--short-break", type=int, default=5, help="Short break")
    start.add_argument("-l", "--long-break", type=int, default=15, help="Long break")
    start.add_argument("-n", "--sessions", type=int, default=4, help="Number of sessions")
    
    # Timer command
    timer = subparsers.add_parser("timer", help="Simple countdown timer")
    timer.add_argument("minutes", type=int, help="Timer duration in minutes")
    timer.add_argument("-l", "--label", default="Timer", help="Timer label")
    
    args = parser.parse_args()
    
    if args.command == "start":
        pomodoro_session(
            args.work,
            args.short_break,
            args.long_break,
            args.sessions,
        )
    elif args.command == "timer":
        run_timer(args.minutes, args.label)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
