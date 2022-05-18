# Building a Wi-Fi scanner in Python using Scapy that finds and displays 
# available nearby wireless networks and their MAC address, dBm signal, 
# channel and encryption type.
from scapy.all import *
from threading import Thread
import pandas as pd
import time
import os

# initialize the networks dataframe that will contain all access points nearby
networks = pd.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])

# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    # extract the MAC addres of the network
    bssid = packet[Dot11].addr2

    # get the name of it
    ssid = packet[Dot11Elt].info.decode()

    try:
        dbm_signal = packet.dBm_AntSignal
    except:
        dbm_signal = 'N/A'
    
    # extract network stats
    stats = packet[Dot11BEacon].network_stats()

    # get the channel of the AP
    channel = stats.get('channel')

    # get the crypto
    crypto = stats.get('crypto')

    networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    while True:
        os.system('clear')
        print(networks)
        time.sleep(0.5)


if __name__ == "__main__":
    # interface name, check using iwconfig
    interface = "wlan0mon"
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)