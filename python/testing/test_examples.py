# pytest examples
import pytest
from typing import List


# ============ Code to Test ============

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_palindrome(s: str) -> bool:
    """Check if string is palindrome."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    result = [0, 1]
    for _ in range(2, n):
        result.append(result[-1] + result[-2])
    return result


class Calculator:
    """Simple calculator class."""
    
    def __init__(self):
        self.result = 0
    
    def add(self, value: float) -> 'Calculator':
        self.result += value
        return self
    
    def subtract(self, value: float) -> 'Calculator':
        self.result -= value
        return self
    
    def multiply(self, value: float) -> 'Calculator':
        self.result *= value
        return self
    
    def reset(self) -> 'Calculator':
        self.result = 0
        return self


# ============ Tests ============

class TestAdd:
    """Tests for add function."""
    
    def test_add_positive_numbers(self):
        assert add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        assert add(-1, -1) == -2
    
    def test_add_zero(self):
        assert add(0, 0) == 0
    
    def test_add_mixed(self):
        assert add(-1, 1) == 0


class TestDivide:
    """Tests for divide function."""
    
    def test_divide_normal(self):
        assert divide(10, 2) == 5.0
    
    def test_divide_float(self):
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestPalindrome:
    """Tests for is_palindrome function."""
    
    @pytest.mark.parametrize("input_str,expected", [
        ("racecar", True),
        ("hello", False),
        ("A man a plan a canal Panama", True),
        ("", True),
        ("a", True),
        ("Was it a car or a cat I saw?", True),
    ])
    def test_palindrome(self, input_str, expected):
        assert is_palindrome(input_str) == expected


class TestFibonacci:
    """Tests for fibonacci function."""
    
    def test_fibonacci_zero(self):
        assert fibonacci(0) == []
    
    def test_fibonacci_one(self):
        assert fibonacci(1) == [0]
    
    def test_fibonacci_two(self):
        assert fibonacci(2) == [0, 1]
    
    def test_fibonacci_ten(self):
        assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


class TestCalculator:
    """Tests for Calculator class."""
    
    @pytest.fixture
    def calc(self):
        """Create a calculator instance."""
        return Calculator()
    
    def test_initial_value(self, calc):
        assert calc.result == 0
    
    def test_add(self, calc):
        calc.add(5)
        assert calc.result == 5
    
    def test_subtract(self, calc):
        calc.add(10).subtract(3)
        assert calc.result == 7
    
    def test_multiply(self, calc):
        calc.add(5).multiply(3)
        assert calc.result == 15
    
    def test_chaining(self, calc):
        calc.add(10).subtract(5).multiply(2)
        assert calc.result == 10
    
    def test_reset(self, calc):
        calc.add(100).reset()
        assert calc.result == 0


# Run with: pytest testing.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
