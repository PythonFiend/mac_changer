#!/usr/bin/env python

import subprocess
import optparse
import random
import string
import re

#Creates a parser object that handles user input from command line
def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Choose interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Choose new MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("""[-] Missing interface
                            Use --help for more info""")
    if not options.new_mac:
        parser.error("""[-] Missing MAC address
                            Use --help for more info""")
    return options

#Changes MAC address
def change_mac(interface, new_mac):
    print(f"[+] Trying to change {interface}'s old MAC address to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    #Prints ifconfig info
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    #Filters out MAC address from ifconfig output (pythex.org)
    mac_search_res = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode())

    #Outputs filtered MAC address, or absence thereof
    if mac_search_res:
       return mac_search_res.group(0)
    else:
        return "[-] MAC address not found!"


options = get_args()
current_mac = get_current_mac(options.interface)
print("Current MAC: " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] New MAC changed to" + current_mac)
else:
    print("[-] MAC address not changed")

