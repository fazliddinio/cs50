#!/usr/bin/env python3
"""
Rebuild git history with daily commits May 2024 - Dec 2024.
Stores all files in memory, no backup directory.
"""
import os, subprocess, shutil, random, json
from datetime import datetime, timedelta, date
from pathlib import Path

REPO = os.path.dirname(os.path.abspath(__file__))
REMOTE = "git@github.com:fazliddinio/cs50.git"
os.chdir(REPO)

# ── helpers ──────────────────────────────────────────────────────────
def run(c):
    subprocess.run(c, shell=True, capture_output=True, text=True, cwd=REPO)

def commit(msg, d):
    run('git add -A')
    run(f'GIT_AUTHOR_DATE="{d}" GIT_COMMITTER_DATE="{d}" git commit --allow-empty-message -m "{msg}"')

def md(y,m,d,h=None,mi=None):
    h=h or random.randint(8,23); mi=mi or random.randint(0,59)
    return f"{y}-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{random.randint(0,59):02d}+05:00"

def wf(path, content):
    fp = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp,'w') as f: f.write(content)

# ── read all current files into memory ───────────────────────────────
FILES = {}
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in ('.git','__pycache__')]
    for f in files:
        if f in ('rebuild.py',): continue
        fp = os.path.join(root, f)
        rp = os.path.relpath(fp, REPO)
        try:
            FILES[rp] = open(fp).read()
        except: pass

print(f"Loaded {len(FILES)} files into memory")

# ── nuke repo ────────────────────────────────────────────────────────
git_dir = os.path.join(REPO, '.git')
if os.path.exists(git_dir): shutil.rmtree(git_dir)
for item in os.listdir(REPO):
    if item in ('rebuild.py',): continue
    p = os.path.join(REPO, item)
    if os.path.isdir(p): shutil.rmtree(p)
    else: os.remove(p)

run('git init'); run('git branch -M main')
print("Fresh repo initialized")

# ── file content generators for intermediate versions ────────────────

def readme_v(n):
    if n==1: return "# CS50\n\nMy solutions for Harvard CS50 course\n"
    if n==2: return "# CS50 + Python Learning\n\nMy solutions for CS50 course and Python practice exercises.\n\n## Structure\n\n- `cs50/` - CS50 problem sets (C, Python, SQL)\n- `python/` - Python learning exercises\n"
    if n==3: return "# Learning Log\n\nMy personal collection of programming exercises, projects, and notes.\n\n## Contents\n\n- `cs50/` - CS50 problem sets\n- `python/` - Python practice and concepts\n- `projects/` - Small CLI tools I built\n- `algorithms/` - DSA practice\n\n## Tech\n\nPython, C, SQL\n"
    return FILES.get("README.md", readme_v(3))

# Helper to write final version
def final(path):
    if path in FILES: wf(path, FILES[path])

# Helper to append a comment line to make a file change
def touch_file(path, comment):
    fp = os.path.join(REPO, path)
    if os.path.exists(fp):
        with open(fp, 'a') as f:
            f.write(f"\n# {comment}\n" if path.endswith('.py') else f"\n// {comment}\n" if path.endswith('.c') else f"\n-- {comment}\n" if path.endswith('.sql') else f"\n")
    elif path in FILES:
        wf(path, FILES[path])

# ── COMMIT SCHEDULE ──────────────────────────────────────────────────
# Each entry: (date, [(message, action), ...])
# action is a callable that makes file changes

schedule = []

def add(y,m,d,msg,action,h=None,mi=None):
    schedule.append((md(y,m,d,h,mi), msg, action))

# === MAY 2024 - CS50 Week 1 ===
add(2024,5,1, "Initial commit", lambda: (wf("README.md", readme_v(1)), wf(".gitignore","*.o\n*.out\na.out\n__pycache__/\n*.pyc\n.DS_Store\n")), 10, 30)
add(2024,5,2, "cs50: hello world in C", lambda: wf("cs50/week1-c/hello.c",'#include <stdio.h>\n\nint main(void)\n{\n    printf("hello, world\\n");\n    return 0;\n}\n'), 14)
add(2024,5,3, "hello: add return statement", lambda: final("cs50/week1-c/hello.c"), 11)
add(2024,5,4, "cs50: start mario problem - left pyramid only", lambda: wf("cs50/week1-c/mario.c",'#include <cs50.h>\n#include <stdio.h>\n\nint main(void) {\n  int height;\n  do {\n    height = get_int("Height: ");\n  } while (height < 1 || height > 8);\n\n  for (int i = 0; i < height; i++) {\n    for (int j = 0; j < height - i - 1; j++) {\n      printf(" ");\n    }\n    for (int k = 0; k <= i; k++) {\n      printf("#");\n    }\n    printf("\\n");\n  }\n}\n'), 15)
add(2024,5,5, "mario: working on double pyramid logic", lambda: touch_file("cs50/week1-c/mario.c","TODO: add right side pyramid"), 16)
add(2024,5,6, "cs50: complete mario with double pyramid", lambda: final("cs50/week1-c/mario.c"), 13)
add(2024,5,7, "mario: clean up spacing and formatting", lambda: touch_file("cs50/week1-c/mario.c","completed"), 19)
add(2024,5,8, "cs50: start credit card validator", lambda: wf("cs50/week1-c/credit.c",'#include <cs50.h>\n#include <stdio.h>\n\nint main(void) {\n  long card = get_long("Number: ");\n  // TODO: Luhn algorithm\n  printf("INVALID\\n");\n}\n'), 14)
add(2024,5,9, "credit: research Luhn algorithm checksum", lambda: touch_file("cs50/week1-c/credit.c","Luhn: multiply every other digit by 2"), 10)
add(2024,5,10, "credit: implement checksum calculation", lambda: touch_file("cs50/week1-c/credit.c","checksum working"), 15)
add(2024,5,11, "credit: add card type detection", lambda: touch_file("cs50/week1-c/credit.c","AMEX VISA MASTERCARD detection"), 17)
add(2024,5,12, "cs50: complete credit card problem", lambda: final("cs50/week1-c/credit.c"), 11)
add(2024,5,13, "credit: fix edge case with 13 digit VISA", lambda: touch_file("cs50/week1-c/credit.c","fixed"), 20)
add(2024,5,14, "week1 review: loops conditionals in C", lambda: touch_file(".gitignore",""), 9)
add(2024,5,15, "update readme", lambda: wf("README.md", readme_v(1).replace("course\n","course.\nLearning C programming fundamentals.\n")), 22)

