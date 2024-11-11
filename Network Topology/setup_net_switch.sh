#!/bin/bash

# To be run BEFORE connecting a host (Host1 in the case of our topology)
# connected to this switch (S1 in this case) to the internet. The port
# should be the port connected to the NAT adapter (enp0s3 in our case -
# can be checked by comparing MAC address from ifconfig and the VM's 
# network settings).

sudo ovs-vsctl add-port S1 enp0s3
sudo dhclient S1



