# file I/O practice
import json
import os

def write_text_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def read_text_file(filename):
    with open(filename, "r") as f:
        return f.read()

# json csv added

# pathlib operations
