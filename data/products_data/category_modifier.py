import csv
import re

# with open("myntra_men.csv", mode='r') as f:
#     with open("myntra_men_modified.csv", mode='w') as f2:
#         r = csv.reader(f)
#         w = csv.writer(f2)

data = []

with open("myntra_women.csv", mode='r') as f:
    r = csv.reader(f)
    for i in r:
        newRow = i
        if (re.search("women-", i[1])):
            print("y: " + i[1])
            newRow[1] = i[1][6:]
        elif(re.search("womens-", i[1])):
            print("y: " + i[1])
            newRow[1] = i[1][7:]
        else:
            print("n: " + i[1])
        data.append(newRow)

with open("myntra_women_latest.csv", mode='w', newline='\n') as f:
    w = csv.writer(f)
    w.writerows(data)
