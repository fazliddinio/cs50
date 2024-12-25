# control flow practice

# If-Elif-Else
def check_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


# Ternary operator
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")


# For loops
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# For loop with index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# Range
for i in range(5):
    print(i)

for i in range(2, 10, 2):
    print(i)


# While loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1


# Break and Continue
for i in range(10):
    if i == 3:
        continue
    if i == 7:
        break
    print(i)


# List comprehension
squares = [x**2 for x in range(10)]
print(squares)

even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)

# Dictionary comprehension
square_dict = {x: x**2 for x in range(5)}
print(square_dict)

# Nested loops
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for item in row:
        print(item, end=" ")
    print()


# Match statement
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown"


print(http_status(200))
print(http_status(404))

# fizzbuzz

# exercises done

# cleanup