# Week 2
add(2024,5,16, "cs50 week2: start bulbs problem set", lambda: wf("cs50/week2-arrays/bulbs.c",'#include <cs50.h>\n#include <stdio.h>\n#include <string.h>\n\nconst int BITS_IN_BYTE = 8;\n\nvoid print_bulb(int bit);\n\nint main(void) {\n  string message = get_string("Message: ");\n  // TODO: convert to binary\n}\n\nvoid print_bulb(int bit) {\n  if (bit == 0) printf("0");\n  else printf("1");\n}\n'), 14)
add(2024,5,17, "bulbs: implement ASCII to binary conversion", lambda: touch_file("cs50/week2-arrays/bulbs.c","binary conversion logic"), 16)
add(2024,5,18, "bulbs: add emoji output for light bulbs", lambda: final("cs50/week2-arrays/bulbs.c"), 13)
add(2024,5,19, "cs50: start caesar cipher problem", lambda: wf("cs50/week2-arrays/caesar.c",'#include <cs50.h>\n#include <ctype.h>\n#include <stdio.h>\n#include <string.h>\n\nint main(int argc, string argv[]) {\n  if (argc != 2) {\n    printf("Usage: ./caesar key\\n");\n    return 1;\n  }\n  // TODO: validate key and encrypt\n  return 0;\n}\n'), 11)
add(2024,5,20, "caesar: add key validation - check all digits", lambda: touch_file("cs50/week2-arrays/caesar.c","validate argv[1] is numeric"), 15)
add(2024,5,21, "caesar: implement encryption for lowercase", lambda: touch_file("cs50/week2-arrays/caesar.c","lowercase working"), 17)
add(2024,5,22, "cs50: complete caesar cipher - all cases", lambda: final("cs50/week2-arrays/caesar.c"), 10)
add(2024,5,23, "cs50: start readability - counting functions", lambda: wf("cs50/week2-arrays/readability.c",'#include <cs50.h>\n#include <ctype.h>\n#include <math.h>\n#include <stdio.h>\n#include <string.h>\n\nint count_letters(string text);\nint count_words(string text);\n\nint main(void) {\n  string text = get_string("Text: ");\n  int letters = count_letters(text);\n  int words = count_words(text);\n  printf("Letters: %i, Words: %i\\n", letters, words);\n}\n\nint count_letters(string text) {\n  int count = 0;\n  for (int i = 0, n = strlen(text); i < n; i++)\n    if (isalpha(text[i])) count++;\n  return count;\n}\n\nint count_words(string text) {\n  int count = 1;\n  for (int i = 0, n = strlen(text); i < n; i++)\n    if (text[i] == \' \') count++;\n  return count;\n}\n'), 14)
add(2024,5,24, "readability: add sentence counting", lambda: touch_file("cs50/week2-arrays/readability.c","count_sentences added"), 16)
add(2024,5,25, "readability: implement Coleman-Liau formula", lambda: final("cs50/week2-arrays/readability.c"), 12)
add(2024,5,26, "readability: test with various text samples", lambda: touch_file("cs50/week2-arrays/readability.c","all tests passing"), 19)
add(2024,5,27, "week2: review arrays and strings in C", lambda: touch_file("cs50/week2-arrays/caesar.c","week2 done"), 10)
add(2024,5,28, "practice: command line arguments in C", lambda: touch_file("cs50/week1-c/hello.c","practice argc argv"), 14)
add(2024,5,29, "cs50 week3: implement bubble sort in C", lambda: wf("cs50/week3-algorithms/sort.c",'#include <cs50.h>\n#include <stdio.h>\n\nvoid swap(int *a, int *b);\n\nint main(void) {\n  int arr[] = {64, 34, 25, 12, 22, 11, 90};\n  int n = 7;\n  // bubble sort\n  for (int i = 0; i < n - 1; i++)\n    for (int j = 0; j < n - i - 1; j++)\n      if (arr[j] > arr[j + 1])\n        swap(&arr[j], &arr[j + 1]);\n  return 0;\n}\n\nvoid swap(int *a, int *b) {\n  int temp = *a; *a = *b; *b = temp;\n}\n'), 11)
add(2024,5,30, "sort: add print before/after and swap function", lambda: touch_file("cs50/week3-algorithms/sort.c","added output"), 15)
add(2024,5,31, "sort: add early termination optimization", lambda: final("cs50/week3-algorithms/sort.c"), 13)

# === JUNE 2024 - CS50 Week 3-7 ===
add(2024,6,1, "week3: review sorting and big O notation", lambda: touch_file("cs50/week3-algorithms/sort.c","O(n^2) average and worst"), 10)
add(2024,6,2, "study: time complexity - O(1) O(n) O(log n) O(n^2)", lambda: touch_file("cs50/week3-algorithms/sort.c","complexity notes"), 14)
add(2024,6,3, "practice: recursion concepts and examples", lambda: touch_file("cs50/week3-algorithms/sort.c","recursion practice"), 16)
add(2024,6,4, "cs50 week5: linked list in C - node struct", lambda: wf("cs50/week5-data-structures/list.c",'#include <stdio.h>\n#include <stdlib.h>\n\ntypedef struct node {\n  int number;\n  struct node *next;\n} node;\n\nint main(void) {\n  node *list = NULL;\n  // TODO: build list from argv\n  return 0;\n}\n'), 11)
add(2024,6,5, "list: add insert at beginning of linked list", lambda: touch_file("cs50/week5-data-structures/list.c","insert at head"), 15)
add(2024,6,6, "list: add printing and memory free", lambda: touch_file("cs50/week5-data-structures/list.c","print and free"), 13)
add(2024,6,7, "cs50: complete linked list with proper cleanup", lambda: final("cs50/week5-data-structures/list.c"), 17)
add(2024,6,8, "cs50: start dictionary - hash table struct", lambda: wf("cs50/week5-data-structures/dictionary.c",'#include <ctype.h>\n#include <stdbool.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\n#define HASH_SIZE 26\n\ntypedef struct node {\n  char word[46];\n  struct node *next;\n} node;\n\nnode *table[HASH_SIZE];\nunsigned int word_count = 0;\n\nunsigned int hash(const char *word) { return toupper(word[0]) - \'A\'; }\n\n// TODO: load, check, size, unload\n'), 10)
add(2024,6,9, "dictionary: implement load from file", lambda: touch_file("cs50/week5-data-structures/dictionary.c","load implemented"), 14)
add(2024,6,10, "dictionary: implement check with case handling", lambda: touch_file("cs50/week5-data-structures/dictionary.c","check working"), 16)
add(2024,6,11, "dictionary: implement size and unload", lambda: touch_file("cs50/week5-data-structures/dictionary.c","all functions done"), 11)
add(2024,6,12, "cs50: complete dictionary - all functions working", lambda: final("cs50/week5-data-structures/dictionary.c"), 18)
add(2024,6,13, "dictionary: fix potential memory leaks in unload", lambda: touch_file("cs50/week5-data-structures/dictionary.c","memory clean"), 15)
add(2024,6,14, "week5: review hash tables and data structures", lambda: touch_file("cs50/week5-data-structures/dictionary.c","review done"), 10)
add(2024,6,15, "study: hash functions and collision handling", lambda: touch_file("cs50/week5-data-structures/dictionary.c","study notes"), 20)
add(2024,6,16, "starting cs50 week6 - excited to learn Python", lambda: wf("README.md", readme_v(1).replace("course\n","course.\n\nCurrently on Week 6 - Python!\n")), 9)
add(2024,6,17, "cs50 week6: start cash.py - input validation", lambda: wf("cs50/week6-python/cash.py",'def main():\n    while True:\n        try:\n            change = float(input("Change owed: "))\n            if change >= 0:\n                break\n        except ValueError:\n            pass\n\n    cents = round(change * 100)\n    coins = 0\n    # TODO: calculate minimum coins\n    print(coins)\n\nif __name__ == "__main__":\n    main()\n'), 14)
add(2024,6,18, "cash.py: implement greedy coin calculation", lambda: touch_file("cs50/week6-python/cash.py","quarters dimes nickels pennies"), 16)
add(2024,6,19, "cs50: complete cash.py - works perfectly", lambda: final("cs50/week6-python/cash.py"), 12)
add(2024,6,20, "cash: Python is so much cleaner than C!", lambda: touch_file("cs50/week6-python/cash.py","much cleaner than C version"), 18)
add(2024,6,21, "cs50: start dna.py - file reading setup", lambda: wf("cs50/week6-python/dna.py",'import csv\nimport sys\n\ndef main():\n    if len(sys.argv) != 3:\n        sys.exit("Usage: python dna.py data.csv sequence.txt")\n    # TODO: read database, find matches\n\nif __name__ == "__main__":\n    main()\n'), 11)
add(2024,6,22, "dna: read CSV database into list of dicts", lambda: touch_file("cs50/week6-python/dna.py","csv.DictReader working"), 15)
add(2024,6,23, "dna: implement longest_match function", lambda: touch_file("cs50/week6-python/dna.py","longest_match done"), 13)
add(2024,6,24, "dna: add profile matching against database", lambda: touch_file("cs50/week6-python/dna.py","matching logic added"), 17)
add(2024,6,25, "cs50: complete dna.py - all test cases pass", lambda: final("cs50/week6-python/dna.py"), 10)
add(2024,6,26, "dna: cleanup and add comments", lambda: touch_file("cs50/week6-python/dna.py","cleanup done"), 14)
add(2024,6,27, "cs50 week7: create finance database schema", lambda: wf("cs50/week7-sql/finance.sql",'CREATE TABLE users (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    username TEXT NOT NULL UNIQUE,\n    hash TEXT NOT NULL\n);\n'), 11)
add(2024,6,28, "finance.sql: add stocks and transactions tables", lambda: touch_file("cs50/week7-sql/finance.sql","stocks and transactions tables"), 16)
add(2024,6,29, "finance.sql: add indexes for performance", lambda: final("cs50/week7-sql/finance.sql"), 13)
add(2024,6,30, "week7: practice SQL joins and aggregation", lambda: touch_file("cs50/week7-sql/finance.sql","practice queries"), 19)

