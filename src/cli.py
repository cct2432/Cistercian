import sys
import argparse
from .converter import to_cis, from_cis

def main():
    parser = argparse.ArgumentParser(description="Convert integers to/from Cistercian Numeral SVGs")
    parser.add_argument("input", nargs="?", help="Convert integer (0-9999) to Cistercian Numeral SVG Code")
    parser.add_argument("-r", "--reverse", action="store_true", help="Convert Cistercian SVG code into integer")

    args = parser.parse_args()

    if not args.input and not sys.stdin.isatty():
        piped_content = sys.stdin.read().strip()
        try:
            if args.reverse:
                print(from_cis(piped_content))
            else:
                number = int(piped_content)
                print(to_cis(number))
            return
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    try:
        if args.reverse:
            try:
                with open(args.input, "r", encoding="utf-8") as f:
                    svg_content = f.read()
            except OSError:
                svg_content = args.input
            print(from_cis(svg_content))
        else:
            number = int(args.input)
            print(to_cis(number))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
