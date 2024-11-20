#!/usr/bin/env python3
"""Git Helper"""
import subprocess

def run_git(args):
    return subprocess.run(["git"]+args, capture_output=True, text=True)

def status_pretty():
    r = run_git(["status","-sb"])
    if r.returncode == 0: print(r.stdout)
