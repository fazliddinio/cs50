def main():
    while True:
        try:
            change = float(input("Change owed: "))
            if change >= 0:
                break
        except ValueError:
            pass

    cents = round(change * 100)
    coins = 0
    # TODO: calculate minimum coins
    print(coins)

if __name__ == "__main__":
    main()

# quarters dimes nickels pennies
