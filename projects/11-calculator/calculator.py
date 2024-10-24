#!/usr/bin/env python3
"""Calculator CLI"""
import math
import operator

class Calculator:
    def __init__(self):
        self.history = []
        self.last_result = 0
    
    def calculate(self, expr):
        result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi})
        self.history.append(f"{expr} = {result}")
        self.last_result = float(result)
        return result
