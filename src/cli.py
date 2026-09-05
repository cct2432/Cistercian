import sys
from .converter import to_cis, from_cis

def main():
    if len(sys.argv) < 2:
        print("Usage: cistercian <number> | --decode <svg>")
        print("  <number>    : integer 0-9999 to encode as SVG")
        print("  --decode <svg> : SVG string to decode back to integer")
        sys.exit(1)

    if sys.argv[1] == "--decode":
        if len(sys.argv) < 3:
            print("Error: --decode requires an SVG string argument")
            sys.exit(1)
        svg = sys.argv[2]
        try:
            result = from_cis(svg)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            number = int(sys.argv[1])
            svg = to_cis(number)
            print(svg)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
