#!/usr/bin/env python3
"""Quiz Game"""
import random
from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    question: str
    options: List[str]
    correct: int
    explanation: str = ""

SAMPLE = [Question("What is type([])?", ["list","tuple","array","set"], 0, "[] creates a list")]

# git linux

# scoring
