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

    # Quarters (25 cents)
    coins += cents // 25
    cents %= 25

    # Dimes (10 cents)
    coins += cents // 10
    cents %= 10

    # Nickels (5 cents)
    coins += cents // 5
    cents %= 5

    # Pennies (1 cent)
    coins += cents

    print(coins)


if __name__ == "__main__":
    main()

# python vs C
