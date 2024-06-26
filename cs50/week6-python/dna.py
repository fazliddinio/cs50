import csv
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Read database into memory
    database = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    # Read DNA sequence
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # Get STR names from fieldnames
    subsequences = list(database[0].keys())[1:]

    # Find longest match of each STR
    result = {}
    for subsequence in subsequences:
        result[subsequence] = longest_match(sequence, subsequence)

    # Check database for matching profiles
    for person in database:
        match = True
        for subsequence in subsequences:
            if int(person[subsequence]) != result[subsequence]:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()

# cleanup done