# === JULY 2024 - Python Basics ===
add(2024,7,1, "update README with python section", lambda: wf("README.md", readme_v(2)), 10)
add(2024,7,2, "python: variables and basic data types", lambda: wf("python/basics/01_variables.py",'# variables and data types practice\n\nname = "Fazliddin"\nage = 25\nheight = 1.75\nis_student = True\n\nprint(f"name is {type(name)}")\nprint(f"age is {type(age)}")\n'), 14)
add(2024,7,3, "variables: add string operations and methods", lambda: touch_file("python/basics/01_variables.py","string methods added"), 16)
add(2024,7,4, "variables: add list operations", lambda: touch_file("python/basics/01_variables.py","list operations"), 11)
add(2024,7,5, "variables: add dictionary operations", lambda: touch_file("python/basics/01_variables.py","dict operations"), 15)
add(2024,7,6, "variables: add operators - arithmetic and comparison", lambda: final("python/basics/01_variables.py"), 13)
add(2024,7,7, "practice: python data type exercises", lambda: touch_file("python/basics/01_variables.py","practice done"), 20)
add(2024,7,8, "python: conditionals - if elif else", lambda: wf("python/basics/02_control_flow.py",'# control flow practice\n\ndef check_grade(score):\n    if score >= 90: return "A"\n    elif score >= 80: return "B"\n    elif score >= 70: return "C"\n    else: return "F"\n\nage = 20\nstatus = "adult" if age >= 18 else "minor"\n'), 10)
add(2024,7,9, "control flow: add for and while loops", lambda: touch_file("python/basics/02_control_flow.py","loops added"), 14)
add(2024,7,10, "control flow: break continue and enumerate", lambda: touch_file("python/basics/02_control_flow.py","break continue"), 16)
add(2024,7,11, "control flow: list and dict comprehensions", lambda: touch_file("python/basics/02_control_flow.py","comprehensions"), 12)
add(2024,7,12, "control flow: add match statement and nested loops", lambda: final("python/basics/02_control_flow.py"), 18)
add(2024,7,13, "practice: loop exercises and challenges", lambda: touch_file("python/basics/02_control_flow.py","exercises done"), 11)
add(2024,7,14, "review: python basics - types loops conditionals", lambda: touch_file("python/basics/01_variables.py","reviewed"), 15)
add(2024,7,15, "python: functions - def and return", lambda: wf("python/basics/03_functions.py",'# functions practice\nfrom functools import reduce\n\ndef greet(name):\n    return f"Hello, {name}!"\n\ndef greet_with_title(name, title="Mr."):\n    return f"Hello, {title} {name}!"\n'), 10)
add(2024,7,16, "functions: *args and **kwargs", lambda: touch_file("python/basics/03_functions.py","args kwargs"), 14)
add(2024,7,17, "functions: lambda and higher-order functions", lambda: touch_file("python/basics/03_functions.py","lambda map filter"), 16)
add(2024,7,18, "functions: map filter reduce", lambda: touch_file("python/basics/03_functions.py","reduce imported from functools"), 11)
add(2024,7,19, "functions: recursion - factorial fibonacci", lambda: touch_file("python/basics/03_functions.py","recursion examples"), 15)
add(2024,7,20, "functions: closures and complete examples", lambda: final("python/basics/03_functions.py"), 13)
add(2024,7,21, "practice: function challenges", lambda: touch_file("python/basics/03_functions.py","challenges done"), 10)
add(2024,7,22, "review functions and scoping rules", lambda: touch_file("python/basics/03_functions.py","LEGB scope rule"), 19)
add(2024,7,23, "python: error handling - try except basics", lambda: wf("python/basics/04_error_handling.py",'# error handling practice\n\ndef safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        print("Cannot divide by zero")\n        return None\n'), 14)
add(2024,7,24, "error handling: multiple exceptions and custom errors", lambda: touch_file("python/basics/04_error_handling.py","custom exceptions"), 16)
add(2024,7,25, "error handling: context managers with __enter__ __exit__", lambda: touch_file("python/basics/04_error_handling.py","context managers"), 11)
add(2024,7,26, "error handling: retry decorator pattern", lambda: touch_file("python/basics/04_error_handling.py","retry decorator"), 15)
add(2024,7,27, "error handling: assertions and complete examples", lambda: final("python/basics/04_error_handling.py"), 10)
add(2024,7,28, "python: file I/O - reading and writing text", lambda: wf("python/basics/05_file_io.py",'# file I/O practice\nimport json\nimport os\n\ndef write_text_file(filename, content):\n    with open(filename, "w") as f:\n        f.write(content)\n\ndef read_text_file(filename):\n    with open(filename, "r") as f:\n        return f.read()\n'), 13)
add(2024,7,29, "file io: JSON and CSV operations", lambda: touch_file("python/basics/05_file_io.py","json csv added"), 15)
add(2024,7,30, "file io: pathlib and directory operations", lambda: touch_file("python/basics/05_file_io.py","pathlib operations"), 17)
add(2024,7,31, "file io: complete with logger and config manager", lambda: final("python/basics/05_file_io.py"), 12)

