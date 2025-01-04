# Network Topology

This section details how to setup the entirety of our topology.  The controller file can be taken from the [Ryu Controller](../Dataset%20Collection/) subdirectory. The steps below can be modified to build a custom topology for any other particular use case.

The script files provided can be used to speed up the setup of the topology. It is recommended to automate the setup of your custom topology using scripts.

## Table of Contents

- [Network Topology](#network-topology)
  - [Table of Contents](#table-of-contents)
  - [Creating the Topology in VirtualBox](#creating-the-topology-in-virtualbox)
  - [Configuring the Ubuntu VM and Mininet](#configuring-the-ubuntu-vm-and-mininet)
  - [Connecting a Mininet host to the internet](#connecting-a-mininet-host-to-the-internet)
  - [Connecting the Kali and Metasploitable VMs - Linux Routing through the Ubuntu VM](#connecting-the-kali-and-metasploitable-vms---linux-routing-through-the-ubuntu-vm)
  - [Configuring the Kali and Metasploitable VMs](#configuring-the-kali-and-metasploitable-vms)
  - [Helpful Links](#helpful-links)

## Creating the Topology in VirtualBox

- Create the Kali, Ubuntu and Metasploitable VMs.

- The Kali and Metasploitable VMs' network adapters are connected to 2 separate [Host-Only networks](https://www.virtualbox.org/manual/ch06.html#network_hostonly).

- For the Ubuntu VM, one network adapter is connected to the Kali Host-Only network, and the other to the Metasploitable one.

- VMs requiring access to the internet are attached with a NAT adapter.

## Configuring the Ubuntu VM and Mininet

- Install the required packages within Ubuntu: `sudo apt install python-ryu mininet xterm`

- Run the Ryu controller Python file through ryu-manager: `ryu-manager <file.py>`

- Any packages/tools that are to be used within Mininet can be installed in the Ubuntu VM itself - Mininet hosts have access to all commands and the filesystem of the underlying OS.

- Start the Mininet topology and use XTerm to access a particular host’s shell: `sudo python <file.py>`

## Connecting a Mininet host to the internet

- Ensure the Mininet switch is up: `sudo ifconfig <switch-name>`

- Add the NAT port (which is providing internet access to Ubuntu) to the switch: `sudo ovs-vsctl add-port <switch-name> enp0sx`

- Assign an IP to the switch through DHCP: `sudo dhclient <switch-name>`

- Within a Mininet host (connected to the above switch) which is to be connected to the internet:

  - Clear adapter’s config: `sudo ifconfig <host-name>-eth0 0`

  - Assign an IP through DHCP: `sudo dhclient <host-name>-eth0`

  - Add a DNS for accessing common URLs: `echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf`

## Connecting the Kali and Metasploitable VMs - Linux Routing through the Ubuntu VM

- Create the OVS bridges using `sudo ovs-vsctl add-br <bridge name>`

- Connect these bridges to the adapters: `sudo ovs-vsctl add-port <bridge name> <enp0sx>`

- Give IP Addresses to these bridges within the same IP range of the respective VM's host-only network: `sudo ip addr add <ip range> dev <bridge name>`

- IP Forwarding is required as well: `sudo sysctl -w net.ipv4.ip_forward=1`

- Add the Linux routing: `sudo ip route add <ip range> via <ip>`

- Enable the bridges: `sudo ip link set dev <bridge name> up`

## Configuring the Kali and Metasploitable VMs

- For Metasploitable - receive an IP through DHCP: `sudo dhclient eth0`

- Add default routes within the Kali and Metasploitable VMs (to their respective bridges): `route add default gw <bridge ip>`

## Helpful Links

- VirtualBox Virtual Networking Manual - <https://www.virtualbox.org/manual/ch06.html>
- Connecting a Mininet host to the internet - <https://gist.github.com/shreyakupadhyay/84dc75607ec1078aca3129c8958f3683>

> [!NOTE]
> If getting 'unknown host' errors when trying to access websites, the DNS nameserver will have to be configured. This can be done through the following command within the xterm window of the host under consideration: `echo 'nameserver 8.8.8.8' | tee /etc/resolv.conf`

- Converting a switch to Layer 3 - <https://github.com/knetsolutions/learn-sdn-with-ryu/blob/master/ryu_part3.md>
