import sys
from .converter import to_cis, from_cis

def to_cis_cli():
    if len(sys.argv) < 2:
        print("Usage: cistercian <number>")
        print("  <number>: integer 0-9999 to encode as SVG")
        sys.exit(1)
    input = sys.argv[1]
    to_cis(input)

def from_cis_cli():
    # WIP
    print("from_cis is WIP")