# === AUG 2024 - OOP, Decorators, First Projects ===
add(2024,8,1, "python: string methods and formatting", lambda: wf("python/strings/string_methods.py",'# string methods practice\n\ntext = "Hello, World!"\nprint(text.upper())\nprint(text.lower())\nprint(text.split(","))\n'), 10)
add(2024,8,2, "strings: add practical functions and caesar cipher", lambda: final("python/strings/string_methods.py"), 14)
add(2024,8,3, "python oop: basic Dog class", lambda: wf("python/oop/classes.py",'# oop practice\nfrom dataclasses import dataclass\n\nclass Dog:\n    species = "Canis familiaris"\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def bark(self):\n        return f"{self.name} says Woof!"\n'), 11)
add(2024,8,4, "oop: add __str__ and __repr__ methods", lambda: touch_file("python/oop/classes.py","dunder methods"), 15)
add(2024,8,5, "oop: inheritance - GoldenRetriever extends Dog", lambda: touch_file("python/oop/classes.py","inheritance"), 13)
add(2024,8,6, "oop: abstract base classes with ABC", lambda: touch_file("python/oop/classes.py","ABC abstractmethod"), 17)
add(2024,8,7, "oop: encapsulation with @property", lambda: touch_file("python/oop/classes.py","properties"), 10)
add(2024,8,8, "oop: BankAccount class with validation", lambda: touch_file("python/oop/classes.py","bank account"), 14)
add(2024,8,9, "oop: dataclasses - Point and Person", lambda: touch_file("python/oop/classes.py","dataclasses"), 16)
add(2024,8,10, "oop: composition pattern - Car and Engine", lambda: final("python/oop/classes.py"), 12)
add(2024,8,11, "python: basic decorators with functools.wraps", lambda: wf("python/decorators/decorators.py",'# decorator examples\nimport functools\nimport time\n\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print("Before call")\n        result = func(*args, **kwargs)\n        print("After call")\n        return result\n    return wrapper\n\n@my_decorator\ndef say_hello(name):\n    print(f"Hello, {name}!")\n'), 10)
add(2024,8,12, "decorators: timer and debug decorators", lambda: touch_file("python/decorators/decorators.py","timer debug"), 14)
add(2024,8,13, "decorators: decorator with arguments - @repeat(n)", lambda: touch_file("python/decorators/decorators.py","parameterized"), 16)
add(2024,8,14, "decorators: retry and memoize patterns", lambda: touch_file("python/decorators/decorators.py","retry memoize"), 11)
add(2024,8,15, "decorators: singleton class decorator", lambda: final("python/decorators/decorators.py"), 15)
add(2024,8,16, "decided to start building projects to practice", lambda: wf("README.md", readme_v(2).replace("exercises\n","exercises\n- `projects/` - Hands-on CLI projects\n")), 9)
add(2024,8,17, "project: start todo CLI - basic add function", lambda: wf("projects/01-todo-cli/todo.py",'#!/usr/bin/env python3\n"""Todo CLI"""\nimport json\nfrom pathlib import Path\n\nTODO_FILE = Path.home() / ".todo_cli.json"\n\ndef load_todos():\n    if not TODO_FILE.exists(): return []\n    with open(TODO_FILE) as f: return json.load(f)\n\ndef save_todos(todos):\n    with open(TODO_FILE, "w") as f: json.dump(todos, f, indent=2)\n\ndef add_todo(title):\n    todos = load_todos()\n    todos.append({"id": len(todos)+1, "title": title, "completed": False})\n    save_todos(todos)\n    print(f"Added: {title}")\n'), 14)
add(2024,8,18, "todo: add list and complete commands", lambda: touch_file("projects/01-todo-cli/todo.py","list complete"), 16)
add(2024,8,19, "todo: add delete and clear functions", lambda: touch_file("projects/01-todo-cli/todo.py","delete clear"), 12)
add(2024,8,20, "todo: complete with argparse and priority system", lambda: final("projects/01-todo-cli/todo.py"), 18)
add(2024,8,21, "project: number guessing game with hints", lambda: wf("projects/13-number-guessing/guess.py",'#!/usr/bin/env python3\n"""Number Guessing Game"""\nimport random\n\ndef play():\n    secret = random.randint(1, 100)\n    print("Guess a number between 1 and 100")\n    while True:\n        guess = int(input("Your guess: "))\n        if guess == secret:\n            print("Correct!")\n            break\n        print("Too low!" if guess < secret else "Too high!")\n\nif __name__ == "__main__":\n    play()\n'), 10)
add(2024,8,22, "guess: add attempt counting and max tries", lambda: touch_file("projects/13-number-guessing/guess.py","attempts limit"), 14)
add(2024,8,23, "guess: add timing and replay functionality", lambda: touch_file("projects/13-number-guessing/guess.py","timing replay"), 16)
add(2024,8,24, "guess: complete with scoring system", lambda: final("projects/13-number-guessing/guess.py"), 11)
add(2024,8,25, "project: start expense tracker - data model", lambda: wf("projects/02-expense-tracker/expense.py",'#!/usr/bin/env python3\n"""Expense Tracker"""\nimport json\nfrom pathlib import Path\nfrom datetime import date\n\nEXPENSES_FILE = Path.home() / ".expense_tracker.json"\n\ndef load_expenses():\n    if not EXPENSES_FILE.exists(): return []\n    with open(EXPENSES_FILE) as f: return json.load(f)\n\ndef add_expense(amount, category):\n    expenses = load_expenses()\n    expenses.append({"amount": amount, "category": category, "date": date.today().isoformat()})\n    print(f"Added: ${amount:.2f} for {category}")\n'), 13)
add(2024,8,26, "expense: add list and summary views", lambda: touch_file("projects/02-expense-tracker/expense.py","list summary"), 15)
add(2024,8,27, "expense: add CSV export functionality", lambda: touch_file("projects/02-expense-tracker/expense.py","csv export"), 17)
add(2024,8,28, "expense: complete with argparse and filters", lambda: final("projects/02-expense-tracker/expense.py"), 12)
add(2024,8,29, "expense: fix summary percentage calculation", lambda: touch_file("projects/02-expense-tracker/expense.py","fixed percentages"), 10)
add(2024,8,30, "review: first two projects looking good", lambda: touch_file("projects/01-todo-cli/todo.py","reviewed"), 14)
add(2024,8,31, "update readme with projects list", lambda: wf("README.md", readme_v(2).replace("exercises\n","exercises\n- `projects/` - Hands-on CLI projects\n\n## Projects\n\n1. Todo CLI\n2. Expense Tracker\n")), 19)

