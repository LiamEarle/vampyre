#!/usr/bin/env python

import argparse
import sys
import re
import io
import ipaddress

# Variables
IP_MATCH_REGEX = re.compile(r'(\d+\.\d+\.\d+\.\d+)')

parser = argparse.ArgumentParser(description='Vampyre - IP Manipulation CLI')
subparsers = parser.add_subparsers(dest='command')

# Standard Arguments
parser.version = '0.1.0-dev'
parser.add_argument('--version', action='version')
parser.add_argument('--outfile', nargs='?', type=argparse.FileType('w'), help='Specify the output file')
parser.add_argument('--infile', nargs='?', type=argparse.FileType('r'), help='Specify the input file')
parser.add_argument('--fangs', nargs='?', type=str, default='[.]', help='Specify the fang characters')
parser.add_argument('--validate', action='store_true', help='Validate IPv4 addresses')


# Fang Parser
fang_parser = subparsers.add_parser(name='fang', help='Add \'fangs\' to input')
fang_parser.add_argument('input', nargs='*')

# Defang Parser
defang_parser = subparsers.add_parser(name='defang', help='Remove \'fangs\' from input')
defang_parser.add_argument('input', nargs='*')

# Extract Parser
extract_parser = subparsers.add_parser(name='extract', help='Extract IPv4 addresses from input')
extract_parser.add_argument('input', nargs='*')

args = parser.parse_args()

# Functions


addresses = [] # Variable for holding matched IPv4 addresses
candidates = []

# Read from stdin and add to candidates
if (sys.stdin):
    data = sys.stdin.read()
    candidates.append(data)

# Read infile and add to candidates
if (args.infile):
    data = args.infile.read()
    candidates.append(data)

# Read arguments and add to candidates
if (len(args.input) > 0):
    candidates.extend(args.input)

# Check all candidates for IPv4 addresses and validate if the flag is specified.
for addr in candidates:
    matches = IP_MATCH_REGEX.findall(addr)

    if (args.validate):
        for match in matches:
            try:
                ipaddress.ip_address(match) # NO-OP: This will throw an error if the address is not valid
                addresses.append(match)
            except ValueError:
                print(f'[!] {match} is not a valid IPv4 address.', file=sys.stderr)
    else:
        addresses.extend(matches)

if (args.command == 'fang'):
    print('Fang was chosen')
elif (args.command == 'defang'):
    print('Defang was chosen')
elif (args.command == 'extract'):
    if (args.outfile):
        outfile = args.outfile
        for addr in addresses:
            outfile.write(f'{addr}\n')
        outfile.close()
    else:
        print(addresses)
        




