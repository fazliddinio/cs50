#!/usr/bin/env python3
"""
Quiz Game - Interactive command-line quiz application
"""
import argparse
import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Question:
    """Quiz question data class."""
    question: str
    options: List[str]
    correct: int
    explanation: str = ""


# Sample quiz data
SAMPLE_QUIZZES = {
    "python": [
        Question(
            "What is the output of print(type([]))?",
            ["<class 'list'>", "<class 'tuple'>", "<class 'array'>", "<class 'set'>"],
            0,
            "Empty brackets [] create a list in Python"
        ),
        Question(
            "Which method is used to add an element to a list?",
            ["add()", "append()", "insert()", "push()"],
            1,
            "append() adds an element to the end of a list"
        ),
        Question(
            "What is a decorator in Python?",
            ["A design pattern", "A function that modifies another function", 
             "A class attribute", "A type of loop"],
            1,
            "Decorators wrap functions to extend their behavior"
        ),
        Question(
            "What does 'self' refer to in a class method?",
            ["The class itself", "The current instance", "The parent class", "Nothing special"],
            1,
            "'self' refers to the instance calling the method"
        ),
        Question(
            "Which is NOT a built-in data type in Python?",
            ["list", "array", "dict", "set"],
            1,
            "Array is not built-in; you need to import it from array module or use numpy"
        ),
    ],
    "git": [
        Question(
            "What command creates a new Git repository?",
            ["git new", "git create", "git init", "git start"],
            2,
            "git init initializes a new Git repository"
        ),
        Question(
            "How do you stage all changes for commit?",
            ["git stage .", "git add .", "git commit -a", "git push"],
            1,
            "git add . stages all changes in the current directory"
        ),
        Question(
            "What does 'git pull' do?",
            ["Pushes changes", "Fetches and merges", "Creates a branch", "Deletes remote"],
            1,
            "git pull fetches from remote and merges into current branch"
        ),
    ],
    "linux": [
        Question(
            "What command lists files in a directory?",
            ["dir", "ls", "list", "show"],
            1,
            "ls (list) shows directory contents"
        ),
        Question(
            "How do you change to the home directory?",
            ["cd home", "cd ~", "cd /", "cd .."],
            1,
            "~ is a shortcut for the home directory"
        ),
        Question(
            "What does 'chmod 755' do?",
            ["Deletes a file", "Changes ownership", "Sets permissions rwxr-xr-x", "Moves a file"],
            2,
            "755 = rwx for owner, rx for group and others"
        ),
    ],
}


def run_quiz(topic: str, num_questions: int = 5, shuffle: bool = True) -> Dict:
    """Run an interactive quiz."""
    if topic not in SAMPLE_QUIZZES:
        print(f"❌ Topic '{topic}' not found")
        print(f"Available topics: {', '.join(SAMPLE_QUIZZES.keys())}")
        return {}
    
    questions = SAMPLE_QUIZZES[topic].copy()
    if shuffle:
        random.shuffle(questions)
    
    questions = questions[:num_questions]
    
    print(f"\n🎯 {topic.upper()} Quiz - {len(questions)} questions")
    print("=" * 50)
    
    score = 0
    results = []
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q.question}")
        print("-" * 40)
        
        for j, option in enumerate(q.options, 1):
            print(f"  {j}. {option}")
        
        while True:
            try:
                answer = int(input("\nYour answer (1-4): ")) - 1
                if 0 <= answer < len(q.options):
                    break
                print("Please enter 1-4")
            except ValueError:
                print("Please enter a number")
            except KeyboardInterrupt:
                print("\n\n⏸️  Quiz cancelled")
                return {"score": score, "total": i - 1}
        
        if answer == q.correct:
            print("✅ Correct!")
            score += 1
            results.append(True)
        else:
            print(f"❌ Wrong! Correct answer: {q.options[q.correct]}")
            results.append(False)
        
        if q.explanation:
            print(f"💡 {q.explanation}")
    
    # Results
    percentage = (score / len(questions)) * 100
    
    print("\n" + "=" * 50)
    print(f"🏆 Final Score: {score}/{len(questions)} ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("🌟 Excellent! Great job!")
    elif percentage >= 60:
        print("👍 Good work! Keep practicing!")
    else:
        print("📚 Keep studying! You'll improve!")
    
    return {
        "topic": topic,
        "score": score,
        "total": len(questions),
        "percentage": percentage,
        "results": results,
    }


def list_topics() -> None:
    """List available quiz topics."""
    print("\n📚 Available Quiz Topics:")
    print("-" * 30)
    for topic, questions in SAMPLE_QUIZZES.items():
        print(f"  • {topic}: {len(questions)} questions")


def main():
    parser = argparse.ArgumentParser(description="Quiz Game CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Quiz command
    quiz = subparsers.add_parser("play", help="Start a quiz")
    quiz.add_argument("topic", help="Quiz topic")
    quiz.add_argument("-n", "--num", type=int, default=5, help="Number of questions")
    quiz.add_argument("--no-shuffle", action="store_true", help="Don't shuffle questions")
    
    # List command
    subparsers.add_parser("list", help="List available topics")
    
    args = parser.parse_args()
    
    if args.command == "play":
        run_quiz(args.topic, args.num, not args.no_shuffle)
    elif args.command == "list":
        list_topics()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