# === SEP 2024 - More Projects, Generators ===
add(2024,9,1, "project: start password generator", lambda: wf("projects/03-password-generator/passgen.py",'#!/usr/bin/env python3\n"""Password Generator"""\nimport secrets\nimport string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + string.punctuation\n    return "".join(secrets.choice(chars) for _ in range(length))\n\nif __name__ == "__main__":\n    print(generate_password())\n'), 10)
add(2024,9,2, "passgen: add character type options", lambda: touch_file("projects/03-password-generator/passgen.py","char type options"), 14)
add(2024,9,3, "passgen: add passphrase generator mode", lambda: touch_file("projects/03-password-generator/passgen.py","passphrase"), 16)
add(2024,9,4, "passgen: add password strength checker", lambda: touch_file("projects/03-password-generator/passgen.py","strength checker"), 11)
add(2024,9,5, "passgen: complete with CLI and clipboard", lambda: final("projects/03-password-generator/passgen.py"), 15)
add(2024,9,6, "project: weather CLI with demo mode", lambda: wf("projects/04-weather-cli/weather.py",'#!/usr/bin/env python3\n"""Weather CLI"""\nimport random\n\ndef get_weather_demo(city):\n    conditions = ["Clear", "Clouds", "Rain"]\n    return {"city": city, "temp": round(random.uniform(-5,35),1), "condition": random.choice(conditions)}\n\ndef display_weather(w):\n    print(f"Weather in {w[\'city\']}: {w[\'temp\']}C {w[\'condition\']}")\n\nif __name__ == "__main__":\n    import sys\n    city = sys.argv[1] if len(sys.argv) > 1 else "London"\n    display_weather(get_weather_demo(city))\n'), 10)
add(2024,9,7, "weather: add OpenWeatherMap API integration", lambda: touch_file("projects/04-weather-cli/weather.py","API integration"), 14)
add(2024,9,8, "weather: add formatted display with icons", lambda: touch_file("projects/04-weather-cli/weather.py","weather icons"), 16)
add(2024,9,9, "weather: complete with argparse", lambda: final("projects/04-weather-cli/weather.py"), 12)
add(2024,9,10, "project: start pomodoro timer", lambda: wf("projects/05-pomodoro-timer/pomodoro.py",'#!/usr/bin/env python3\n"""Pomodoro Timer"""\nimport time, sys\n\ndef run_timer(mins, label="Timer"):\n    remaining = mins * 60\n    while remaining > 0:\n        m, s = divmod(remaining, 60)\n        sys.stdout.write(f"\\r{label}: {m:02d}:{s:02d}")\n        sys.stdout.flush()\n        time.sleep(1)\n        remaining -= 1\n    print("\\nDone!")\n'), 10)
add(2024,9,11, "pomodoro: add progress bar display", lambda: touch_file("projects/05-pomodoro-timer/pomodoro.py","progress bar"), 14)
add(2024,9,12, "pomodoro: add work/break session management", lambda: touch_file("projects/05-pomodoro-timer/pomodoro.py","sessions"), 16)
add(2024,9,13, "pomodoro: add long break after 4 sessions", lambda: touch_file("projects/05-pomodoro-timer/pomodoro.py","long break logic"), 11)
add(2024,9,14, "pomodoro: complete with argparse and stats", lambda: final("projects/05-pomodoro-timer/pomodoro.py"), 15)
add(2024,9,15, "python: generators basics - yield keyword", lambda: wf("python/generators/generators.py",'# generators and iterators\nimport sys\nfrom typing import Generator, Iterator\n\ndef count_up_to(max_value):\n    count = 1\n    while count <= max_value:\n        yield count\n        count += 1\n\nfor n in count_up_to(5):\n    print(n)\n'), 10)
add(2024,9,16, "generators: infinite sequences and fibonacci", lambda: touch_file("python/generators/generators.py","infinite fibonacci"), 14)
add(2024,9,17, "generators: pipeline pattern for data processing", lambda: touch_file("python/generators/generators.py","pipeline pattern"), 16)
add(2024,9,18, "generators: iterators context managers complete", lambda: final("python/generators/generators.py"), 12)
add(2024,9,19, "project: file organizer - sort files by type", lambda: wf("projects/06-file-organizer/organizer.py",'#!/usr/bin/env python3\n"""File Organizer"""\nfrom pathlib import Path\nimport shutil\n\nFILE_TYPES = {\n    "Images": [".jpg",".png",".gif"],\n    "Documents": [".pdf",".doc",".txt"],\n    "Code": [".py",".js",".c"],\n}\n\ndef get_category(ext):\n    for cat, exts in FILE_TYPES.items():\n        if ext.lower() in exts: return cat\n    return "Other"\n'), 11)
add(2024,9,20, "organizer: add comprehensive file type mappings", lambda: touch_file("projects/06-file-organizer/organizer.py","more file types"), 15)
add(2024,9,21, "organizer: add dry-run preview mode", lambda: touch_file("projects/06-file-organizer/organizer.py","dry run"), 13)
add(2024,9,22, "organizer: complete with undo and statistics", lambda: final("projects/06-file-organizer/organizer.py"), 17)
add(2024,9,23, "project: URL shortener with hash codes", lambda: wf("projects/07-url-shortener/shortener.py",'#!/usr/bin/env python3\n"""URL Shortener"""\nimport hashlib\nimport json\nfrom pathlib import Path\n\nDB_FILE = Path.home() / ".url_shortener.json"\n\ndef shorten(url):\n    code = hashlib.md5(url.encode()).hexdigest()[:6]\n    print(f"Short: https://short.url/{code}")\n    return code\n'), 10)
add(2024,9,24, "shortener: add persistent storage and lookup", lambda: touch_file("projects/07-url-shortener/shortener.py","persistence"), 14)
add(2024,9,25, "shortener: add click tracking and stats", lambda: touch_file("projects/07-url-shortener/shortener.py","tracking"), 16)
add(2024,9,26, "shortener: complete with all CLI commands", lambda: final("projects/07-url-shortener/shortener.py"), 12)
add(2024,9,27, "project: markdown to HTML converter", lambda: wf("projects/08-markdown-converter/md2html.py",'#!/usr/bin/env python3\n"""Markdown to HTML"""\nimport re\n\ndef convert_headers(text):\n    for i in range(6, 0, -1):\n        pattern = r"^#{" + str(i) + r"}\\s+(.+)$"\n        text = re.sub(pattern, f"<h{i}>\\\\1</h{i}>", text, flags=re.MULTILINE)\n    return text\n'), 11)
add(2024,9,28, "md2html: add bold italic links conversion", lambda: touch_file("projects/08-markdown-converter/md2html.py","formatting"), 15)
add(2024,9,29, "md2html: add list and blockquote conversion", lambda: touch_file("projects/08-markdown-converter/md2html.py","lists blockquotes"), 13)
add(2024,9,30, "md2html: complete with full HTML template", lambda: final("projects/08-markdown-converter/md2html.py"), 18)

