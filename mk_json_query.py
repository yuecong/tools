#python mk_json_quert.py & excute it in backgroud
# excute ES query and export it to apache directory for data visulization
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os.path
import time
import json

#JSON export for further data visulization
FILE_PATH_JSON_HITINFO = "/var/www/cache_info1.json"
FILE_PATH_JSON_TOP_REQUEST_URL = "/var/www/toprequestURL.json"
FILE_PATH_JSON_TOP_MISS_URL = "/var/www/topchachemissURL.json"
FILE_PATH_JSON_SYSINFO = "/var/www/sysinfo.json"

#ES information
ES_HOST = {
    "host" : "10.0.0.158", 
    "port" : 9200
}
INDEX_ATS = 'ats'
INDEX_ATS_SYS = 'ats_sysinfo'

POLL_INTERVAL = 5 #5 seconds

mBody_hitInfo = {
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
mBody_topRequestURLInfo = {
  "size": 0,
  "aggs": {
    "top_request_URL": {
      "terms": {
        "field": "requestURL",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
          "spentTime_stats": {
            "stats": {
              "field": "spentTime"
            }
          },
        "cache_ratio": {
          "avg": {
            "field": "cacheCode"
          }
        },
        "contentSize": {
          "avg": {
            "field": "contentLength"
          }
        }
      }
    }
  }
}
mBody_topCacheMissURLInfo = {
  "query": {
    "filtered": {
      "query": {
        "match_all": {}
      },
      "filter": {
        "term": {
          "cacheCode": 0
        }
      }
    }
  },
  "size": 0,
  "aggs": {
    "top_request_URL": {
      "terms": {
        "field": "requestURL",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "spentTime_stats": {
          "stats": {
            "field": "spentTime"
          }
        },
        "contentSize": {
          "avg": {
            "field": "contentLength"
          }
        }
      }
    }
  }
}

mBody_sysInfo ={
  "query": {
    "match_all": {}
  },
   "size": 1,
   "sort": [
     {
       "timeStamp": {
         "order": "desc"
       }
     }
   ]
}

# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

def exportInfo(index_for_query,mBody,filePath):
    #print (mBody)
    res = es.search(index = index_for_query, size=1, body = mBody)
    #print(res)
    f = open(filePath,'w') #clear the contents
    f.write(json.dumps(res))
    f.close()

#Main function    
if __name__ == '__main__':
    while (True):  
        exportInfo(INDEX_ATS,mBody_hitInfo,FILE_PATH_JSON_HITINFO)
        exportInfo(INDEX_ATS,mBody_topRequestURLInfo,FILE_PATH_JSON_TOP_REQUEST_URL)
        exportInfo(INDEX_ATS,mBody_topCacheMissURLInfo,FILE_PATH_JSON_TOP_MISS_URL)
        exportInfo(INDEX_ATS_SYS,mBody_sysInfo,FILE_PATH_JSON_SYSINFO)
        time.sleep(POLL_INTERVAL)


        


