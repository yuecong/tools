#!/bin/sh
cd /root/
yum install gcc gcc-c++ pkgconfig pcre-devel tcl-devel expat-devel 
yum install perl-ExtUtils-MakeMaker
yum install libunwind libunwind-devel
yum install autoconf automake libtool
yum install openssl-devel.x86_64
yum install git
yum install wget
wget http://mirror.cogentco.com/pub/apache/trafficserver/trafficserver-5.2.0.tar.bz2
tar -xf /root/trafficserver-5.2.0.tar.bz2 
cd /root/trafficserver-5.2.0
./configure 
make
make install
#Disable iptables to make 80 can be accessable
/etc/init.d/iptables stop
/etc/init.d/iptables save
