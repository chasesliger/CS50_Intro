import csv
from sys import argv, exit
from cs50 import SQL

# error checking to make sure the usage is correct
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

# open the SQL database
db = SQL("sqlite:///students.db")

# open the CSV file
with open(argv[1], "r") as characters:

    # create the dictionary reader for the CSV file
    reader = csv.DictReader(characters)

    # for loop and split name into list to handle middle names
    for row in reader:
        name_list = row["name"].split()

        # if the student has no middle name
        if len(name_list) == 2:
            # handle null
            db.execute("INSERT INTO students (first, middle, last, birth, house) VALUES(?, ?, ?, ?, ?)",
                       name_list[0], None, name_list[1], row["birth"], row["house"])

        # otherwise
        else:
            db.execute("INSERT INTO students (first, middle, last, birth, house) VALUES(?, ?, ?, ?, ?)",
                       name_list[0], name_list[1], name_list[2], row["birth"], row["house"])