#!/bin/sh

#IP=$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -f1 -d'/');
IP=10.0.0.229
sed -i "s/\[MY_IP_ADDR\]/$IP/g" /etc/kamailio/kamctlrc;
sed -i "s/\[MY_IP_ADDR\]/$IP/g" /etc/kamailio/kamailio.cfg;
