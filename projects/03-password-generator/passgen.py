#!/usr/bin/env python3
"""Password Generator"""
import secrets
import string

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    print(generate_password())

# char type options

# passphrase

# strength checker
