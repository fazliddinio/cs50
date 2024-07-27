# error handling practice


# Basic try-except
def safe_divide(a, b):
    """Safely divide two numbers."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Invalid types for division")
        return None
    else:
        print(f"Division successful: {result}")
        return result
    finally:
        print("Division operation completed")


# Multiple exceptions
def process_data(data):
    """Process data with multiple error handling."""
    try:
        value = int(data)
        result = 100 / value
        return result
    except ValueError:
        return "Error: Not a valid number"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Unexpected error: {e}"


# Custom Exceptions
class ValidationError(Exception):
    """Custom validation error."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw ${amount}. Balance: ${balance}"
        )


# Using custom exceptions
def validate_age(age):
    """Validate age input."""
    if not isinstance(age, int):
        raise ValidationError("age", "Must be an integer")
    if age < 0:
        raise ValidationError("age", "Cannot be negative")
    if age > 150:
        raise ValidationError("age", "Unrealistic age value")
    return True


def validate_email(email):
    """Basic email validation."""
    if not isinstance(email, str):
        raise ValidationError("email", "Must be a string")
    if "@" not in email:
        raise ValidationError("email", "Must contain @")
    if "." not in email.split("@")[-1]:
        raise ValidationError("email", "Invalid domain")
    return True


# Context manager for error handling
class DatabaseConnection:
    """Simulated database connection with error handling."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        print(f"Connecting to {self.db_name}...")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.db_name}")
        self.connected = False
        if exc_type is not None:
            print(f"Error occurred: {exc_val}")
        return False  # Don't suppress exceptions
    
    def query(self, sql):
        if not self.connected:
            raise ConnectionError("Not connected to database")
        print(f"Executing: {sql}")
        return f"Results for: {sql}"


# Retry decorator with error handling
def retry(max_attempts=3, exceptions=(Exception,)):
    """Decorator to retry function on failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
            raise last_exception
        return wrapper
    return decorator


@retry(max_attempts=3, exceptions=(ValueError,))
def unreliable_function():
    """Function that sometimes fails."""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"


# Assertions
def calculate_discount(price, discount_percent):
    """Calculate discounted price with assertions."""
    assert price >= 0, "Price must be non-negative"
    assert 0 <= discount_percent <= 100, "Discount must be 0-100"
    
    discounted = price * (1 - discount_percent / 100)
    
    assert discounted <= price, "Discounted price exceeds original"
    return round(discounted, 2)


if __name__ == "__main__":
    # Basic try-except
    print("=== Safe Division ===")
    safe_divide(10, 2)
    safe_divide(10, 0)
    
    # Process data
    print("\n=== Process Data ===")
    print(process_data("5"))
    print(process_data("0"))
    print(process_data("abc"))
    
    # Custom exceptions
    print("\n=== Custom Exceptions ===")
    try:
        validate_age(-5)
    except ValidationError as e:
        print(f"Validation failed: {e}")
    
    try:
        validate_email("invalid-email")
    except ValidationError as e:
        print(f"Validation failed: {e}")
    
    # Context manager
    print("\n=== Context Manager ===")
    with DatabaseConnection("mydb") as db:
        result = db.query("SELECT * FROM users")
        print(result)
    
    # Discount calculation
    print("\n=== Assertions ===")
    print(f"$100 with 20% off: ${calculate_discount(100, 20)}")
    print(f"$50 with 10% off: ${calculate_discount(50, 10)}")

# EAFP LBYL
