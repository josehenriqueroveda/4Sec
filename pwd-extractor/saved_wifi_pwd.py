import os
import re
import subprocess
from collections import namedtuple
from dotenv import load_dotenv


load_dotenv()


def get_windows_ssids():
    """Returns a list of saved SSIDs on Windows"""
    output = subprocess.check_output("netsh wlan show profiles").decode()
    profiles = re.findall(r"All User Profile\s(.*)", output)
    ssids = [profile.strip().strip(":").strip() for profile in profiles]
    return ssids


def get_windows_saved_pwds(verbose=1):
    """Extracts saved Wi-Fi passwords saved in a Windows machine, this function extracts data using netsh
    command in Windows
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "ciphers", "key"]
    """
    ssids = get_windows_ssids()
    Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
    profiles = []

    for ssid in ssids:
        ssid_details = subprocess.check_output(
            f"""netsh wlan show profile "{ssid}" key=clear"""
        ).decode()
        ciphers = re.findall(r"Cipher\s(.*)", ssid_details)
        ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
        key = re.findall(r"Key Content\s(.*)", ssid_details)
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "None"
        profile = Profile(ssid=ssid, ciphers=ciphers, key=key)
        if verbose >= 1:
            print_windows_profile(profile)
        profiles.append(profile)
    return profiles


def print_windows_profile(profile):
    """Prints a single profile on Windows"""
    print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")


def get_linux_saved_pwds(verbose=1):
    """Extracts saved Wi-Fi passwords saved in a Linux machine, this function extracts data in the
    `/etc/NetworkManager/system-connections/` directory
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "auth-alg", "key-mgmt", "psk"]
    """
    network_connections_path = "/etc/NetworkManager/system-connections/"
    fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
    Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
    profiles = []
    for file in os.listdir(network_connections_path):
        data = {k.replace("-", "_"): None for k in fields}
        config = configparser.ConfigParser()
        config.read(os.path.join(network_connections_path, file))
        for _, section in config.items():
            for k, v in section.items():
                if k in fields:
                    data[k.replace("-", "_")] = v
        profile = Profile(**data)
        if verbose >= 1:
            print_linux_profile(profile)
        profiles.append(profile)
    return profiles


def print_linux_profile(profile):
    """Prints a single profile on Linux"""
    print(
        f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}"
    )


def print_profiles(verbose=1):
    """Prints all extracted SSIDs along with Key"""
    if os.name == "nt":
        print("SSID                     CIPHER(S)      KEY")
        print("-" * 50)
        get_windows_saved_pwds(verbose)
    elif os.name == "posix":
        print("SSID                     AUTH KEY-MGMT  PSK")
        print("-" * 50)
        get_linux_saved_pwds(verbose)
    else:
        raise NotImplemented("Code only works for either Linux or Windows")


if __name__ == "__main__":
    print_profiles()
