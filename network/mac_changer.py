import subprocess
import string
import random
import re


# Making a function to generate and return a MAC address (Linux format)
def get_random_mac():
    # get hexadecimal digits used in MAC address
    upper_hex = ''.join(set(string.hexdigits.upper()))
    # Second character must be 0, 2, 4, 6, 8, A, C or E
    mac = ''
    for i in range(6):
        for j in range(2):
            if i == 0:
                # sample one of these characters
                mac += random.choice('02468ACE')
            else:
                mac += random.choice(upper_hex)
        mac += ':'
    return mac.strip(':')


# Making a function to get the current MAC address of the machine
def get_current_mac(iface):
    # Using 'ifconfig' to get the interface details
    # runs command in default shell
    output = subprocess.check_output(f'ifconfig {iface}', shell=True).decode()
    # locate the MAC address after the 'ether' word
    return re.search('ether (.+) ', output).group().split()[1].strip()


# Making a function to change the MAC address
def change_mac(iface, new_mac):
    # disable network interface
    subprocess.check_output(f'ifconfig {iface} down', shell=True)
    # change MAC
    subprocess.check_output(f'ifconfig {iface} hw ether {new_mac}', shell=True)
    # enable network interface again
    subprocess.check_output(f'ifconfig {iface} up', shell=True)


# Using the 'argparse' module to wrap the script
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Python MAC changer for Linux')
    parser.add_argument(
        'interface', help='The network interface name on Linux')
    parser.add_argument('-r', '--random', action='store_true',
                        help='To generate a random MAC')
    parser.add_argument(
        '-m', '--mac', help='The new MAC you want to change to')
    args = parser.parse_args()
    iface = args.interface
    if args.random:
        # Random parameter is set: generate a random MAC
        new_mac = get_random_mac()
    elif args.mac:
        # MAC is set: use it instead
        new_mac = args.mac
    # get current MAC
    old_mac = get_current_mac(iface)
    print('[*] Old MAC Address: ', old_mac)
    # change the MAC address
    change_mac(iface, new_mac)
    # check if it changed
    print('[+] New MAC Address: ', new_mac)