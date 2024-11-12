# Attack Traffic Generation

This section contains the scripts to generate the various types of network attack traffic.

## Table of Contents

- [Attack Traffic Generation](#attack-traffic-generation)
  - [Table of Contents](#table-of-contents)
  - [Generated Attack Classes](#generated-attack-classes)
  - [Attack Classes and Tools](#attack-classes-and-tools)
  - [Provided Files](#provided-files)
  - [Usage Instructions](#usage-instructions)

## Generated Attack Classes

| Classes of Attack | Impacted Location on SDN                            | Attack Type                                                                  | Tool(s)                           | Intruder Machine                               | Victim                                                     |
| ----------------- | --------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| DDoS              | • Application Plane<br>• Controller<br>• Data Plane | TCP Flood, UDP Flood, ICMP Flood                                             | Scapy                             | Mininet Host:10.0.0.2<br>Mininet Host:10.0.0.3 | Mininet Host:10.0.0.1                                      |
| Probe             | • Application Plane<br>• Controller<br>• Data Plane | Network discovery (scan IP Address, service name, operating system and port) | Nmap                              | Kali Linux VM: 192.168.56.101                  | Metasploitable 2 server VM 192.168.21.3                    |
| Web Attacks       | • Application Plane                                 | SQL Injection, Cross Site Scripting (XSS)                                    | Selenium                          | Kali Linux VM: 192.168.56.101                  | Metasploitable 2 server VM Web server (DVWA): 192.168.21.3 |
| R2L               | • Application Plane<br>• Controller<br>• Data Plane | Brute Force Attack, CMD, File upload                                         | Selenium                          | Kali Linux VM: 192.168.56.101                  | Metasploitable 2 server VM Web server (DVWA): 192.168.21.3 |
| U2R               | • Application Plane<br>• Controller<br>• Data Plane | Exploit VNC port 5900, Samba Server                                          | Metasploit framework (msfconsole) | Kali Linux VM: 192.168.56.101                  | Metasploitable 2 server VM 192.168.21.3                    |

## Attack Classes and Tools

1. **DDoS Attacks**
   - **Tool**: [Scapy](https://scapy.net/)
   - **Description**: Scapy is used to generate TCP, UDP, and ICMP flood attacks by forging packets with randomized source IPs targeting selected victims. Packets are sent asynchronously for a continuous attack simulation.

2. **Probe Attacks**
   - **Tool**: [Nmap](https://nmap.org/)
   - **Description**: Nmap is used to scan a target for open ports, services, and OS details. The gathered data simulates probe attacks, where network information is collected for potential exploitation.
   - **Command Used**: `nmap <victim-ip> -sV -O -p`

3. **Web and R2L (Remote-to-Local) Attacks**
   - **Tools**: [Selenium](https://www.selenium.dev/), [Damn Vulnerable Web Application (DVWA)](https://github.com/digininja/DVWA)
   - **Description**: Selenium automates web interactions on the DVWA to generate:
     - **SQL Injection (SQLi)**: Manipulates SQL queries to access unauthorized data.
     - **Cross-Site Scripting (XSS)**: Injects scripts into web pages viewed by others.
     - **Command Injection (CMD)**: Executes unauthorized commands on the server.
     - **File Upload Vulnerability**: Uploads a malicious PHP script instead of an image.
     - **Brute Force Attack**: Tries multiple passwords using a list of common passwords.

4. **U2R (User-to-Root) Attacks**
   - **Tool**: [Metasploit Framework](https://www.metasploit.com/)
   - **Description**: Metasploit is used to exploit Samba and VNC vulnerabilities in Metasploitable VM to gain root access, simulating privilege escalation attacks.

## Provided Files

- DDoS
  - **ddos_tcp_udp_icmp.py**: Script to generate DDoS traffic using Scapy.
- Web
  - **web_reflected_xss.py**: Script for XSS attacks.
  - **web_sql_injection.py**: Script for SQL injection attacks.

> [!NOTE]
> The Probe attack uses only the single command mentioned in the [previous section](#attack-classes-and-tools).

- R2L
  - **r2l_brute_force.py**: Script for brute force login attempts.
  - **r2l_cmd_injection.py**: Script for command injection attack.
  - **r2l_file_upload.py**: Script for file upload attack.
  - **10-million-password-list-top-100000.txt**: Password list for brute force attacks.
  - **malicious.php**: Malicious PHP file used for file upload vulnerability.

- U2R
  > [!IMPORTANT]
  > All msf scripts require configuration with the MSFRPCD utility for proper functioning. Details are provided as comments within the scripts.
  - **u2r_msf_samba.py**: Metasploit script for Samba vulnerability exploitation.
  - **u2r_msf_vnc.py**: Metasploit script for VNC vulnerability exploitation.

## Usage Instructions

1. Setup your topology and ensure everything is connected and working. This can be verified by pinging between your VMs / Mininet Hosts and / or using Wireshark to listen to bridges.
2. Ensure all necessary tools / packages are installed:
   - [Scapy](https://scapy.net/)
   - [Nmap](https://nmap.org/)
   - [Selenium](https://www.selenium.dev/)
3. Follow each script's comments for specific configurations, such as target IP addresses and network interface settings.
4. Run the scripts in their respective VMs / Mininet Hosts - refer the [table](#generated-attack-classes) given above.
