#!/bin/bash

# To be run within the XTerm window of the host (Host1 in this case)
# which is to be connected to the internet. This is to be done AFTER
# enabling internet access for the switch this host is connected to.

sudo ifconfig Host1-eth0 0
sudo dhclient Host1-eth0

# DNS server configured to allow for domain name resolution, enabling access to URLs.
echo "nameserver 8.8.8.8" | tee /etc/resolv.conf
