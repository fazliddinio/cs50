# oop practice
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


# Basic Class
class Dog:
    """A simple Dog class."""
    
    species = "Canis familiaris"  # Class attribute
    
    def __init__(self, name: str, age: int):
        self.name = name  # Instance attribute
        self.age = age
    
    def __str__(self):
        return f"{self.name} is {self.age} years old"
    
    def __repr__(self):
        return f"Dog(name='{self.name}', age={self.age})"
    
    def bark(self):
        return f"{self.name} says Woof!"
    
    def birthday(self):
        self.age += 1
        return f"Happy birthday {self.name}! Now {self.age} years old."


# Inheritance
class GoldenRetriever(Dog):
    """Golden Retriever inherits from Dog."""
    
    def __init__(self, name: str, age: int, trained: bool = False):
        super().__init__(name, age)
        self.trained = trained
    
    def fetch(self):
        return f"{self.name} fetches the ball!"
    
    # Method overriding
    def bark(self):
        return f"{self.name} says Woof Woof! (friendly)"


# Abstract Base Class
class Animal(ABC):
    """Abstract base class for animals."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def speak(self):
        """All animals must implement speak."""
        pass
    
    @abstractmethod
    def move(self):
        """All animals must implement move."""
        pass


class Cat(Animal):
    """Cat implementation of Animal."""
    
    def speak(self):
        return f"{self.name} says Meow!"
    
    def move(self):
        return f"{self.name} walks gracefully"


class Bird(Animal):
    """Bird implementation of Animal."""
    
    def speak(self):
        return f"{self.name} says Tweet!"
    
    def move(self):
        return f"{self.name} flies through the air"


# Encapsulation with Properties
class BankAccount:
    """Bank account with encapsulation."""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance  # Protected
        self.__account_number = "1234567890"  # Private
    
    @property
    def balance(self):
        """Get current balance."""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """Set balance with validation."""
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
    
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount: float):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance


# Dataclass (Python 3.7+)
@dataclass
class Point:
    """A point in 2D space."""
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass
class Person:
    """Person dataclass with default values."""
    name: str
    age: int
    email: Optional[str] = None
    skills: List[str] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []


# Composition
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower
    
    def start(self):
        return "Engine started"


class Car:
    """Car class using composition."""
    
    def __init__(self, brand: str, engine: Engine):
        self.brand = brand
        self.engine = engine  # Composition
    
    def start(self):
        return f"{self.brand}: {self.engine.start()}"


if __name__ == "__main__":
    # Test Dog
    buddy = Dog("Buddy", 3)
    print(buddy)
    print(buddy.bark())
    
    # Test inheritance
    max_dog = GoldenRetriever("Max", 5, trained=True)
    print(max_dog.bark())
    print(max_dog.fetch())
    
    # Test polymorphism
    animals: List[Animal] = [Cat("Whiskers"), Bird("Tweety")]
    for animal in animals:
        print(animal.speak())
        print(animal.move())
    
    # Test encapsulation
    account = BankAccount("John", 1000)
    account.deposit(500)
    print(f"Balance: ${account.balance}")
    
    # Test dataclass
    point = Point(3, 4)
    print(f"Distance: {point.distance_from_origin()}")
    
    # Test composition
    engine = Engine(200)
    car = Car("Tesla", engine)
    print(car.start())
