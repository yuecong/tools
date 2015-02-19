#!/usr/bin/python
import psutil
import subprocess
import simplejson
import time
import random
import multiprocessing as mp

procs_id = 0
procs = {}
procs_data = []
url_num = 0

# Define an output queue
output = mp.Queue()

MAX_THREAD_NUM = 700

proxy_url='10.0.0.204:80'
urls = [
     'http://drbd.linbit.com/home/what-is-drbd/',
     'http://drbd.linbit.com/home/what-is-ha/',
     'http://en.wikipedia.org/wiki/Main_Page',
     'http://en.wikipedia.org/wiki/Walden%E2%80%93Wallkill_Rail_Trail',
     'http://en.wikipedia.org/wiki/New_York_metropolitan_area',
     'http://www.citrix.com/products.html',
     'http://www.citrix.co.jp/products.html?posit=glnav',
     'http://www.citrix.co.jp/products/gotowebinar/overview.html'
    ]

#Get http access time for particular url with/without proxy
def getInfoForCurl(url,proxy=''):
    start_time = time.time()
    if len(proxy) >0:
        cmd = ['curl','--proxy',proxy,url]
    else:
        cmd = ['curl',url]
    runCommand(cmd, return_stdout = False, busy_wait = True)
    end_time = time.time()
    return [url,proxy,end_time - start_time]

def accesswithOutput(proxyUrl):
    for x in range(5):
        info = getInfoForCurl(random.choice(urls),proxyUrl)
    output.put(info)
    #url_num = url_num + 1
    print (info)



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
                data = proc.as_dict(attrs = ['get_io_counters', 'get_cpu_times'])
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

#Main function    
if __name__ == '__main__':
    #warmup for ATS
    print ("warmup start....")
    for url in urls:
        getInfoForCurl(url,proxy_url)

    print ("test start....")
    # Setup a list of processes that we want to run
    print "add it into thead queue...."
    processes = [mp.Process(target=accesswithOutput, args=(proxy_url,)) for x in range(MAX_THREAD_NUM)]
    #processes = [mp.Process(target=accesswithOutput, args=('',)) for x in range(MAX_THREAD_NUM)]
    # Run processes
    print "thread start..."
    for p in processes:
        p.start()
    # Exit the completed processes    
    for p in processes:
        p.join()
    print "thread exit!"
    # Get process results from the output queue
    results = [output.get() for p in processes]
    time_sum=0
    for result in results:
        time_sum =time_sum + result[2]

    print(time_sum)

#    for url in urls:
#        info= getInfoForCurl(url,proxy_url)
#        print (info)
#        info= getInfoForCurl(url)
#        print (info)

