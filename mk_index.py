# build_index.py
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os.path

FILE_PATH_BLOG = "/usr/local/var/log/trafficserver/squid.blog"
FILE_PATH = "./squid.log.elasticsearch"

ES_HOST = {
    "host" : "10.0.0.158", 
    "port" : 9200
}

INDEX_NAME = 'ats'
TYPE_NAME = 'accesslog'
COMMIT_DATA_PER_TIME =5000
bulk_data = []

# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

def indexPrepare():
    """
    if es.indices.exists(INDEX_NAME):
        print("deleting '%s' index..." % (INDEX_NAME))
        res = es.indices.delete(index = INDEX_NAME)
        print(" response: '%s'" % (res))
    """
    request_body = {
        "mappings" : {
            "accesslog" : {
                "properties" : {
                  "accessTime" : {
                    "type" : "date" ,
                    "format" : "dateOptionalTime"
                  },
                  "authUserName" : {
                    "type" : "string"
                  },
                  "cacheResult" : {
                    "type" : "string"
                  },
                  "cacheCode" : {
                    "type" : "long"
                  },
                  "clientIP" : {
                    "type" : "string"
                  },
                  "contentLength" : {
                    "type" : "long"
                  },
                  "contentType" : {
                    "type" : "string"
                  },
                  "hierarchyRoute" : {
                    "type" : "string"
                  },
                  "requestMethod" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                  },
                  "requestURL" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                  },
                  "responseCode" : {
                    "type" : "long"
                  },
                  "routerServer" : {
                    "type" : "string"
                  },
                  "spentTime" : {
                    "type" : "long"
                  }
                }
          }
        },
        "settings" : {
            "number_of_shards": 5,
            "number_of_replicas": 0
        }
    }

    if not es.indices.exists(INDEX_NAME):
        print("creating '%s' index..." % (INDEX_NAME))
        res = es.indices.create(index = INDEX_NAME, body = request_body)
        print(" response: '%s'" % (res))

def indexBulkData():
    bulk_data = [] 
    logFile = open(FILE_PATH,'r')
    line_cnt= 0
    for line in logFile:
        #print line
        line= line.replace("\n","")
        items=line.split(' ')
        #one example
        # ['1424376277.821', '0', '10.0.0.210', 'TCP_MEM_HIT/200',
        # '86949', 'GET', 'http://www.citrix.co.jp/products.html?posit=glnav', '-', 'NONE/-', 'text/html']
        cacheCode =0
        # refer to squid-netscape-result-codes
        #https://www.websense.com/content/support/library/web/v78/wcg_help/cachrslt.aspx
        #Cache Hit : tcp_hit,tcp_refresh_hit, tcp_mem_hit, tcp_ims_hit
        cacheResult = items[3].split('/')[0].lower()
        if (cacheResult == "tcp_hit" or cacheResult == "tcp_ims_hit" or cacheResult == "tcp_mem_hit" or cacheResult == "tcp_refresh_hit" ):
            cacheCode = 1
        data_dict = {
        "_index": INDEX_NAME, 
        "_type": TYPE_NAME, 
        "_source": {
                'accessTime': datetime.datetime.fromtimestamp(float(items[0])).strftime('%Y-%m-%dT%H:%M:%SZ'), #The client request timestamp
                'spentTime': items[1], #The time Traffic Server spent processing the client request. 
                                       #The number of milliseconds between the time the client established the connection with Traffic Server 
                                       #and the time Traffic Server sent the last byte of the response back to the client.
                'clientIP': items[2], #The IP address of the client's host machine.
                'cacheResult': items[3].split('/')[0], #The cache result code; how the cache responded to the request: HIT, MISS, and so on. 
                'cacheCode' : cacheCode, #1 Cache Hit(), 0 Cache MISS()
                'responseCode': items[3].split('/')[1], #The proxy response status code (the HTTP response status code from Traffic Server to client
                'contentLength': items[4], #The length of the Traffic Server response to the client in bytes, including headers and content.
                'requestMethod': items[5], #The client request method: GET, POST, and so on.
                'requestURL': items[6], #The client request canonical URL; 
                                       #blanks and other characters that might not be parsed by log analysis tools are 
                                       #replaced by escape sequences. The escape sequence is a percentage sign 
                                       #followed by the ASCII code number of the replaced character in hex.
                'authUserName': items[7], #The username of the authenticated client. 
                                          #A hyphen (-) means that no authentication was required.
                'hierarchyRoute': items[8].split('/')[0], # The proxy hierarchy route. 
                'routerServer': items[8].split('/')[1], # The route Traffic Server used to retrieve the object. 
                'contentType': items[9] # The proxy response content type. The object content type taken from the Traffic Server response header.
            }
        }
        #bulk_data.append(op_dict)
        bulk_data.append(data_dict)
        line_cnt = line_cnt +1
        if line_cnt == COMMIT_DATA_PER_TIME:
            # bulk index the data
            #print("bulk indexing...")
            #print(bulk_data)
            #res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
            helpers.bulk(es,bulk_data)
            es.indices.refresh()
            #print(" response: '%s'" % (res))
            line_cnt =0
            bulk_data = []
            #res = es.count(index= INDEX_NAME, doc_type= TYPE_NAME, body={"query": {"match_all": {}}})
            #print(" response: '%s'" % (res))
    #print(bulk_data)
    if len(bulk_data) >0:
      #res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
        #print bulk_data
        res = helpers.bulk(es,bulk_data)
        es.indices.refresh()
    # sanity check
    #print("searching...")
    res = es.search(index = INDEX_NAME, size=3, body={"query": {"match_all": {}}})
    #print(" response: '%s'" % (res))
def prepareLogFile():
    result = True
    result = os.path.isfile(FILE_PATH_BLOG)
    return result


if prepareLogFile(): #if squid.blog exists and converted to squid.log.elasticsearch with traffic_logcat sucessfully
    print("Inserting...")
    indexPrepare()
    indexBulkData()


