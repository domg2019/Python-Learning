'''
This script:
1. Creates a list of numbers from 1 to 195.
2. Shuffles the list to ensure randomness.
3. Waits for the user to press Enter before picking a number.
4. Removes and prints a number from the list.
5. Repeats until all numbers are picked.
'''


import random


def main():
    numbers = list(range(1, 196))  # Create a list of numbers from 1 to 195
    random.shuffle(numbers)  # Shuffle the numbers to ensure randomness

    while numbers:
        input("Press Enter to pick a number...")  # Wait for user input
        picked_number = numbers.pop(0)  # Pick and remove the first number
        print(f"Picked number: {picked_number}")

    print("All numbers have been picked!")


if __name__ == "__main__":
    main()