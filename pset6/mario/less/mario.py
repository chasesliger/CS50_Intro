# import get integer function form CS50 library
from cs50 import get_int

# prompt user for input until it is an integer in the desired range
while True:
    height = get_int("Height:  ")
    if 0 < height < 9:
        break

# for loop to print, start at 1 and go till height plus 1 so the math works out
for i in range(1, height + 1):
    print(" " * (height - i), end="")
    print("#" * i, end="")
    print()
