import csv

# DONOT use pandas here as it laods all of data into RAM at once.


cnt=0

with open('./data/Questions.csv', encoding="latin1") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', )
        next(readCSV, None)  # skip the headers
        for row in readCSV:
                # keep count of # rows processed
                cnt += 1
                #print(cnt)

print(cnt,len(row))




cnt=0

with open('./data/Answers.csv', encoding="latin1") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip the headers
        for row in readCSV:
                # keep count of # rows processed
                cnt += 1

print(cnt,len(row))
