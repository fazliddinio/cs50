#!/usr/bin/env python3
"""
Calculator CLI - A command-line calculator with history
"""
import argparse
import math
import operator
from typing import List, Optional


class Calculator:
    """Calculator with history and memory."""
    
    OPERATIONS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '**': operator.pow,
        '%': operator.mod,
        '//': operator.floordiv,
    }
    
    def __init__(self):
        self.history: List[str] = []
        self.memory: float = 0
        self.last_result: float = 0
    
    def calculate(self, expression: str) -> float:
        """Evaluate a math expression."""
        # Replace common math functions
        expression = expression.replace('^', '**')
        
        try:
            # Safe evaluation with limited builtins
            allowed_names = {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'pi': math.pi,
                'e': math.e,
                'abs': abs,
                'round': round,
                'pow': pow,
                'ans': self.last_result,
                'mem': self.memory,
            }
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            self.last_result = float(result)
            self.history.append(f"{expression} = {result}")
            
            return result
            
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def basic_calc(self, a: float, op: str, b: float) -> float:
        """Perform basic calculation."""
        if op not in self.OPERATIONS:
            raise ValueError(f"Unknown operator: {op}")
        
        if op in ('/', '//', '%') and b == 0:
            raise ValueError("Division by zero")
        
        result = self.OPERATIONS[op](a, b)
        self.history.append(f"{a} {op} {b} = {result}")
        self.last_result = result
        return result
    
    def memory_store(self, value: float = None) -> None:
        """Store value in memory."""
        self.memory = value if value is not None else self.last_result
    
    def memory_recall(self) -> float:
        """Recall value from memory."""
        return self.memory
    
    def memory_clear(self) -> None:
        """Clear memory."""
        self.memory = 0
    
    def show_history(self, limit: int = 10) -> None:
        """Show calculation history."""
        if not self.history:
            print("No calculations yet")
            return
        
        print("\nCalculation History:")
        print("-" * 40)
        for entry in self.history[-limit:]:
            print(f"  {entry}")
    
    def clear_history(self) -> None:
        """Clear history."""
        self.history = []


def interactive_mode():
    """Run calculator in interactive mode."""
    calc = Calculator()
    
    print("Calculator (type 'help' for commands, 'quit' to exit)")
    print("=" * 50)
    
    while True:
        try:
            expr = input("\n> ").strip()
            
            if not expr:
                continue
            
            if expr.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            
            if expr.lower() == 'help':
                print("\nCommands:")
                print("  Basic math: 2 + 3, 10 * 5, etc.")
                print("  Functions:  sqrt(16), sin(pi/2)")
                print("  Constants:  pi, e")
                print("  Variables:  ans (last result), mem (memory)")
                print("  ms         - store last result in memory")
                print("  mr         - recall memory")
                print("  mc         - clear memory")
                print("  history    - show history")
                print("  clear      - clear history")
                print("  quit       - exit")
                continue
            
            if expr.lower() == 'history':
                calc.show_history()
                continue
            
            if expr.lower() == 'clear':
                calc.clear_history()
                print("History cleared")
                continue
            
            if expr.lower() == 'ms':
                calc.memory_store()
                print(f"Stored: {calc.memory}")
                continue
            
            if expr.lower() == 'mr':
                print(f"Memory: {calc.memory_recall()}")
                continue
            
            if expr.lower() == 'mc':
                calc.memory_clear()
                print("Memory cleared")
                continue
            
            result = calc.calculate(expr)
            print(f"= {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def main():
    parser = argparse.ArgumentParser(description="Calculator CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Calculate command
    calc_parser = subparsers.add_parser("calc", help="Evaluate expression")
    calc_parser.add_argument("expression", nargs="+", help="Math expression")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Interactive calculator")
    
    args = parser.parse_args()
    
    if args.command == "calc":
        calc = Calculator()
        expr = " ".join(args.expression)
        try:
            result = calc.calculate(expr)
            print(result)
        except ValueError as e:
            print(f"Error: {e}")
    
    elif args.command == "interactive":
        interactive_mode()
    
    else:
        # Default to interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
