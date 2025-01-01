## ARP Spoofing Script

This Python script performs ARP spoofing, intercepting and manipulating network traffic between a target machine and the gateway. The script is based on concepts learned in the Udemy course "Learn Python & Ethical Hacking From Scratch" by z Security.

### Prerequisites

Make sure you have the following dependencies installed:
- Python 3.x Or 2.x
- scapy

To install `scapy`, run:
```bash
pip install scapy
```

### Usage

Run the script with the following command:
```bash
#! /usr/bin/env python
# import sys
python3 arp_spoof.py -t <target_ip> -g <gateway_ip>
```
- `-t` or `--target`: IP address of the target machine.
- `-g` or `--gateway`: IP address of the router.

### Description

The script does the following:
1. Takes target and gateway IP addresses as input arguments.
2. Fetches the MAC addresses of both the target and gateway using ARP requests.
3. Spoofs the ARP table by sending ARP packets to both the target and gateway, making them believe that the attacker's machine is the other device.
4. Continuously sends ARP packets to maintain the spoofing.
5. Restores the ARP tables of the target and gateway upon interrupt.

### Functions

- `get_arguments()`: Parses command-line arguments.
- `get_mac(ip)`: Retrieves the MAC address of a given IP.
- `spoof(target_ip, spoof_ip)`: Sends spoofed ARP packets to the target and gateway.
- `restore(des_ip, sou_ip)`: Restores the ARP tables of the target and gateway.
