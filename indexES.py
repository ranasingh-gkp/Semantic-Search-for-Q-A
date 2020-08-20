import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf
import tensorflow_hub as hub


# connect to ES on localhost on port 9200
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
	print('Connected to ES!')
else:
	print('Could not connect!')
	sys.exit()

print("*********************************************************************************");


# index in ES = DB in an RDBMS
# Read each question and index into an index called questions
# Indexing only titles for this example to improve speed. In practice, its good to index CONCATENATE(title+body)
# Define the index


#Refer: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
# Mapping: Structure of the index
# Property/Field: name and type  
b = {"mappings": {
  	"properties": {
    		"title": {
      			"type": "text"
    		},
    		"title_vector": {
      			"type": "dense_vector",
      			"dims": 512
		}
	}
     }
   }


ret = es.indices.create(index='questions-index', ignore=400, body=b) #400 caused by IndexAlreadyExistsException, 
print(json.dumps(ret,indent=4))

# TRY this in browser: http://localhost:9200/questions-index

print("*********************************************************************************");

sys.exit();

#load USE4 model

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")




# CONSTANTS
NUM_QUESTIONS_INDEXED = 200000

# Col-Names: Id,OwnerUserId,CreationDate,ClosedDate,Score,Title,Body
cnt=0

with open('./data/Questions.csv', encoding="latin1") as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',' )
	next(readCSV, None)  # skip the headers 
	for row in readCSV:
		#print(row[0], row[5])
		doc_id = row[0];
		title = row[5];
		vec = tf.make_ndarray(tf.make_tensor_proto(embed([title]))).tolist()[0]		
		
		b = {"title":title,
			"title_vector":vec,
			}	
		#print(json.dumps(tmp,indent=4))		
		
		res = es.index(index="questions-index", id=doc_id, body=b)
		#print(res)
		

		# keep count of # rows processed
		cnt += 1
		if cnt%100==0:
			print(cnt)
		
		if cnt == NUM_QUESTIONS_INDEXED:
			break;

	print("Completed indexing....")

	print("*********************************************************************************");
	




