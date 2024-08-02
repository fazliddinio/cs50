# string methods and operations practice


# ============ String Methods ============

text = "  Hello, World! Welcome to Python.  "

# Stripping whitespace
print(text.strip())
print(text.lstrip())
print(text.rstrip())

# Case methods
msg = "hello world"
print(msg.upper())          # HELLO WORLD
print(msg.capitalize())     # Hello world
print(msg.title())          # Hello World
print("HELLO".lower())      # hello
print("hello".swapcase())   # HELLO

# Finding and replacing
sentence = "the quick brown fox jumps over the lazy dog"
print(sentence.find("fox"))       # 16
print(sentence.index("fox"))      # 16
print(sentence.count("the"))      # 2
print(sentence.replace("fox", "cat"))

# Checking string content
print("hello123".isalnum())    # True
print("hello".isalpha())       # True
print("12345".isdigit())       # True
print("hello".islower())       # True
print(" \t\n".isspace())       # True

# Splitting and joining
csv_line = "apple,banana,cherry,date"
fruits = csv_line.split(",")
print(fruits)

words = "Hello World Python".split()
joined = " - ".join(words)
print(joined)

# String formatting methods
name = "Fazliddin"
age = 25

# f-string (Python 3.6+)
print(f"Name: {name}, Age: {age}")

# format method
print("Name: {}, Age: {}".format(name, age))
print("Name: {n}, Age: {a}".format(n=name, a=age))

# %-formatting (old style)
print("Name: %s, Age: %d" % (name, age))

# Format specifiers
pi = 3.14159265
print(f"Pi: {pi:.2f}")           # 3.14
print(f"Pi: {pi:10.4f}")         # padding
print(f"Number: {42:05d}")       # 00042
print(f"Percent: {0.756:.1%}")   # 75.6%
print(f"Binary: {255:08b}")      # 11111111
print(f"Hex: {255:#06x}")        # 0x00ff


# ============ Practical Functions ============

def is_palindrome(s):
    """Check if a string is a palindrome."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(s):
    """Count vowels in a string."""
    return sum(1 for c in s.lower() if c in 'aeiou')


def reverse_words(s):
    """Reverse the order of words in a string."""
    return ' '.join(s.split()[::-1])


def caesar_cipher(text, shift):
    """Simple Caesar cipher encryption."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)


def truncate(text, max_length=50, suffix="..."):
    """Truncate a string to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def slugify(text):
    """Convert text to URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


if __name__ == "__main__":
    print("\n=== Palindrome Check ===")
    test_strings = ["racecar", "hello", "A man a plan a canal Panama"]
    for s in test_strings:
        print(f"  '{s}' -> {is_palindrome(s)}")
    
    print("\n=== Count Vowels ===")
    print(f"  'Hello World' has {count_vowels('Hello World')} vowels")
    
    print("\n=== Reverse Words ===")
    print(f"  '{reverse_words('Hello World Python')}'")
    
    print("\n=== Caesar Cipher ===")
    original = "Hello World"
    encrypted = caesar_cipher(original, 3)
    decrypted = caesar_cipher(encrypted, -3)
    print(f"  Original:  {original}")
    print(f"  Encrypted: {encrypted}")
    print(f"  Decrypted: {decrypted}")
    
    print("\n=== Slugify ===")
    titles = ["Hello World!", "My Blog Post #1", "Python is Great!!!"]
    for title in titles:
        print(f"  '{title}' -> '{slugify(title)}'")
