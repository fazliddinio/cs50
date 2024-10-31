#!/usr/bin/env python3
"""
Hangman Game - Classic word guessing game
"""
import random


WORDS = {
    "python": ["function", "variable", "decorator", "iterator", "generator",
               "lambda", "module", "package", "exception", "inheritance"],
    "animals": ["elephant", "giraffe", "penguin", "dolphin", "butterfly",
                "crocodile", "kangaroo", "octopus", "chameleon", "tortoise"],
    "countries": ["brazil", "australia", "germany", "japan", "canada",
                  "mexico", "france", "egypt", "india", "norway"],
}

HANGMAN_STAGES = [
    """
  -----
  |   |
      |
      |
      |
      |
  =========""",
    """
  -----
  |   |
  O   |
      |
      |
      |
  =========""",
    """
  -----
  |   |
  O   |
  |   |
      |
      |
  =========""",
    """
  -----
  |   |
  O   |
 /|   |
      |
      |
  =========""",
    """
  -----
  |   |
  O   |
 /|\\  |
      |
      |
  =========""",
    """
  -----
  |   |
  O   |
 /|\\  |
 /    |
      |
  =========""",
    """
  -----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
  ========="""
]


def display_word(word, guessed_letters):
    """Display the word with guessed letters revealed."""
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in word
    )


def play_hangman(category=None):
    """Play a game of hangman."""
    if category and category in WORDS:
        word_list = WORDS[category]
    else:
        word_list = [w for words in WORDS.values() for w in words]
    
    word = random.choice(word_list).lower()
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = len(HANGMAN_STAGES) - 1
    
    print("\n" + "=" * 30)
    print("    HANGMAN")
    print("=" * 30)
    
    if category:
        print(f"Category: {category}")
    print(f"Word has {len(word)} letters\n")
    
    while wrong_guesses < max_wrong:
        # Display current state
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"\n  {display_word(word, guessed_letters)}")
        print(f"\n  Guessed: {', '.join(sorted(guessed_letters)) or 'none'}")
        print(f"  Wrong guesses: {wrong_guesses}/{max_wrong}")
        
        # Check if won
        if all(letter in guessed_letters for letter in word):
            print(f"\nYou won! The word was: {word}")
            return True
        
        # Get guess
        try:
            guess = input("\n  Guess a letter: ").lower().strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\nThe word was: {word}")
            return False
        
        if len(guess) != 1 or not guess.isalpha():
            print("  Please enter a single letter.")
            continue
        
        if guess in guessed_letters:
            print("  Already guessed that letter!")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"  '{guess}' is in the word!")
        else:
            wrong_guesses += 1
            print(f"  '{guess}' is not in the word.")
    
    # Lost
    print(HANGMAN_STAGES[wrong_guesses])
    print(f"\nGame over! The word was: {word}")
    return False


def main():
    """Main game loop."""
    print("HANGMAN - Word Guessing Game")
    print("-" * 30)
    print("Categories:", ", ".join(WORDS.keys()))
    
    wins = 0
    games = 0
    
    while True:
        category = input("\nChoose category (or 'all'): ").strip().lower()
        if category == 'all':
            category = None
        
        result = play_hangman(category)
        games += 1
        if result:
            wins += 1
        
        print(f"\nScore: {wins}/{games}")
        
        try:
            again = input("Play again? (y/n): ").strip().lower()
            if again != 'y':
                break
        except (KeyboardInterrupt, EOFError):
            break
    
    print(f"\nFinal score: {wins}/{games}. Thanks for playing!")


if __name__ == "__main__":
    main()