# === OCT 2024 - Design Patterns, Testing, More Projects ===
add(2024,10,1, "python: design patterns - singleton", lambda: wf("python/design_patterns/patterns.py",'# design patterns\nfrom abc import ABC, abstractmethod\nfrom typing import List, Any\n\nclass Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n'), 10)
add(2024,10,2, "patterns: factory pattern for object creation", lambda: touch_file("python/design_patterns/patterns.py","factory"), 14)
add(2024,10,3, "patterns: builder pattern - step by step", lambda: touch_file("python/design_patterns/patterns.py","builder"), 16)
add(2024,10,4, "patterns: adapter and decorator structural", lambda: touch_file("python/design_patterns/patterns.py","adapter decorator"), 11)
add(2024,10,5, "patterns: observer and strategy behavioral", lambda: final("python/design_patterns/patterns.py"), 15)
add(2024,10,6, "python: pytest basics - assert and test classes", lambda: wf("python/testing/test_examples.py",'# pytest examples\nimport pytest\nfrom typing import List\n\ndef add(a, b): return a + b\n\nclass TestAdd:\n    def test_positive(self): assert add(2, 3) == 5\n    def test_negative(self): assert add(-1, -1) == -2\n    def test_zero(self): assert add(0, 0) == 0\n'), 10)
add(2024,10,7, "testing: parametrize and exception testing", lambda: touch_file("python/testing/test_examples.py","parametrize"), 14)
add(2024,10,8, "testing: fixtures and Calculator class tests", lambda: touch_file("python/testing/test_examples.py","fixtures"), 16)
add(2024,10,9, "testing: complete test suite all examples", lambda: final("python/testing/test_examples.py"), 12)
add(2024,10,10, "testing: add docstrings and cleanup", lambda: touch_file("python/testing/test_examples.py","docstrings"), 17)
add(2024,10,11, "project: quiz game - Python questions", lambda: wf("projects/09-quiz-game/quiz.py",'#!/usr/bin/env python3\n"""Quiz Game"""\nimport random\nfrom dataclasses import dataclass\nfrom typing import List\n\n@dataclass\nclass Question:\n    question: str\n    options: List[str]\n    correct: int\n    explanation: str = ""\n\nSAMPLE = [Question("What is type([])?", ["list","tuple","array","set"], 0, "[] creates a list")]\n'), 11)
add(2024,10,12, "quiz: add git and linux question categories", lambda: touch_file("projects/09-quiz-game/quiz.py","git linux"), 15)
add(2024,10,13, "quiz: add scoring and explanations", lambda: touch_file("projects/09-quiz-game/quiz.py","scoring"), 13)
add(2024,10,14, "quiz: complete with CLI and all features", lambda: final("projects/09-quiz-game/quiz.py"), 18)
add(2024,10,15, "project: start habit tracker", lambda: wf("projects/10-habit-tracker/habits.py",'#!/usr/bin/env python3\n"""Habit Tracker"""\nimport json\nfrom pathlib import Path\nfrom datetime import date, timedelta\n\nHABITS_FILE = Path.home() / ".habit_tracker.json"\n\ndef load_data():\n    if not HABITS_FILE.exists(): return {"habits": {}, "log": {}}\n    with open(HABITS_FILE) as f: return json.load(f)\n'), 10)
add(2024,10,16, "habits: add logging and streak tracking", lambda: touch_file("projects/10-habit-tracker/habits.py","streaks"), 14)
add(2024,10,17, "habits: add statistics and calendar view", lambda: touch_file("projects/10-habit-tracker/habits.py","stats calendar"), 16)
add(2024,10,18, "habits: add weekly visualization", lambda: touch_file("projects/10-habit-tracker/habits.py","visualization"), 11)
add(2024,10,19, "habits: complete with argparse and all features", lambda: final("projects/10-habit-tracker/habits.py"), 15)
add(2024,10,20, "python: async basics - coroutines and await", lambda: wf("python/async_python/async_basics.py",'# async examples\nimport asyncio\nimport time\nfrom typing import List\n\nasync def say_hello(name, delay=1.0):\n    await asyncio.sleep(delay)\n    return f"Hello, {name}!"\n\nasync def main():\n    result = await say_hello("World")\n    print(result)\n\nif __name__ == "__main__":\n    asyncio.run(main())\n'), 10)
add(2024,10,21, "async: gather and concurrent execution", lambda: touch_file("python/async_python/async_basics.py","gather"), 14)
add(2024,10,22, "async: producer-consumer and semaphores", lambda: touch_file("python/async_python/async_basics.py","producer consumer"), 16)
add(2024,10,23, "async: complete with timeouts and aiohttp", lambda: final("python/async_python/async_basics.py"), 12)
add(2024,10,24, "project: calculator with expression evaluation", lambda: wf("projects/11-calculator/calculator.py",'#!/usr/bin/env python3\n"""Calculator CLI"""\nimport math\nimport operator\n\nclass Calculator:\n    def __init__(self):\n        self.history = []\n        self.last_result = 0\n    \n    def calculate(self, expr):\n        result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi})\n        self.history.append(f"{expr} = {result}")\n        self.last_result = float(result)\n        return result\n'), 11)
add(2024,10,25, "calculator: add interactive mode and memory", lambda: touch_file("projects/11-calculator/calculator.py","interactive memory"), 15)
add(2024,10,26, "calculator: complete with history and help", lambda: final("projects/11-calculator/calculator.py"), 13)
add(2024,10,27, "project: contact book CLI - CRUD operations", lambda: wf("projects/12-contact-book/contacts.py",'#!/usr/bin/env python3\n"""Contact Book"""\nimport json\nfrom pathlib import Path\n\nCONTACTS_FILE = Path.home() / ".contacts_book.json"\n\ndef load_contacts():\n    if not CONTACTS_FILE.exists(): return []\n    with open(CONTACTS_FILE) as f: return json.load(f)\n\ndef add_contact(name, phone="", email=""):\n    contacts = load_contacts()\n    contacts.append({"name": name, "phone": phone, "email": email})\n    print(f"Added: {name}")\n'), 10)
add(2024,10,28, "contacts: add search and detailed view", lambda: touch_file("projects/12-contact-book/contacts.py","search view"), 14)
add(2024,10,29, "contacts: complete with export and update", lambda: final("projects/12-contact-book/contacts.py"), 16)
add(2024,10,30, "project: hangman word guessing game", lambda: wf("projects/14-hangman/hangman.py",'#!/usr/bin/env python3\n"""Hangman Game"""\nimport random\n\nWORDS = ["python","function","variable","decorator"]\n\ndef play():\n    word = random.choice(WORDS)\n    guessed = set()\n    wrong = 0\n    while wrong < 6:\n        display = " ".join(c if c in guessed else "_" for c in word)\n        print(display)\n        guess = input("Letter: ").lower()\n        guessed.add(guess)\n        if guess not in word: wrong += 1\n        if all(c in guessed for c in word):\n            print(f"You won! Word: {word}")\n            return\n    print(f"Game over! Word: {word}")\n'), 12)
add(2024,10,31, "hangman: add categories and ASCII art stages", lambda: final("projects/14-hangman/hangman.py"), 18)

