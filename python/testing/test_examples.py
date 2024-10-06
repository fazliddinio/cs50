# pytest examples
import pytest
from typing import List

def add(a, b): return a + b

class TestAdd:
    def test_positive(self): assert add(2, 3) == 5
    def test_negative(self): assert add(-1, -1) == -2
    def test_zero(self): assert add(0, 0) == 0
