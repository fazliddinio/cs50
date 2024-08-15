# decorator examples
import functools
import time
from typing import Callable, Any


# Basic Decorator
def my_decorator(func):
    """Simple decorator that wraps a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper


@my_decorator
def say_hello(name):
    """Say hello to someone."""
    print(f"Hello, {name}!")


# Timer Decorator
def timer(func):
    """Measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


@timer
def slow_function():
    """A slow function for testing."""
    time.sleep(0.5)
    return "Done"


# Decorator with Arguments
def repeat(times: int):
    """Repeat a function multiple times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")


# Debug Decorator
def debug(func):
    """Print function signature and return value."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result
    return wrapper


@debug
def add(a, b):
    return a + b


# Retry Decorator
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    print(f"Attempt {attempts} failed, retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator


# Cache Decorator (memoization)
def memoize(func):
    """Cache function results."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@memoize
def fibonacci(n):
    """Calculate fibonacci with memoization."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Class Decorator
def singleton(cls):
    """Make a class a Singleton."""
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DatabaseConnection:
    def __init__(self):
        print("Creating database connection")
        self.connected = True


# Method Decorators
class MyClass:
    @staticmethod
    def static_method():
        """Doesn't access class or instance."""
        return "I'm a static method"
    
    @classmethod
    def class_method(cls):
        """Accesses the class."""
        return f"I'm a method of {cls.__name__}"
    
    @property
    def computed_property(self):
        """Acts like an attribute but is computed."""
        return "I'm a computed property"


if __name__ == "__main__":
    say_hello("World")
    print()
    
    slow_function()
    print()
    
    greet("Alice")
    print()
    
    add(2, 3)
    print()
    
    print(f"Fibonacci(30) = {fibonacci(30)}")
    print()
    
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")
