#!/usr/bin/env python3
"""
Password Generator - Generate secure passwords
"""
import argparse
import secrets
import string
import pyperclip
from typing import Optional


def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    special: bool = True,
    exclude_chars: str = "",
) -> str:
    """Generate a secure random password."""
    characters = ""
    
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if special:
        characters += string.punctuation
    
    # Remove excluded characters
    for char in exclude_chars:
        characters = characters.replace(char, "")
    
    if not characters:
        raise ValueError("Must include at least one character type")
    
    # Generate password
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


def generate_passphrase(num_words: int = 4, separator: str = "-") -> str:
    """Generate a passphrase from random words."""
    # Simple word list (in production, use a larger list)
    words = [
        "apple", "banana", "cherry", "dragon", "eagle", "falcon",
        "garden", "harbor", "island", "jungle", "knight", "lemon",
        "mountain", "nebula", "ocean", "planet", "quantum", "river",
        "sunset", "thunder", "umbrella", "velocity", "winter", "xenon",
        "yellow", "zephyr", "anchor", "bridge", "castle", "diamond"
    ]
    
    selected = [secrets.choice(words) for _ in range(num_words)]
    return separator.join(selected)


def check_strength(password: str) -> dict:
    """Check password strength."""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    # Character type checks
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add digits")
    
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Rating
    if score <= 2:
        rating = "Weak"
        emoji = "🔴"
    elif score <= 4:
        rating = "Fair"
        emoji = "🟡"
    elif score <= 5:
        rating = "Good"
        emoji = "🟢"
    else:
        rating = "Strong"
        emoji = "💪"
    
    return {
        "score": score,
        "max_score": 7,
        "rating": rating,
        "emoji": emoji,
        "feedback": feedback,
    }


def main():
    parser = argparse.ArgumentParser(description="Password Generator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate password")
    gen_parser.add_argument("-l", "--length", type=int, default=16, help="Password length")
    gen_parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase")
    gen_parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase")
    gen_parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    gen_parser.add_argument("--no-special", action="store_true", help="Exclude special chars")
    gen_parser.add_argument("-e", "--exclude", default="", help="Characters to exclude")
    gen_parser.add_argument("-c", "--copy", action="store_true", help="Copy to clipboard")
    gen_parser.add_argument("-n", "--count", type=int, default=1, help="Number to generate")
    
    # Passphrase command
    phrase_parser = subparsers.add_parser("phrase", help="Generate passphrase")
    phrase_parser.add_argument("-w", "--words", type=int, default=4, help="Number of words")
    phrase_parser.add_argument("-s", "--separator", default="-", help="Word separator")
    phrase_parser.add_argument("-c", "--copy", action="store_true", help="Copy to clipboard")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check password strength")
    check_parser.add_argument("password", help="Password to check")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        print("\n🔐 Generated Password(s):")
        print("-" * 40)
        for i in range(args.count):
            password = generate_password(
                length=args.length,
                uppercase=not args.no_upper,
                lowercase=not args.no_lower,
                digits=not args.no_digits,
                special=not args.no_special,
                exclude_chars=args.exclude,
            )
            print(password)
            if args.copy and i == 0:
                try:
                    pyperclip.copy(password)
                    print("📋 Copied to clipboard!")
                except:
                    pass
    
    elif args.command == "phrase":
        passphrase = generate_passphrase(args.words, args.separator)
        print(f"\n🔐 Passphrase: {passphrase}")
        if args.copy:
            try:
                pyperclip.copy(passphrase)
                print("📋 Copied to clipboard!")
            except:
                pass
    
    elif args.command == "check":
        result = check_strength(args.password)
        print(f"\n{result['emoji']} Strength: {result['rating']}")
        print(f"   Score: {result['score']}/{result['max_score']}")
        if result['feedback']:
            print("   Suggestions:")
            for tip in result['feedback']:
                print(f"   - {tip}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
