#python mk_json_quert.py & excute it in backgroud
# excute ES query and export it to apache directory for data visulization
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os.path
import time
import json

#JSON export for further data visulization
FILE_PATH_JSON1 = "/var/www/cache_info1.json"

#ES information
ES_HOST = {
    "host" : "10.0.0.158", 
    "port" : 9200
}
INDEX_NAME = 'ats'
TYPE_NAME = 'accesslog'
POLL_INTERVAL = 10 #10 seconds

mBody = {
  "query": {
    "filtered": {
      "query": {
        "match_all": {}
      },
      "filter": {
        "range": {
          "accessTime": {
            "gte": "now-1d/d"
          }
        }
      }
    }
  },
  "size": 0,
  "aggregations": {
    "accessTime_1h": {
      "date_histogram": {
        "field": "accessTime",
        "interval": "1h",
        "order": {
          "_key": "desc"
        },
        "min_doc_count": 0
      },
      "aggs": {
        "hit_ratio": {
          "avg": {
            "field": "cacheCode"
          }
        },
        "size_access_info": {
          "terms": {
            "field": "cacheCode",
            "size": 2
          },
          "aggs": {
            "sum_cache_size": {
              "sum": {
                "field": "contentLength"
              }
            }
          }
        }
      }
    },
    "accessTime_5m": {
      "date_histogram": {
        "field": "accessTime",
        "interval": "5m",
        "order": {
          "_key": "desc"
        },
        "min_doc_count": 0
      },
      "aggs": {
        "hit_ratio": {
          "avg": {
            "field": "cacheCode"
          }
        },
        "size_access_info": {
          "terms": {
            "field": "cacheCode",
            "size": 2
          },
          "aggs": {
            "sum_cache_size": {
              "sum": {
                "field": "contentLength"
              }
            }
          }
        }
      }
    }
  }
}


# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

def exportInfo(mBody,filePath):
    #print (mBody)
    res = es.search(index = INDEX_NAME, size=0, body = mBody)
    #print(res)
    f = open(filePath,'w') #clear the contents
    f.write(json.dumps(res))
    f.close()

#Main function    
if __name__ == '__main__':
    while (True):  
        exportInfo(mBody,FILE_PATH_JSON1)
        time.sleep(POLL_INTERVAL)


        


