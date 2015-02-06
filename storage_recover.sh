#!/bin/sh
#start glusterfsd deamon forcely
service glusterfsd start
 
#mount all target again
mount -a

#print mount information
echo "--Confirm sdc,sdd and gluster are mounted correctly!!--"
mount
 
#config iscsi target
tgtadm --lld iscsi --op new --mode target --tid 1 -T iqn.2015-02.ati.ethergrid:ssd.gluster
tgtadm --lld iscsi --op show --mode target
tgtadm --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b /mnt/gluster-ssd/fs.iscsi.ssd1.sdc.200G
tgtadm --lld iscsi --op bind --mode target --tid 1 -I ALL
tgtadm --lld iscsi --op show --mode target
 
#Tune I/O schedule inside linux kernel for SSD/SATA
echo noop >/sys/block/sda/queue/scheduler
echo noop >/sys/block/sdb/queue/scheduler
echo noop >/sys/block/sdc/queue/scheduler
echo cfq >/sys/block/sdd/queue/scheduler
echo cfq >/sys/block/sde/queue/scheduler
                                                 
