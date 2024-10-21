# async examples
import asyncio
import time
from typing import List

async def say_hello(name, delay=1.0):
    await asyncio.sleep(delay)
    return f"Hello, {name}!"

async def main():
    result = await say_hello("World")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

# gather
