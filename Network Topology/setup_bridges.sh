#!/bin/bash

# To be run BEFORE configuring the Kali and Metasploitable VMs. 

# Deleting any previous bridges of the same name.
sudo ovs-vsctl del-br br0
sudo ovs-vsctl del-br br1

sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-br br1

# In this case, br0 is connected to the port enp0s8, which is in turn connected via VirtualBox to the Host-only network
# with the Kali VM. The same applies to br1, enp0s9 and the Metasploitable VM.
sudo ovs-vsctl add-port br0 enp0s8
sudo ovs-vsctl add-port br1 enp0s9

sudo ip addr add 192.168.56.200/24 dev br0
sudo ip addr add 192.168.21.200/24 dev br1

# Enabling IP Forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# The actual Linux Routing taking place.
sudo ip route add 192.168.56.0/24 via 192.168.21.2
sudo ip route add 192.168.21.0/24 via 192.168.56.2

sudo ip link set dev br0 up
sudo ip link set dev br1 up

# Assigning the created bridges to the Ryu Controller.
sudo ovs-vsctl set-controller br0 tcp:0.0.0.0:6633
sudo ovs-vsctl set-controller br1 tcp:0.0.0.0:6633
