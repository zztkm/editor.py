import argparse
import logging
import sys
from pathlib import Path
from shutil import get_terminal_size

from readchar import readkey

from .piece_table import PieceTable
from .terminal import Terminal

__version__ = "0.2.0"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 横幅に余白を持たせるための定数
MARGIN = 1


def main():
    parser = argparse.ArgumentParser(description="toy editor")
    parser.add_argument("file", type=str, help="file to open")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {}".format(__version__))
    args = parser.parse_args()

    file = Path(args.file)

    if not file.exists():
        print(f"{file.stem} not exists")
        sys.exit(1)

    original_content = file.read_text(encoding="utf-8")
    table = PieceTable(original_content)

    terminal_size = get_terminal_size()
    terminal = Terminal(terminal_size.columns - MARGIN, terminal_size.lines - MARGIN, table.get_text())
    terminal.clear()
    terminal.print()
    while True:
        k = ""
        try:
            k = readkey()
            terminal.input(k)
            # TODO: 画面のスクロールがない場合は再描画をスキップする
            terminal.print()
        except KeyboardInterrupt:
            pass
