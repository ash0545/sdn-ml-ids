# Normal Traffic Generation

This section contains the scripts to generate the various types of network normal traffic.

## Table of Contents

- [Normal Traffic Generation](#normal-traffic-generation)
  - [Table of Contents](#table-of-contents)
  - [Generated Normal Classes](#generated-normal-classes)
  - [Normal Classes and Tools](#normal-classes-and-tools)
  - [Provided Files](#provided-files)
  - [Usage Instructions](#usage-instructions)

## Generated Normal Classes

- iPerf
- Internet
- Ping
- Telnet
- DNS

## Normal Classes and Tools

1. **iPerf Traffic**
   - **Tool**: [IPerf](https://iperf.fr/)
   - **Description**: iPerf3 is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, buffers and protocols (TCP, UDP, SCTP with IPv4 and IPv6). For each test it reports the bandwidth, loss, and other parameters.
   - **Commands Used**:
       + For the server host: `iperf -s`
       + For the client hosts: `iperf -c <host-ip> -t 10000 -i 1`  
         This makes sure the command runs for long enough to collect the required dataset. The iPerf reports are sent every second using the `-i` flag

2. **Internet Traffic**
   - **Tool**: [w3m](https://w3m.sourceforge.net/)
   - **Description**: A list of websites were compiled into a single text file and a Python script was made to iterate through the list and visit the websites using w3m, a command-line browser. These packets are collected as the internet traffic dataset.
   - **Files**: Check the [provided files](#provided-files) section

3. **Ping Traffic**
   - **Tool**: Python scripting
   - **Description**: The `ping` command was used within a Python script to ping between the hosts and collect packet features.
   - **Files**: Check the [provided files](#provided-files) section

4. **Telnet Traffic**
   - **Tool**: [D-ITG](https://traffic.comics.unina.it/software/ITG/documentation.php)
   - **Description**: D-ITG (Distributed Internet Traffic Generator) is a tool that generates network traffic by accurately simulating how data packets are sent and their sizes. It uses different statistical models (like exponential, uniform, normal, and others) to mimic real-world patterns of packet timing and sizes.
   - **Commands Used**:
       + For the receiver host: `./ITGRecv`
       + For the sender host: `./ITGSend Telnet -a <receiver-ip> -t 150000`

> [!NOTE]
> Make sure D-ITG is installed in your project directory and the terminal is open in the bin folder of the installed D-ITG directory!

5. **DNS Traffic**
   - **Tool**: [D-ITG](https://traffic.comics.unina.it/software/ITG/documentation.php)
   - **Commands Used**:
       + For the receiver host: `./ITGRecv`
       + For the sender host: `./ITGSend DNS -a <receiver-ip> -t 150000`
  
## Provided Files

- Internet
  - **websites.txt**: Website list for simulating internet access.
  - **w3m_traffic_script.sh**: Script to access a website from `websites.txt` every 5 seconds.

- Ping
  - ****:

## Usage Instructions

1. Setup your Mininet topology and ensure the internet connection is setup and working, and ensure the hosts can ping among each other. This can be verified by visiting a website on xterm using w3m and pinging between your Mininet Hosts respectively.
2. Ensure all necessary tools / packages are installed:
   - [IPerf](https://iperf.fr/)
   - [w3m](https://w3m.sourceforge.net/)
   - [D-ITG](https://traffic.comics.unina.it/software/ITG/documentation.php)
   - [Python 2.7](https://www.python.org/)
3. Follow each script's comments for specific configurations, such as target IP addresses and network interface settings.
4. Run the scripts / commands in their respective VMs / Mininet Hosts.
