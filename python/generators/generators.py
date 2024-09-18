# generators and iterators
import sys
from typing import Generator, Iterator


# Basic Generator
def count_up_to(max_value: int) -> Generator[int, None, None]:
    """Generate numbers from 1 to max_value."""
    count = 1
    while count <= max_value:
        yield count
        count += 1


# Generator Expression vs List Comprehension
def memory_comparison():
    """Compare memory usage of generator vs list."""
    # List comprehension - loads all into memory
    list_comp = [x * 2 for x in range(1000000)]
    print(f"List size: {sys.getsizeof(list_comp)} bytes")
    
    # Generator expression - lazy evaluation
    gen_exp = (x * 2 for x in range(1000000))
    print(f"Generator size: {sys.getsizeof(gen_exp)} bytes")


# Infinite Generator
def infinite_sequence() -> Generator[int, None, None]:
    """Generate infinite sequence of numbers."""
    num = 0
    while True:
        yield num
        num += 1


# Fibonacci Generator
def fibonacci_gen() -> Generator[int, None, None]:
    """Generate Fibonacci sequence infinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Generator with Send
def accumulator() -> Generator[int, int, None]:
    """Accumulator that accepts values via send()."""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value


# File Reader Generator
def read_large_file(file_path: str) -> Generator[str, None, None]:
    """Read large file line by line."""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


# Pipeline with Generators
def numbers(n: int) -> Generator[int, None, None]:
    """Generate numbers 0 to n."""
    for i in range(n):
        yield i


def squared(nums: Iterator[int]) -> Generator[int, None, None]:
    """Square each number."""
    for n in nums:
        yield n ** 2


def filtered(nums: Iterator[int], threshold: int) -> Generator[int, None, None]:
    """Filter numbers above threshold."""
    for n in nums:
        if n > threshold:
            yield n


# Custom Iterator Class
class Countdown:
    """Iterator that counts down from n to 0."""
    
    def __init__(self, start: int):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start < 0:
            raise StopIteration
        current = self.start
        self.start -= 1
        return current


# Context Manager with Generator
from contextlib import contextmanager

@contextmanager
def timer_context(name: str):
    """Context manager using generator."""
    import time
    start = time.perf_counter()
    print(f"Starting {name}...")
    yield
    end = time.perf_counter()
    print(f"{name} took {end - start:.4f} seconds")


if __name__ == "__main__":
    # Basic generator
    print("Count up to 5:")
    for num in count_up_to(5):
        print(num)
    print()
    
    # Memory comparison
    memory_comparison()
    print()
    
    # Fibonacci
    print("First 10 Fibonacci numbers:")
    fib_gen = fibonacci_gen()
    for _ in range(10):
        print(next(fib_gen), end=" ")
    print("\n")
    
    # Generator pipeline
    print("Pipeline: numbers -> squared -> filtered (>10):")
    pipeline = filtered(squared(numbers(10)), 10)
    print(list(pipeline))
    print()
    
    # Custom iterator
    print("Countdown from 5:")
    for num in Countdown(5):
        print(num, end=" ")
    print("\n")
    
    # Context manager
    with timer_context("Sleep test"):
        import time
        time.sleep(0.2)
