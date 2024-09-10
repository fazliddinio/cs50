#!/usr/bin/env python3
"""Pomodoro Timer"""
import time, sys

def run_timer(mins, label="Timer"):
    remaining = mins * 60
    while remaining > 0:
        m, s = divmod(remaining, 60)
        sys.stdout.write(f"\r{label}: {m:02d}:{s:02d}")
        sys.stdout.flush()
        time.sleep(1)
        remaining -= 1
    print("\nDone!")
