"""
vampyre.py - an IPv4 manipulation CLI

python3 vampyre.py --help
"""

import argparse
import sys
import re
import ipaddress

# Globals
VAMPYRE_VERSION = "0.1.0-dev"

# Variables
IP_MATCH_REGEX = re.compile(r"(\d+\.\d+\.\d+\.\d+)")

parser = argparse.ArgumentParser(description="Vampyre - IP Manipulation CLI")
subparsers = parser.add_subparsers(dest="command")

# Standard Arguments
parser.version = VAMPYRE_VERSION
parser.add_argument("--version", action="version")
parser.add_argument(
    "--outfile", nargs="?", type=argparse.FileType("w"), help="Specify the output file"
)
parser.add_argument(
    "--infile", nargs="?", type=argparse.FileType("r"), help="Specify the input file"
)
parser.add_argument(
    "--fangs", nargs="?", type=str, default="[.]", help="Specify the fang characters"
)
parser.add_argument("--validate", action="store_true", help="Validate IPv4 addresses")

# Fang Parser
fang_parser = subparsers.add_parser(name="fang", help="Add 'fangs' to input")
fang_parser.add_argument("input", nargs="*")

# Defang Parser
defang_parser = subparsers.add_parser(name="defang", help="Remove 'fangs' from input")
defang_parser.add_argument("input", nargs="*")

# Extract Parser
extract_parser = subparsers.add_parser(
    name="extract", help="Extract IPv4 addresses from input"
)
extract_parser.add_argument("input", nargs="*")

args = parser.parse_args()

# Check is parser has a command, if not - exit.
if args.command is None:
    parser.print_help()
    sys.exit(1)

# Functions

candidates = []

# Read from stdin and add to candidates
if not sys.stdin.isatty():
    data = sys.stdin.read()
    candidates.append(data)

# Read infile and add to candidates
if args.infile:
    data = args.infile.read()
    candidates.append(data)

# Read arguments and add to candidates
if args.input:
    candidates.extend(args.input)

if args.command == "fang":
    print("Fang was chosen")
elif args.command == "defang":
    print("Defang was chosen")
elif args.command == "extract":
    # Check all candidates for IPv4 addresses and validate if the flag is specified.
    addresses = []

    for addr in candidates:
        matches = IP_MATCH_REGEX.findall(addr)

        if args.validate:
            for match in matches:
                try:
                    ipaddress.ip_address(match)
                    addresses.append(match)
                except ValueError:
                    print(f"[!] {match} is not a valid IPv4 address.", file=sys.stderr)
        else:
            addresses.extend(matches)

    if args.outfile:
        outfile = args.outfile
        for addr in addresses:
            outfile.write(f"{addr}\n")
        outfile.close()
    else:
        print(addresses)