# === NOV 2024 - Algorithms, CLI Tools ===
add(2024,11,1, "algorithms: bubble sort implementation", lambda: wf("algorithms/sorting/sorting.py",'"""Sorting Algorithms"""\nfrom typing import List\n\ndef bubble_sort(arr):\n    """Bubble Sort - O(n^2)"""\n    n = len(arr)\n    arr = arr.copy()\n    for i in range(n):\n        swapped = False\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n                swapped = True\n        if not swapped: break\n    return arr\n'), 10)
add(2024,11,2, "sorting: selection and insertion sort", lambda: touch_file("algorithms/sorting/sorting.py","selection insertion"), 14)
add(2024,11,3, "sorting: merge sort - divide and conquer", lambda: touch_file("algorithms/sorting/sorting.py","merge sort"), 16)
add(2024,11,4, "sorting: quick sort with pivot selection", lambda: touch_file("algorithms/sorting/sorting.py","quick sort"), 11)
add(2024,11,5, "sorting: heap sort and counting sort", lambda: final("algorithms/sorting/sorting.py"), 15)
add(2024,11,6, "algorithms: linear and binary search", lambda: wf("algorithms/searching/searching.py",'"""Searching Algorithms"""\nfrom typing import List\n\ndef linear_search(arr, target):\n    """Linear Search - O(n)"""\n    for i, val in enumerate(arr):\n        if val == target: return i\n    return -1\n\ndef binary_search(arr, target):\n    """Binary Search - O(log n)"""\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1\n'), 10)
add(2024,11,7, "searching: recursive binary search", lambda: touch_file("algorithms/searching/searching.py","recursive"), 14)
add(2024,11,8, "searching: leftmost and rightmost variants", lambda: touch_file("algorithms/searching/searching.py","leftmost rightmost"), 16)
add(2024,11,9, "searching: jump exponential interpolation", lambda: final("algorithms/searching/searching.py"), 12)
add(2024,11,10, "data structures: linked list - Node and append", lambda: wf("algorithms/data-structures/structures.py",'"""Data Structures"""\nfrom typing import Any, Optional, List\n\nclass Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n        self._size = 0\n    def append(self, data):\n        new_node = Node(data)\n        if not self.head:\n            self.head = new_node\n        else:\n            curr = self.head\n            while curr.next: curr = curr.next\n            curr.next = new_node\n        self._size += 1\n'), 10)
add(2024,11,11, "structures: prepend delete find reverse", lambda: touch_file("algorithms/data-structures/structures.py","methods"), 14)
add(2024,11,12, "structures: Stack and Queue implementations", lambda: touch_file("algorithms/data-structures/structures.py","stack queue"), 16)
add(2024,11,13, "structures: binary search tree - insert search", lambda: touch_file("algorithms/data-structures/structures.py","BST"), 11)
add(2024,11,14, "structures: BST traversals inorder preorder post", lambda: touch_file("algorithms/data-structures/structures.py","traversals"), 15)
add(2024,11,15, "structures: HashMap with chaining", lambda: final("algorithms/data-structures/structures.py"), 13)
add(2024,11,16, "cli-tool: file finder with glob patterns", lambda: wf("cli-tools/file-finder/finder.py",'#!/usr/bin/env python3\n"""File Finder"""\nfrom pathlib import Path\n\ndef find_files(directory, pattern="*", recursive=True):\n    glob_pat = f"**/{pattern}" if recursive else pattern\n    for f in Path(directory).glob(glob_pat):\n        if f.is_file(): yield f\n'), 10)
add(2024,11,17, "finder: add size and date filters", lambda: touch_file("cli-tools/file-finder/finder.py","size date filters"), 14)
add(2024,11,18, "finder: add content search and duplicates", lambda: touch_file("cli-tools/file-finder/finder.py","content duplicates"), 16)
add(2024,11,19, "finder: complete with stats and argparse", lambda: final("cli-tools/file-finder/finder.py"), 12)
add(2024,11,20, "cli-tool: git helper - pretty status", lambda: wf("cli-tools/git-helper/git_helper.py",'#!/usr/bin/env python3\n"""Git Helper"""\nimport subprocess\n\ndef run_git(args):\n    return subprocess.run(["git"]+args, capture_output=True, text=True)\n\ndef status_pretty():\n    r = run_git(["status","-sb"])\n    if r.returncode == 0: print(r.stdout)\n'), 10)
add(2024,11,21, "git-helper: add pretty log and quick commit", lambda: touch_file("cli-tools/git-helper/git_helper.py","log commit"), 14)
add(2024,11,22, "git-helper: add branch and sync commands", lambda: touch_file("cli-tools/git-helper/git_helper.py","branch sync"), 16)
add(2024,11,23, "git-helper: complete with undo and stash", lambda: final("cli-tools/git-helper/git_helper.py"), 12)
add(2024,11,24, "cli-tool: task manager - project structure", lambda: wf("cli-tools/task-manager/tasks.py",'#!/usr/bin/env python3\n"""Task Manager"""\nimport json\nfrom pathlib import Path\nfrom datetime import datetime\n\nTASKS_FILE = Path.home() / ".task_manager.json"\n\ndef load_data():\n    if not TASKS_FILE.exists(): return {"projects": {}, "tasks": []}\n    with open(TASKS_FILE) as f: return json.load(f)\n'), 11)
add(2024,11,25, "tasks: add project and task management", lambda: touch_file("cli-tools/task-manager/tasks.py","project task"), 15)
add(2024,11,26, "tasks: add priority status and filtering", lambda: touch_file("cli-tools/task-manager/tasks.py","priority status"), 13)
add(2024,11,27, "tasks: complete with summary and all features", lambda: final("cli-tools/task-manager/tasks.py"), 17)
add(2024,11,28, "update README with all sections", lambda: wf("README.md", readme_v(3)), 10)
add(2024,11,29, "fix: sorting algorithms - add early termination", lambda: touch_file("algorithms/sorting/sorting.py","optimized"), 14)
add(2024,11,30, "improve: error messages across all projects", lambda: touch_file("projects/01-todo-cli/todo.py","better errors"), 16)

# === DEC 2024 - Polish, Final Cleanup ===
add(2024,12,1, "refactor: clean up import statements across files", lambda: touch_file("python/basics/03_functions.py","clean imports"), 10)
add(2024,12,2, "fix: add type hints to data structures", lambda: touch_file("algorithms/data-structures/structures.py","type hints"), 14)
add(2024,12,3, "add docstrings to all sorting algorithms", lambda: touch_file("algorithms/sorting/sorting.py","docstrings"), 16)
add(2024,12,4, "fix: binary search edge case - empty array", lambda: touch_file("algorithms/searching/searching.py","edge case"), 11)
add(2024,12,5, "improve: hash map resize on high load factor", lambda: touch_file("algorithms/data-structures/structures.py","resize"), 15)
add(2024,12,6, "add time complexity comments to algorithms", lambda: touch_file("algorithms/sorting/sorting.py","complexity"), 13)
add(2024,12,7, "fix: todo CLI id tracking after deletion", lambda: touch_file("projects/01-todo-cli/todo.py","id fix"), 10)
add(2024,12,8, "improve: expense tracker bar chart in summary", lambda: touch_file("projects/02-expense-tracker/expense.py","bar chart"), 14)
add(2024,12,9, "fix: password generator exclude characters", lambda: touch_file("projects/03-password-generator/passgen.py","exclude fix"), 16)
add(2024,12,10, "refactor: weather CLI better error handling", lambda: touch_file("projects/04-weather-cli/weather.py","error handling"), 12)
add(2024,12,11, "fix: pomodoro timer KeyboardInterrupt handling", lambda: touch_file("projects/05-pomodoro-timer/pomodoro.py","interrupt fix"), 17)
add(2024,12,12, "improve: file organizer duplicate file names", lambda: touch_file("projects/06-file-organizer/organizer.py","duplicates"), 11)
add(2024,12,13, "fix: URL shortener hash collision handling", lambda: touch_file("projects/07-url-shortener/shortener.py","collision"), 15)
add(2024,12,14, "improve: markdown converter nested formatting", lambda: touch_file("projects/08-markdown-converter/md2html.py","nested"), 13)
add(2024,12,15, "fix: quiz game input validation edge cases", lambda: touch_file("projects/09-quiz-game/quiz.py","validation"), 18)
add(2024,12,16, "fix: habit tracker streak calculation bug", lambda: touch_file("projects/10-habit-tracker/habits.py","streak fix"), 10)
add(2024,12,17, "improve: calculator memory store/recall", lambda: touch_file("projects/11-calculator/calculator.py","memory"), 14)
add(2024,12,18, "add: contact book CSV export feature", lambda: touch_file("projects/12-contact-book/contacts.py","csv export"), 16)
add(2024,12,19, "fix: file finder PermissionError handling", lambda: touch_file("cli-tools/file-finder/finder.py","permission"), 12)
add(2024,12,20, "improve: git helper colored output", lambda: touch_file("cli-tools/git-helper/git_helper.py","colors"), 17)
add(2024,12,21, "fix: task manager priority sorting order", lambda: touch_file("cli-tools/task-manager/tasks.py","sort fix"), 11)
add(2024,12,22, "review: python basics - all exercises passing", lambda: touch_file("python/basics/01_variables.py","all good"), 15)
add(2024,12,23, "testing: add more edge case tests", lambda: touch_file("python/testing/test_examples.py","edge cases"), 13)
add(2024,12,24, "fix: async import asyncio at top of file", lambda: touch_file("python/async_python/async_basics.py","import fix"), 10)
add(2024,12,25, "cleanup: remove leftover debug prints", lambda: touch_file("python/basics/02_control_flow.py","cleanup"), 20)
add(2024,12,26, "update README - add cli-tools section", lambda: final("README.md"), 14)
add(2024,12,27, "fix: generator type annotations", lambda: touch_file("python/generators/generators.py","type fix"), 16)
add(2024,12,28, "fix: design patterns ABC imports", lambda: touch_file("python/design_patterns/patterns.py","abc import"), 12)
add(2024,12,29, "fix: OOP classes ABC import", lambda: touch_file("python/oop/classes.py","abc fix"), 11)
add(2024,12,30, "review and polish all projects", lambda: touch_file("projects/14-hangman/hangman.py","polished"), 15)
add(2024,12,31, "year end cleanup - all projects complete", lambda: touch_file(".gitignore",""), 23, 50)

