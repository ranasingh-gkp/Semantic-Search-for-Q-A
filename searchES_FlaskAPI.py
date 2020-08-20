import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf
import tensorflow_hub as hub
from flask import Flask



def connect2ES():
    # connect to ES on localhost on port 9200
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
            print('Connected to ES!')
    else:
            print('Could not connect!')
            sys.exit()

    print("*********************************************************************************");
    return es

def keywordSearch(es, q):
    #Search by Keywords
    b={
            'query':{
                'match':{
                    "title":q
                }
            }
        }

    res= es.search(index='questions-index',body=b)

    return res


# Search by Vec Similarity
def sentenceSimilaritybyNN(es, sent):
    query_vector = tf.make_ndarray(tf.make_tensor_proto(embed([sent]))).tolist()[0]
    b = {"query" : {
                "script_score" : {
                    "query" : {
                        "match_all": {}
                    },
                    "script" : {
                        "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
             }
        }


    #print(json.dumps(b,indent=4))
    res= es.search(index='questions-index',body=b)
    
    return res;


app = Flask(__name__)
es = connect2ES();
embed = hub.load("./data/USE4/")

@app.route('/search/<query>')
def search(query):
    q = query.replace("+", " ")
    res_kw = keywordSearch(es, q)
    res_semantic = sentenceSimilaritybyNN( es, q)

    ret = ""
    for hit in res_kw['hits']['hits']:
        ret += (" KW: " + str( hit['_score']) + "\t" + hit['_source']['title'] +"\n" )

    for hit in res_semantic['hits']['hits']:
        ret += (" Semantic: " +str(hit['_score']) + "\t" + hit['_source']['title'] +"\n")
    return ret
