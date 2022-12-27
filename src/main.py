import argparse
import sys
from pathlib import Path

__version__ = "0.1.0"


def main():
    parser = argparse.ArgumentParser(description="toy editor")
    parser.add_argument("file", type=str, help="file to open")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {}".format(__version__))
    args = parser.parse_args()

    file = Path(args.file)

    if not file.exists():
        print(f"{file.stem} not exists")
        sys.exit(1)

    print(file.read_text())
