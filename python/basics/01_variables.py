# variables and data types practice

# Variables and Data Types
name = "Fazliddin"
age = 25
height = 1.75
is_student = True
skills = ["Python", "JavaScript", "SQL"]
info = {"role": "Developer", "location": "Remote"}

# Type checking
print(f"name is {type(name)}")
print(f"age is {type(age)}")
print(f"height is {type(height)}")
print(f"is_student is {type(is_student)}")

# String operations
message = "Hello, World!"
print(message.upper())
print(message.lower())
print(message.split(","))
print(len(message))

# String formatting
greeting = f"My name is {name} and I am {age} years old"
print(greeting)

# List operations
skills.append("Docker")
skills.extend(["Git", "Linux"])
skills.remove("JavaScript")
print(skills)
print(skills[0])  # First element
print(skills[-1])  # Last element
print(skills[1:3])  # Slicing

# Dictionary operations
info["experience"] = 3
info.update({"level": "Mid"})
print(info.keys())
print(info.values())
print(info.items())

# Arithmetic operators
x, y = 10, 3
print(f"Addition: {x + y}")
print(f"Subtraction: {x - y}")
print(f"Multiplication: {x * y}")
print(f"Division: {x / y}")
print(f"Floor Division: {x // y}")
print(f"Modulus: {x % y}")
print(f"Exponentiation: {x ** y}")

# Comparison operators
print(f"x > y: {x > y}")
print(f"x == y: {x == y}")
print(f"x != y: {x != y}")

# Logical operators
a, b = True, False
print(f"a and b: {a and b}")
print(f"a or b: {a or b}")
print(f"not a: {not a}")
