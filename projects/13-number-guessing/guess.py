#!/usr/bin/env python3
"""
Number Guessing Game - Guess the number with hints
"""
import random
import time
from datetime import datetime


def play_game(min_num=1, max_num=100, max_attempts=None):
    """Play a number guessing game."""
    secret = random.randint(min_num, max_num)
    
    if max_attempts is None:
        # Calculate fair number of attempts
        import math
        max_attempts = int(math.log2(max_num - min_num + 1)) + 1
    
    print(f"\nI'm thinking of a number between {min_num} and {max_num}")
    print(f"You have {max_attempts} attempts. Good luck!\n")
    
    attempts = 0
    start_time = time.time()
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue
        except (KeyboardInterrupt, EOFError):
            print(f"\nThe number was {secret}. Better luck next time!")
            return None
        
        attempts += 1
        
        if guess == secret:
            elapsed = round(time.time() - start_time, 1)
            print(f"\nCongratulations! You got it in {attempts} attempts!")
            print(f"Time: {elapsed} seconds")
            return attempts
        elif guess < secret:
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Too low! ({remaining} attempts left)")
        else:
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Too high! ({remaining} attempts left)")
    
    print(f"\nGame over! The number was {secret}")
    return None


def play_multiple_rounds():
    """Play multiple rounds and track scores."""
    scores = []
    
    print("=" * 40)
    print("   NUMBER GUESSING GAME")
    print("=" * 40)
    
    while True:
        result = play_game()
        if result is not None:
            scores.append(result)
        
        print(f"\nGames played: {len(scores)}")
        if scores:
            print(f"Average attempts: {sum(scores) / len(scores):.1f}")
            print(f"Best game: {min(scores)} attempts")
        
        try:
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again != 'y':
                break
        except (KeyboardInterrupt, EOFError):
            break
    
    print("\nThanks for playing!")
    if scores:
        print(f"Final stats: {len(scores)} games, best: {min(scores)} attempts")


if __name__ == "__main__":
    play_multiple_rounds()

# validation
