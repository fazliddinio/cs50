# async examples
import asyncio
import time
from typing import List


# Basic Async Function
async def say_hello(name: str, delay: float = 1.0) -> str:
    """Async function with delay."""
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


# Running Multiple Coroutines
async def main_gather():
    """Run multiple coroutines concurrently with gather."""
    results = await asyncio.gather(
        say_hello("Alice", 1),
        say_hello("Bob", 2),
        say_hello("Charlie", 1.5),
    )
    for result in results:
        print(result)


# Async Context Manager
class AsyncResource:
    """Example async context manager."""
    
    async def __aenter__(self):
        print("Acquiring resource...")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource...")
        await asyncio.sleep(0.1)
    
    async def do_work(self):
        await asyncio.sleep(0.2)
        return "Work done!"


# Async Iterator
class AsyncCounter:
    """Async iterator example."""
    
    def __init__(self, stop: int):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.current += 1
        return self.current


# Async Generator
async def async_range(count: int):
    """Async generator."""
    for i in range(count):
        await asyncio.sleep(0.1)
        yield i


# Producer-Consumer Pattern
async def producer(queue: asyncio.Queue, n: int):
    """Produce items and put in queue."""
    for i in range(n):
        await asyncio.sleep(0.1)
        await queue.put(f"item-{i}")
        print(f"Produced: item-{i}")
    await queue.put(None)  # Signal end


async def consumer(queue: asyncio.Queue):
    """Consume items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        await asyncio.sleep(0.2)


async def producer_consumer_demo():
    """Demo producer-consumer pattern."""
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue, 5),
        consumer(queue),
    )


# Semaphore for Rate Limiting
async def limited_task(sem: asyncio.Semaphore, name: str):
    """Task with semaphore limiting."""
    async with sem:
        print(f"Task {name} started")
        await asyncio.sleep(1)
        print(f"Task {name} completed")


async def semaphore_demo():
    """Demo semaphore for concurrent limit."""
    sem = asyncio.Semaphore(2)  # Max 2 concurrent
    tasks = [limited_task(sem, str(i)) for i in range(5)]
    await asyncio.gather(*tasks)


# Timeout
async def long_operation():
    """Operation that takes too long."""
    await asyncio.sleep(10)
    return "Completed"


async def timeout_demo():
    """Demo timeout handling."""
    try:
        result = await asyncio.wait_for(long_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out!")


# HTTP Requests with aiohttp (requires: pip install aiohttp)
try:
    import aiohttp

    async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
        """Fetch a URL asynchronously."""
        async with session.get(url) as response:
            return {
                "url": url,
                "status": response.status,
                "length": len(await response.text())
            }

    async def fetch_multiple_urls(urls: List[str]):
        """Fetch multiple URLs concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results

except ImportError:
    pass


if __name__ == "__main__":
    # Basic async
    print("=== Basic Async ===")
    result = asyncio.run(say_hello("World"))
    print(result)
    
    # Gather
    print("\n=== Gather ===")
    asyncio.run(main_gather())
    
    # Async context manager
    print("\n=== Async Context Manager ===")
    async def context_demo():
        async with AsyncResource() as resource:
            result = await resource.do_work()
            print(result)
    asyncio.run(context_demo())
    
    # Async iterator
    print("\n=== Async Iterator ===")
    async def iterator_demo():
        async for num in AsyncCounter(5):
            print(num, end=" ")
        print()
    asyncio.run(iterator_demo())
    
    # Timeout
    print("\n=== Timeout ===")
    asyncio.run(timeout_demo())

# benchmark
