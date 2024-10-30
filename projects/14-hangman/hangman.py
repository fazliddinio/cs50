#!/usr/bin/env python3
"""Hangman Game"""
import random

WORDS = ["python","function","variable","decorator"]

def play():
    word = random.choice(WORDS)
    guessed = set()
    wrong = 0
    while wrong < 6:
        display = " ".join(c if c in guessed else "_" for c in word)
        print(display)
        guess = input("Letter: ").lower()
        guessed.add(guess)
        if guess not in word: wrong += 1
        if all(c in guessed for c in word):
            print(f"You won! Word: {word}")
            return
    print(f"Game over! Word: {word}")
