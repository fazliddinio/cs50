# error handling practice

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None

# custom exceptions

# context managers

# retry decorator
