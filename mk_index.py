# import data from squid.blod of traffic server to elastic search
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os.path
import psutil
import subprocess
import time

#Log data information
FILE_PATH_BLOG = "/usr/local/var/log/trafficserver/squid.blog"
FILE_PATH = "./squid.log.elasticsearch"

#ES information
ES_HOST = {
    "host" : "10.0.0.158", 
    "port" : 9200
}
INDEX_NAME = 'ats'
TYPE_NAME = 'accesslog'
COMMIT_DATA_PER_TIME =5000
bulk_data = []

#For runCommand
procs_id = 0
procs = {}
procs_data = []

# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

def indexPrepare():
    """ #delete index
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
        line= line.replace("\n","")
        items=line.split(' ')
        #data example
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
            helpers.bulk(es,bulk_data)
            es.indices.refresh()
            #print(" response: '%s'" % (res))
            line_cnt =0
            bulk_data = []
    logFile.close()
    #print(bulk_data)
    if len(bulk_data) >0:
        #print bulk_data
        res = helpers.bulk(es,bulk_data)
        es.indices.refresh()
    # sanity check
    #print("searching...")
    res = es.search(index = INDEX_NAME, size=3, body={"query": {"match_all": {}}})
    #print(" response: '%s'" % (res))

# Runs command silently
def runCommand(cmd, use_shell = False, return_stdout = False, busy_wait = False, poll_duration = 0.5):
    # Sanitize cmd to string
    cmd = map(lambda x: '%s' % x, cmd)
    if return_stdout:
        proc = psutil.Popen(cmd, shell = use_shell, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    else:
        proc = psutil.Popen(cmd, shell = use_shell, 
                                stdout = open('/dev/null', 'w'),
                                stderr = open('/dev/null', 'w'))


    global procs_id 
    global procs
    global procs_data
    proc_id = procs_id
    procs[proc_id] = proc
    procs_id += 1
    data = { }
    #print(proc_id)
    while busy_wait:
        returncode = proc.poll()
        if returncode == None:
            try:
                data = proc.as_dict(attrs = ['io_counters', 'cpu_times'])
            except Exception as e:
                pass
            time.sleep(poll_duration)
        else:
            break

    (stdout, stderr) = proc.communicate()
    returncode = proc.returncode
    del procs[proc_id]

    if returncode != 0:
        raise Exception(stderr)
    else:
        if data:
            procs_data.append(data)
        return stdout

#Conver squid.blog to squid.log.elasticsearch if exists
def prepareLogFile():
    result = True
    result = os.path.isfile(FILE_PATH_BLOG)
    if os.path.isfile(FILE_PATH):
        #rm -f ./squid.log.elasticsearch
        cmd = ['rm','-f', FILE_PATH]
        #print(cmd,)
        runCommand(cmd, return_stdout = False, busy_wait = True)
    if result: #In case squid.blog exsits
        
        #traffic_logcat /usr/local/var/log/trafficserver/squid.blog -o ./squid.log.elasticsearch
        cmd = ['traffic_logcat',FILE_PATH_BLOG,'-o',FILE_PATH]
        #print(cmd,)
        runCommand(cmd, return_stdout = False, busy_wait = True)
        result = os.path.isfile(FILE_PATH) #double check FILE_PATH exists
        
        f = open(FILE_PATH_BLOG,'w') #clear the contents
        f.close()
 
    return result

#Main function    
if __name__ == '__main__':
    if prepareLogFile(): #if squid.blog exists and converted to squid.log.elasticsearch with traffic_logcat sucessfully
        #print("Inserting...")
        indexPrepare()
        indexBulkData()


