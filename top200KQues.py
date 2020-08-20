import json
import time
import sys

import csv



# CONSTANTS
NUM_QUESTIONS_INDEXED = 200000

# Col-Names: Id,OwnerUserId,CreationDate,ClosedDate,Score,Title,Body
cnt=0

f = open("top200KQuesData", "w", encoding="latin1")

with open('./data/Questions.csv', encoding="latin1") as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',' )
	next(readCSV, None)  # skip the headers
	for row in readCSV:
		#print(row[0], row[5])
		doc_id = row[0];
		title = row[5];

		# write to file
		f.write(doc_id+ "," +title+"\n")

		# keep count of # rows processed
		cnt += 1
		if cnt%100==0:
			print(cnt)

		if cnt == NUM_QUESTIONS_INDEXED:
			break;

	print("Completed indexing....")

	print("*********************************************************************************");

f.close()
