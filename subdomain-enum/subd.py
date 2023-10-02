import argparse
import socket
import time


def parse_args():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description="Resolve subdomains to IP addresses.")
    parser.add_argument("-d", "--domain", required=True, help="The domain name.")
    parser.add_argument(
        "-i", "--input", required=True, help="The input file with subdomains."
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="The output file with subdomains and IP addresses.",
    )
    return parser.parse_args()


def resolve_subdomains(args):
    """Resolve subdomains to IP addresses and write them to the output file."""
    with open(args.input, "r") as f_in, open(args.output, "w") as f_out:
        for subdomain in f_in:
            subdomain = subdomain.strip()
            try:
                ip = socket.gethostbyname(f"{subdomain}.{args.domain}")
                f_out.write(f"{subdomain}.{args.domain},{ip}\n")
            except socket.gaierror:
                pass
            time.sleep(1)


def main():
    """Resolve subdomains to IP addresses."""
    args = parse_args()
    resolve_subdomains(args)


if __name__ == "__main__":
    main()
