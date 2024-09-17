# generators and iterators
import sys
from typing import Generator, Iterator

def count_up_to(max_value):
    count = 1
    while count <= max_value:
        yield count
        count += 1

for n in count_up_to(5):
    print(n)

# infinite fibonacci

# pipeline pattern
