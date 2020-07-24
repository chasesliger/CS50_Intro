# import get float function from cs50 library
from cs50 import get_float

# initialize variables for each coin value
q = 25
d = 10
n = 5
p = 1

# ask user for float until it is positive
while True:
    dollars = get_float("Change owed: ")
    if dollars > 0:
        break

# convert and round dollars to cents
cents = round(dollars * 100)

# initialize a variable to keep track of how many times each coin is used in algorithm
coins = 0

# series of while loops that try to divide cents by coin value, iterate coin count, subtract that value from cents
while (cents / q) >= 1:
    coins += 1
    cents -= q

while (cents / d) >= 1:
    coins += 1
    cents -= d

while (cents / n) >= 1:
    coins += 1
    cents -= n

while (cents / p) >= 1:
    coins += 1
    cents -= p

print(coins)