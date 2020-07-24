# import get string function from CS50 library
from cs50 import get_string
import string

# ask user for a text to be analyzed
text = get_string("Text: ")

# create list of punctuation to check for below
punctuation = [".", "!", "?"]

# initialize letter and sentence count
letters = 0
sentences = 0

# split text by white space then take the lenght of the resulting list...this seems like an easier way to get the word count than counting spaces, with counting spaces you have to initialize at 1
words = len(text.split(" "))

# iterate over chars in string, incrementing letter if they are a letter, and sentences if they are a puncuation
for char in text:
    if char.isalpha():
        letters += 1
    if char in punctuation:
        sentences += 1

# calculate L and S...using floats for precision
L = float(letters) / float(words) * 100
S = float(sentences) / float(words) * 100

# forumla for Coleman-Liau index
Grade = round(0.0588 * L - 0.296 * S - 15.8)

# if below 1, print before grade 1, if above print 16+, elsewise print grade level
if Grade < 1:
    print("Before Grade 1")

elif Grade > 16:
    print("Grade 16+")

else:
    print(f"Grade {Grade}")