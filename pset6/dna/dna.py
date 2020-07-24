# import sys.argv and csv modules
from sys import argv, exit
import csv

# error checking to make sure the usage is correct
if len(argv) != 3:
    print("Usage python dna.py data.csv sequence.txt")
    exit(1)

# open up the database as a dictionary reader object
dictionary = open(argv[1])
dict_reader = csv.DictReader(dictionary)

# get STR's from dictionary...fieldnames is a DictReader attribute, and use [1:] to remove the name from the list
STR_list = dict_reader.fieldnames[1:]

# read in sequence rom file
sequence_file = open(argv[2])
sequence = sequence_file.read()

# this for loop is wrong right now, but something like this...maybe make a dictionary of all the STR_list and update that?

# dictionary list comprehension adapted from -> https://thispointer.com/python-how-to-convert-a-list-to-dictionary/
STR_dict = {i: 0 for i in STR_list}

# for loop to go through the sequence file, count the max number of times a STR appears in a row, then add that to the STR dictionary
for STR in STR_list:
    count = 0
    for i in range(len(sequence)):
        if (STR == sequence[i:(i + len(STR))]):
            temp_count = 0
            index1 = i
            index2 = i + len(STR)
            while STR == sequence[index1:index2]:
                temp_count += 1
                index1 += len(STR)
                index2 += len(STR)
            if temp_count > count:
                count = temp_count
    STR_dict[STR] = count


# this loop was used to print out what STR's were found in the sequence
# for STR in STR_dict:
#      print(f"{STR} : ", end="")
#      print(STR_dict[STR])

# intialize a match outside the coming for loop
match = "No match"


# the first loop iterates through the database that has been opened as a Dictionary Reader object
# the second loop loops through the STR's in the sequence that was processed as a dictionary. It compares the STR in sequence to the STR in database
# there is a count variable to make sure that the STR for loop has gone through every STR before it stops and declares a match
for row in dict_reader:
    count = 0
    for STR in STR_list:
        # print("Name: ", row["name"], "STR In Database", row[STR], " STR in dictionary: ", STR_dict[STR])
        if (int(row[STR]) != int(STR_dict[STR])):
            break
        count += 1
        if count == len(STR_list):
            match = row["name"]


print(match)


exit(0)