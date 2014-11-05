#!/usr/bin/python
import commands
counter =0
while counter <=100 :
  #alocate new Elastic IP, and get the allocation id
  (stauts,output) = commands.getstatusoutput("aws ec2 allocate-address")
  allocation_id = output.split('\t') [0]

  #associate the allocated ip to indicated ec2 instance
  (status,output) = commands.getstatusoutput("aws ec2 associate-address --instance-id i-9afe2b90 --allocation-id "+allocation_id)

  #Sleep for 3 seconds
  (status,output) = commands.getstatusoutput("sleep 3")
 
 #click the URL!!
 (status,output) = commands.getstatusoutput("wget http://star.sznsibi.org/vote.ashx?id=2560")
  #Sleep for 2 seconds
  (status,output) = commands.getstatusoutput("sleep 2")

  #release allocated Elastic IP
  (status,output) = commands.getstatusoutput("aws ec2 release-address --allocation-id " + allocation_id)
  counter +=1
  print counter

