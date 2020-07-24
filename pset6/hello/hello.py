#import cs50 library for the function to get a string
from cs50 import get_string

#get string and store in answer...us \n to get the input on a newline
answer = get_string("What is your name? \n")

#print using a formated string
print(f"hello, {answer}")