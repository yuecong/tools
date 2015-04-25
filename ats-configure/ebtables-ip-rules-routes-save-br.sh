#! /bin/bash

sleep 20

ebtables -t broute -F
ebtables -t filter --flush FORWARD
ebtables -t filter --flush INPUT

ebtables -t broute -A BROUTING -p IPv4 --ip-proto tcp --ip-dport 80 -j redirect --redirect-target DROP
ebtables -t broute -A BROUTING -p IPv4 --ip-proto tcp --ip-sport 80 -j redirect --redirect-target DROP

iptables -t filter --flush FORWARD
iptables -t filter --flush INPUT

iptables -t mangle -A PREROUTING -i eth1 -p tcp -m tcp --dport 80 -j TPROXY --on-ip 0.0.0.0 --on-port 8080 --tproxy-mark 1/1
iptables -t mangle -A PREROUTING -i eth0 -p tcp -m tcp --sport 80 -j MARK --set-mark 1/1

ip route add local 0.0.0.0/0 dev lo table 1
ip rule add dev lo fwmark 1/1 table 1

ip rule add dev eth0 fwmark 1/1 lookup 1
ip rule add dev eth1 fwmark 1/1 lookup 1

sleep 10

/usr/local/bin/trafficserver start
