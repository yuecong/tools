import psutil
import time,datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def cpu_info():
	psutil.cpu_percent()
	time.sleep(1) 
	return psutil.cpu_percent()

def mem_info():
	return psutil.virtual_memory().percent

def network_info():
	start_network_info = psutil.net_io_counters()
	time.sleep(1) #1 seconds
	end_network_info = psutil.net_io_counters()
	Bps_sent = int(end_network_info.bytes_sent - start_network_info.bytes_sent) 
	Bps_rcv = int(end_network_info.bytes_recv - start_network_info.bytes_recv )
	return [Bps_sent,Bps_rcv]

def indexPrepare():
	request_body = {
		"settings" : {
		"number_of_shards": 5,
		"number_of_replicas": 0}
	}

	if not es.indices.exists(INDEX_NAME):
		print("creating '%s' index..." % (INDEX_NAME))
		res = es.indices.create(index = INDEX_NAME, body = request_body)
		print(" response: '%s'" % (res))

#Main function  
POLL_INTERVAL= 3; # 3+2 5 seconds
#ES information
ES_HOST = {
"host" : "10.0.0.158", 
"port" : 9200
}
INDEX_NAME = 'ats_sysinfo'
TYPE_NAME = 'systeminfo'
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

if __name__ == '__main__':
	indexPrepare();
	while (True):
		cpuInfo = int(cpu_info())
		memInfo = int(mem_info())
		networkInfo = network_info()
		timeStamp= st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ') #2015-02-19T14:59:03Z
		#print(timeStamp,"CPU:",cpuInfo,"Memmory:",memInfo,"networkInfo_sent(bytes):",networkInfo[0],"networkInfo_rcv(bytes):",networkInfo[1])
		bulk_data = []
		data= {"_index": INDEX_NAME, "_type": TYPE_NAME, 
		  "_source": {"timeStamp":timeStamp,"cpu":cpuInfo,"memory":memInfo,"Bps_sent":networkInfo[0],"Bps_rcv":networkInfo[1]}}
		bulk_data.append(data)
		res = helpers.bulk(es,bulk_data)
		es.indices.refresh()
		time.sleep(POLL_INTERVAL)