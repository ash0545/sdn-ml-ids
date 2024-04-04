### sdn-ml-ids
# SDN Emulation and Development of Dataset for ML-Based Intrusion Detection
Project work done for the **IP1202** course of our 4th Semester

**Reference Paper**: [MCAD: A Machine Learning Based Cyberattacks Detector in Software-Defined Networking (SDN) for Healthcare Systems](https://ieeexplore.ieee.org/document/10101795)


### Team Members:
 - Ashwin Santhosh (CS22B1005, GitHub: [ash0545](https://www.github.com/ash0545))
 - Aswin Valsaraj (CS22B1006, GitHub: [aswinn03](https://www.github.com/aswinn03))
 - Kaustub Pavagada (CS22B1042, GitHub: [Kaustub26Pvgda](https://www.github.com/Kaustub26Pvgda))

# Project Overview
## Aim
  Our overall goal was to delve into the creation of SDN Topologies through the use of the Ryu SDN Framework, and the collection of flow statistics through it's inbuilt APIs. Through this, we simulated attack and normal traffic flows within our emulated network to make a dataset, which can be used to train a Machine Learning (ML) based Intrusion Detection System (IDS).
  
  In short: **To strengthen security in SDNs by creating a dataset for an ML-based IDS present within the controller.**

## Tools / Libraries Used
 - [Ryu SDN Framework](https://ryu-sdn.org/) : for the control plane of our simulated network
 - [Mininet](http://mininet.org/) : creation of virtual network
 - [Scapy](https://scapy.net/) : packet manipulation python library for simulating attacks
 - [Wireshark](https://www.wireshark.org/) : to verify functionality of attack / normal flow simulation
 - [Nmap](https://nmap.org/) : network discovery tool, to simulate a probe attack
 - [w3m](https://w3m.sourceforge.net/) : text-based web browser for use in terminals, to simulate normal traffic flow
 - [iPerf](https://iperf.fr/) : for network performance measurement, to simulate normal traffic flow

## Topology
![image](https://github.com/ash0545/sdn-ml-ids/assets/112403369/beba11d3-71fa-47e0-9f9b-4656ba078559)

## Implementation
### Attack Flow
 - Scapy Attacks :
   - TCP, UDP, ICMP Flood Attacks
   - Nestea Attack
   - LAND Attack (Windows)
   - Malformed Packet Attack
   - Ping of Death Attack
 - Nmap : scan IP Address, service name, operating system and port
### Normal Flow
 - w3m was used to routinely access common websites within 2 Mininet hosts
 - Iperf was used between 2 Mininet hosts as well
### Dataset Collection
 - Ryu's ofctl_rest, a built in application providing REST APIs for retrieving various statistics was used alongside our controller
 - The controller periodically sends requests to this API to collect all relevant statistics
 - 24 features were retrieved through this process

![image](https://github.com/ash0545/sdn-ml-ids/assets/112403369/7a981481-853b-4006-ba98-2c36be574535)

### Model Development
 - Following our reference paper, division transformation was used to extract 13 new complex features from existing raw ones. These new features are given below:

![image](https://github.com/ash0545/sdn-ml-ids/assets/112403369/40db3f9f-99f1-4ca6-b211-9e7ad6673195)
 - This data was then cleaned and normalized using Robust Scaling
 - Principal Component Analysis (PCA) was used for dimensionality reduction (to 5 features)
 - This processed dataset was then used to train a Random Forest model
   - Accuracy without PCA : 88.3%
   - Accuracy with PCA : 99.8%

## Future Work
 - Imbalance in training data (4x more attack data than normal) is to be reduced, as current model appears to be overfitted to attack flows
 - Implementation of a _functional_ IDS and Intrusion Prevention System (IPS)
 - Test out Deep Learning (DL) models
 - Emulate more complex topologies by connecting multiple Virtual Machines (VMs), each on separate networks

# Helpful Links
 - Connecting Mininet hosts to VM's network interface for access to the internet : https://gist.github.com/shreyakupadhyay/84dc75607ec1078aca3129c8958f3683
> [!NOTE]
> If getting 'unknown host' errors when trying to access websites, the DNS nameserver will have to be configured. This can be done through the following command within the xterm window of the host under consideration: `echo 'nameserver 8.8.8.8' | tee /etc/resolv.conf`
 - Ryu's ofctl_rest API documentation : https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#ryu-app-ofctl-rest
 - Classical attacks of Scapy : https://scapy.readthedocs.io/en/latest/usage.html#classical-attacks
