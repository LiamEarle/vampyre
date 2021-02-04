# Vampyre
A Python CLI for manipulating IP addresses

## Usage
```
usage: vampyre.py [-h] [--version] [--outfile [OUTFILE]] [--infile [INFILE]] [--fangs [FANGS]] [--validate] {fang,defang,extract} ...

Vampyre - IP Manipulation CLI

positional arguments:
  {fang,defang,extract}
    fang                Add 'fangs' to input
    defang              Remove 'fangs' from input
    extract             Extract IPv4 addresses from input

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --outfile [OUTFILE]   Specify the output file
  --infile [INFILE]     Specify the input file
  --fangs [FANGS]       Specify the fang characters
  --validate            Validate IPv4 addresses
```