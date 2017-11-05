import csv

values = []

""" SET STANDARD FORMAT 
C:[0] SYMBOL
C:[1] OPEN
C:[2] HIGH
C:[3] LOW
C:[4] CLOSE
C:[5] CHANGE
C:[6] CHANGE_PERCENT
C:[7] BID
C:[8] OFFER
C:[9] VOLUMN
C:[10] VALUE_000BAHT
"""

f = open('sec_result\\20171025_SET_glob_all_result.csv')
lines_sort = f.readlines()
f.close()
lines_sort.sort()
i=0

with open('sec_result\\20171025_SET_glob_all_result.csv') as file_object:
    for line in sorted(csv.reader(file_object, delimiter=',')):
        print(line[0] + "|" + line[1] + "|" + line[2] + "|" + line[3] + "|" + \
            line[4] + "|" + line[5] + "|" + line[6] + "|" + line[7] + "|" + \
            line[8] + "|" + line[9] + "|" + line[10] )

        i=i+1
        values.append(map(int, line))

print("rows:", i)
print("columns")
#for column in itertools.izip(*values):
#    print(column)
