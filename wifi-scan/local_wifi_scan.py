"""
This script scans for nearby Wi-Fi networks and displays their information.
"""

import logging
import os
import time
from threading import Thread

import pandas as pd
from scapy.all import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NETWORKS = pd.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
NETWORKS.set_index("BSSID", inplace=True)


def callback(packet):
    """
    Extracts information about a Wi-Fi network from a packet and adds it to the NETWORKS dataframe.
    """
    bssid = packet[Dot11].addr2
    ssid = packet[Dot11Elt].info.decode()
    try:
        dbm_signal = packet.dBm_AntSignal
    except AttributeError:
        dbm_signal = "N/A"
    stats = packet[Dot11Beacon].network_stats()
    channel = stats.get("channel")
    crypto = stats.get("crypto")
    NETWORKS.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    """
    Prints the NETWORKS dataframe to the console every 0.5 seconds.
    """
    while True:
        os.system("clear")
        logger.info(NETWORKS)
        time.sleep(0.5)


def main():
    """
    Runs the Wi-Fi scanner.
    """
    interface = "wlan0mon"
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    sniff(prn=callback, iface=interface)


if __name__ == "__main__":
    main()
