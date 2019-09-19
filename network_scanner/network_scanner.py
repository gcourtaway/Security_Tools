#!/usr/bin/env python

#instead of typing scapy.all.[function] can just type scapy.function
import scapy.all as scapy
import argparse #python3 optparse, optparse still works python3

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip", help="Target IP/IPs")
    options = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please specify an IP or IP range")
    return options

def scan(ip):
    #discovers clients on same network using arp, can take netmask
    #scapy.arping(ip) will do everything this program does

    #run scapy.ls on scapy.ARP to get a list of all the fields you can set like pdst
    arp_request = scapy.ARP(pdst=ip)
    #set broadcast mac to this mac, ff.. is every mac
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy allows you to combine packets in this way
    arp_request_broadcast = broadcast/arp_request
    #send and recieve (with added ether layer otherwise use scapy.sr) stored in 2 vars but 0 makes it store 1
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_lists):
    print("IP\t\t\tMAC Address\n--------------------------------------------")
    for client in results_lists:
        print(client["ip"] + "\t\t" + client["mac"])


target_ip = parse_arg()
scan_result = scan(target_ip.ip)
print_result(scan_result)