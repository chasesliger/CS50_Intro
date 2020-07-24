from sys import argv, exit
from cs50 import SQL

# check to make sure that usage is correct
# error checking to make sure the usage is correct
if len(argv) != 2:
    print("Usage: python report.py 'house name'")
    exit(1)

# open the SQL database
db = SQL("sqlite:///students.db")

# sql query to get first middle last and birth year from table by house
query = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])

for row in query:

    if row["middle"] == None:
        # print without middle name
        print(row["first"], row["last"] + ", born", row["birth"])

    else:
        # otherwise if they have a middle name
        print(row["first"], row["middle"], row["last"] + ", born", row["birth"])