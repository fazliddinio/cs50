# design patterns
from abc import ABC, abstractmethod
from typing import List, Any

class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# factory
