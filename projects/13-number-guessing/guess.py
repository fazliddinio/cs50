#!/usr/bin/env python3
"""Number Guessing Game"""
import random

def play():
    secret = random.randint(1, 100)
    print("Guess a number between 1 and 100")
    while True:
        guess = int(input("Your guess: "))
        if guess == secret:
            print("Correct!")
            break
        print("Too low!" if guess < secret else "Too high!")

if __name__ == "__main__":
    play()

# attempts limit
