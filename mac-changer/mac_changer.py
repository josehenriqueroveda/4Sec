import logging
import random
import re
import string
import argparse
import subprocess


MAC_ADDRESS_LENGTH = 17
VALID_SECOND_CHARACTERS = "02468ACE"


def get_random_mac() -> str:
    """Generate and return a random MAC address in Linux format."""
    upper_hex = "".join(set(string.hexdigits.upper()))
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice(VALID_SECOND_CHARACTERS)
            else:
                mac += random.choice(upper_hex)
        mac += ":"
    return mac.strip(":")


def get_current_mac(iface: str) -> str:
    """Get the current MAC address of the specified network interface."""
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()


def change_mac(iface: str, new_mac: str) -> None:
    """Change the MAC address of the specified network interface."""
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac}", shell=True)
    subprocess.check_output(f"ifconfig {iface} up", shell=True)


def main() -> None:
    """Parse command-line arguments and change the MAC address."""
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Python MAC changer for Linux")
    parser.add_argument("interface", help="The network interface name on Linux")
    parser.add_argument(
        "-r", "--random", action="store_true", help="To generate a random MAC"
    )
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    iface = args.interface
    if args.random:
        new_mac = get_random_mac()
    elif args.mac:
        new_mac = args.mac
    else:
        logging.error("Either --random or --mac must be specified")
        return
    old_mac = get_current_mac(iface)
    logging.info(f"Old MAC Address: {old_mac}")
    change_mac(iface, new_mac)
    new_mac = get_current_mac(iface)
    if new_mac == old_mac:
        logging.error("Failed to change MAC address")
    else:
        logging.info(f"New MAC Address: {new_mac}")


if __name__ == "__main__":
    main()
