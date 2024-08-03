# oop practice
from dataclasses import dataclass

class Dog:
    species = "Canis familiaris"
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def bark(self):
        return f"{self.name} says Woof!"
