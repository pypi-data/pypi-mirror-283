import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Cobanov command line tool")
    parser.add_argument("--watch", action="store_true", help="Watch for changes")
    args = parser.parse_args()

    if args.watch:
        print("Watching for changes...")
        # Add your watch functionality here


if __name__ == "__main__":
    main()
