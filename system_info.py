import psutil
import time,datetime

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

POLL_INTERVAL= 3; # 3+2 5 seconds
#Main function    
if __name__ == '__main__':
	while (True):
		cpuInfo = int(cpu_info())
		memInfo = int(mem_info())
		networkInfo = network_info()
		timeStamp= st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ') #2015-02-19T14:59:03Z
		print(timeStamp,"CPU:",cpuInfo,"Memmory:",memInfo,"networkInfo_sent(bytes):",networkInfo[0],"networkInfo_rcv(bytes):",networkInfo[1])
		time.sleep(POLL_INTERVAL)