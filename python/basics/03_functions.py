# functions practice
from functools import reduce


# Basic function
def greet(name):
    """Simple greeting function."""
    return f"Hello, {name}!"


# Default parameters
def greet_with_title(name, title="Mr."):
    """Greeting with optional title."""
    return f"Hello, {title} {name}!"


# *args - Variable positional arguments
def calculate_sum(*args):
    """Sum any number of arguments."""
    return sum(args)


# **kwargs - Variable keyword arguments
def build_profile(**kwargs):
    """Build a user profile from keyword arguments."""
    return kwargs


# Combined parameters
def complex_function(required, *args, default="value", **kwargs):
    """Demonstrates all parameter types."""
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Default: {default}")
    print(f"Kwargs: {kwargs}")


# Lambda functions
square = lambda x: x ** 2
add = lambda x, y: x + y

# Map, Filter, Reduce
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
total = reduce(lambda x, y: x + y, numbers)

print(f"Squared: {squared}")
print(f"Evens: {evens}")
print(f"Total: {total}")


# Recursion
def factorial(n):
    """Calculate factorial recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    """Calculate nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Closure
def multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(number):
        return number * factor
    return multiply


double = multiplier(2)
triple = multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15


# Higher-order function
def apply_operation(func, x, y):
    """Apply a function to two arguments."""
    return func(x, y)


result = apply_operation(lambda a, b: a + b, 3, 4)
print(result)  # 7


if __name__ == "__main__":
    print(greet("World"))
    print(greet_with_title("Smith"))
    print(greet_with_title("Jane", "Dr."))
    print(calculate_sum(1, 2, 3, 4, 5))
    print(build_profile(name="John", age=30, city="NYC"))
    print(f"5! = {factorial(5)}")
    print(f"Fib(10) = {fibonacci(10)}")
