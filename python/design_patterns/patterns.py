# design patterns
import copy
from abc import ABC, abstractmethod
from typing import List, Any


# ============ Creational Patterns ============

# Singleton Pattern
class Singleton:
    """Singleton pattern - ensures only one instance exists."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class DatabaseConnection(Singleton):
    """Example Singleton - Database connection."""
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = "Connected to database"
            self.initialized = True


# Factory Pattern
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


class AnimalFactory:
    """Factory pattern - creates objects without exposing creation logic."""
    
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


# Builder Pattern
class Pizza:
    """Product to be built."""
    
    def __init__(self):
        self.size = "medium"
        self.cheese = True
        self.toppings: List[str] = []
    
    def __str__(self):
        return f"Pizza(size={self.size}, cheese={self.cheese}, toppings={self.toppings})"


class PizzaBuilder:
    """Builder pattern - constructs complex objects step by step."""
    
    def __init__(self):
        self.pizza = Pizza()
    
    def set_size(self, size: str) -> 'PizzaBuilder':
        self.pizza.size = size
        return self
    
    def add_cheese(self, cheese: bool = True) -> 'PizzaBuilder':
        self.pizza.cheese = cheese
        return self
    
    def add_topping(self, topping: str) -> 'PizzaBuilder':
        self.pizza.toppings.append(topping)
        return self
    
    def build(self) -> Pizza:
        return self.pizza


# ============ Structural Patterns ============

# Adapter Pattern
class OldPrinter:
    """Old interface that needs adapting."""
    
    def print_old(self, text: str) -> str:
        return f"[OLD] {text}"


class NewPrinterInterface(ABC):
    @abstractmethod
    def print(self, text: str) -> str:
        pass


class PrinterAdapter(NewPrinterInterface):
    """Adapter pattern - makes incompatible interfaces work together."""
    
    def __init__(self, old_printer: OldPrinter):
        self.old_printer = old_printer
    
    def print(self, text: str) -> str:
        return self.old_printer.print_old(text)


# Decorator Pattern (not Python decorator, the design pattern)
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass


class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0
    
    def description(self) -> str:
        return "Simple coffee"


class CoffeeDecorator(Coffee):
    """Decorator pattern - adds behavior dynamically."""
    
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()
    
    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.5
    
    def description(self) -> str:
        return super().description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.2
    
    def description(self) -> str:
        return super().description() + ", sugar"


# ============ Behavioral Patterns ============

# Observer Pattern
class Subject:
    """Observable subject."""
    
    def __init__(self):
        self._observers: List['Observer'] = []
        self._state = None
    
    def attach(self, observer: 'Observer') -> None:
        self._observers.append(observer)
    
    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state: Any) -> None:
        self._state = state
        self.notify()


class Observer(ABC):
    @abstractmethod
    def update(self, state: Any) -> None:
        pass


class EmailObserver(Observer):
    def update(self, state: Any) -> None:
        print(f"Email notification: {state}")


class SMSObserver(Observer):
    def update(self, state: Any) -> None:
        print(f"SMS notification: {state}")


# Strategy Pattern
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with credit card"


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with PayPal"


class ShoppingCart:
    """Context that uses a strategy."""
    
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    
    def checkout(self, amount: float) -> str:
        return self._strategy.pay(amount)


if __name__ == "__main__":
    # Singleton
    print("=== Singleton ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")
    
    # Factory
    print("\n=== Factory ===")
    dog = AnimalFactory.create_animal("dog")
    cat = AnimalFactory.create_animal("cat")
    print(f"Dog says: {dog.speak()}")
    print(f"Cat says: {cat.speak()}")
    
    # Builder
    print("\n=== Builder ===")
    pizza = (PizzaBuilder()
             .set_size("large")
             .add_cheese()
             .add_topping("pepperoni")
             .add_topping("mushrooms")
             .build())
    print(pizza)
    
    # Adapter
    print("\n=== Adapter ===")
    old_printer = OldPrinter()
    adapter = PrinterAdapter(old_printer)
    print(adapter.print("Hello World"))
    
    # Decorator
    print("\n=== Decorator ===")
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    print(f"{coffee.description()}: ${coffee.cost()}")
    
    # Observer
    print("\n=== Observer ===")
    subject = Subject()
    subject.attach(EmailObserver())
    subject.attach(SMSObserver())
    subject.set_state("New order received!")
    
    # Strategy
    print("\n=== Strategy ===")
    cart = ShoppingCart(CreditCardPayment())
    print(cart.checkout(100))
    cart.set_strategy(PayPalPayment())
    print(cart.checkout(50))

# pattern selection
