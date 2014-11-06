#!/usr/bin/python
import commands
counter =0
while counter <=100 :
  (stauts,output) = commands.getstatusoutput("/usr/local/bin/aws ec2 describe-addresses ")
  if len(output) > 5 :
    print output
    break;
  #alocate new Elastic IP, and get the allocation id and allocated ip
  (stauts,output) = commands.getstatusoutput("/usr/local/bin/aws ec2 allocate-address")
  allocation_id = output.split('\t') [0]
  new_gip =  output.split('\t') [2]

  #Sleep for 2 seconds
  (status,output) = commands.getstatusoutput("/bin/sleep 2")

  #associate the allocated ip to indicated ec2 instance
  (status,output) = commands.getstatusoutput("/usr/local/bin/aws ec2 associate-address --instance-id i-9afe2b90 --allocation-id "+allocation_id)
  print status,output
  association_id = output;

  #Sleep for 3 seconds
  (status,output) = commands.getstatusoutput("/bin/sleep 5")
 
  #click the URL!!
  (status,output) = commands.getstatusoutput("/usr/bin/wget http://star.sznsibi.org/vote.ashx?id=2560")
  print counter, new_gip
  #Sleep for 2 seconds
  (status,output) = commands.getstatusoutput("/bin/sleep 10")

  #Disassociate Elastic IP address
  (status,output) = commands.getstatusoutput("/usr/local/bin/aws ec2 disassociate-address --association-id " + association_id)

  #Sleep for 3 seconds
  (status,output) = commands.getstatusoutput("/bin/sleep 3")

  #release allocated Elastic IP
  (status,output) = commands.getstatusoutput("/usr/local/bin/aws ec2 release-address --allocation-id " + allocation_id)
  
  #Sleep for 3 seconds
  (status,output) = commands.getstatusoutput("/bin/sleep 3")

  counter +=1