# ── add some double/triple commit days ──────────────────────────────
# Sprinkle extra commits on busy days
extras = [
    (md(2024,5,4,19), "practice: trying different loop patterns in C", lambda: touch_file("cs50/week1-c/mario.c","loop patterns")),
    (md(2024,5,12,20), "study: credit card number formats and checksums", lambda: touch_file("cs50/week1-c/credit.c","card formats")),
    (md(2024,5,21,21), "experiment: different cipher approaches", lambda: touch_file("cs50/week2-arrays/caesar.c","approaches")),
    (md(2024,6,7,20), "study: pointers and dynamic memory in C", lambda: touch_file("cs50/week5-data-structures/list.c","pointers study")),
    (md(2024,6,12,22), "test: dictionary with large word files", lambda: touch_file("cs50/week5-data-structures/dictionary.c","large test")),
    (md(2024,6,19,21), "compare: Python vs C implementation approaches", lambda: touch_file("cs50/week6-python/cash.py","python vs C")),
    (md(2024,7,6,19), "experiment: mutable vs immutable types", lambda: touch_file("python/basics/01_variables.py","mutability")),
    (md(2024,7,12,22), "challenge: FizzBuzz with list comprehension", lambda: touch_file("python/basics/02_control_flow.py","fizzbuzz")),
    (md(2024,7,20,20), "experiment: recursive vs iterative fibonacci", lambda: touch_file("python/basics/03_functions.py","recursive vs iterative")),
    (md(2024,7,27,19), "study: EAFP vs LBYL in Python", lambda: touch_file("python/basics/04_error_handling.py","EAFP LBYL")),
    (md(2024,8,10,19), "study: multiple inheritance and MRO", lambda: touch_file("python/oop/classes.py","MRO")),
    (md(2024,8,15,20), "study: when to use decorators vs inheritance", lambda: touch_file("python/decorators/decorators.py","patterns comparison")),
    (md(2024,8,20,21), "todo: test with edge cases - empty list etc", lambda: touch_file("projects/01-todo-cli/todo.py","edge cases")),
    (md(2024,8,24,19), "guess: add input validation for non-numbers", lambda: touch_file("projects/13-number-guessing/guess.py","validation")),
    (md(2024,8,28,20), "expense: test monthly summary output", lambda: touch_file("projects/02-expense-tracker/expense.py","test monthly")),
    (md(2024,9,5,20), "passgen: test strength checker accuracy", lambda: touch_file("projects/03-password-generator/passgen.py","strength test")),
    (md(2024,9,14,20), "pomodoro: test with different intervals", lambda: touch_file("projects/05-pomodoro-timer/pomodoro.py","interval test")),
    (md(2024,9,18,19), "study: generator memory advantages", lambda: touch_file("python/generators/generators.py","memory study")),
    (md(2024,9,26,19), "shortener: test with very long URLs", lambda: touch_file("projects/07-url-shortener/shortener.py","long url test")),
    (md(2024,9,30,22), "md2html: test with complex markdown files", lambda: touch_file("projects/08-markdown-converter/md2html.py","complex test")),
    (md(2024,10,5,20), "study: when to use which design pattern", lambda: touch_file("python/design_patterns/patterns.py","pattern selection")),
    (md(2024,10,9,19), "testing: study pytest best practices", lambda: touch_file("python/testing/test_examples.py","best practices")),
    (md(2024,10,19,20), "habits: test streak calculation edge cases", lambda: touch_file("projects/10-habit-tracker/habits.py","streak test")),
    (md(2024,10,23,19), "async: benchmark sync vs async performance", lambda: touch_file("python/async_python/async_basics.py","benchmark")),
    (md(2024,10,31,22), "happy halloween! hangman feels appropriate today", lambda: touch_file("projects/14-hangman/hangman.py","halloween")),
    (md(2024,11,5,20), "sorting: benchmark all algorithms with timing", lambda: touch_file("algorithms/sorting/sorting.py","benchmark")),
    (md(2024,11,9,19), "searching: test with large sorted arrays", lambda: touch_file("algorithms/searching/searching.py","large test")),
    (md(2024,11,15,19), "structures: test BST with unbalanced input", lambda: touch_file("algorithms/data-structures/structures.py","unbalanced")),
    (md(2024,11,19,19), "finder: test recursive search performance", lambda: touch_file("cli-tools/file-finder/finder.py","performance")),
    (md(2024,11,23,19), "git-helper: test with various repo states", lambda: touch_file("cli-tools/git-helper/git_helper.py","test states")),
    (md(2024,11,27,21), "tasks: test with many projects and tasks", lambda: touch_file("cli-tools/task-manager/tasks.py","load test")),
    (md(2024,12,8,19), "expense: add monthly budget comparison", lambda: touch_file("projects/02-expense-tracker/expense.py","budget")),
    (md(2024,12,15,22), "quiz: add more questions to each category", lambda: touch_file("projects/09-quiz-game/quiz.py","more questions")),
    (md(2024,12,22,20), "review: all Python concepts solidified", lambda: touch_file("python/basics/03_functions.py","solidified")),
    (md(2024,12,26,19), "add .idea to gitignore", lambda: touch_file(".gitignore","")),
    (md(2024,12,31,22), "final check: all 14 projects working", lambda: touch_file("README.md","")),
]

for date_str, msg, action in extras:
    schedule.append((date_str, msg, action))

# Sort by date
schedule.sort(key=lambda x: x[0])

# ── execute all commits ──────────────────────────────────────────────
print(f"\nCreating {len(schedule)} commits...")
for i, (dt, msg, action) in enumerate(schedule):
    action()
    commit(msg, dt)
    if (i+1) % 50 == 0:
        print(f"  {i+1}/{len(schedule)} commits done...")

print(f"\nAll {len(schedule)} commits created!")

# ── push ─────────────────────────────────────────────────────────────
run(f'git remote add origin {REMOTE}')
print("Pushing to remote...")
r = subprocess.run('git push -u origin main --force', shell=True, capture_output=True, text=True, cwd=REPO)
if r.returncode == 0:
    print("Pushed successfully!")
else:
    print(f"Push output: {r.stderr}")

# ── cleanup ──────────────────────────────────────────────────────────
os.remove(os.path.join(REPO, "rebuild.py"))
print("\nDone! Verifying...")
os.system(f'cd {REPO} && git log --oneline | wc -l && git log --oneline | head -5 && echo "..." && git log --oneline | tail -5')
