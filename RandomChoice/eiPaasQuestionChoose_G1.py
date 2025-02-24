# This script randomly picks numbers from 1 to 195 without replacement, one by one, waiting for user input to proceed.

import random

print("Starting to pick numbers from 1 to 195.")
pool = list(range(1, 196))  # Creates list [1, 2, ..., 195]

while pool:
    number = random.choice(pool)  # Randomly select a number
    print("Number picked:", number)  # Display the selected number
    pool.remove(number)  # Remove the number to avoid repetition
    input("Click enter to choose another number.")  # Wait for user input

print("All numbers have been picked.")  # Inform user when done