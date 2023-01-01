import logging
import platform
import subprocess
import sys
import unicodedata

from colorama import Back, Fore, Style
from readchar import key

from .cursor import Cursor

logger = logging.getLogger(__name__)


# 文字白
WHITE = "\033[37"
# 背景白
BG_WHITE = "\033[47m"


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    return count


class Terminal:
    def __init__(self, width: int, height: int, text: str):
        self.__width = width
        self.__height = height

        self.__window_start_y = 0
        self.__cursor = Cursor(0, 0)
        self.__set_number = True
        self.__platform = platform.system()
        self.__buffer = self.__init_buffer(text)

    def __init_buffer(self, text: str) -> list[str]:
        lines = text.splitlines()
        if self.__set_number:
            width = self.__width - 2
        else:
            width = self.__width

        for i in range(len(lines)):
            if get_east_asian_width_count(lines[i]) >= width:
                # テキストが折り返すパターン
                new_lines = self.__split_lines(lines[i], width)
                lines = lines[:i] + new_lines + lines[i + 1 :]

        return lines

    def __split_lines(self, line: str, n) -> list[str]:
        lines = []
        count = 0
        step = 0
        for i in range(len(line)):
            if unicodedata.east_asian_width(line[i]) in "FWA":
                count += 2
            else:
                count += 1

            if count == n:
                lines.append(line[step:i])
                count = 0
                step = i
            elif count == n - 1:
                lines.append(line[step:i])
                count = 0
                step = i

        return lines

    def input(self, k: str):
        if k == "q":
            logger.info("終了します")
            sys.exit(1)

        # 移動系
        if k == "j" or k == key.DOWN:
            if self.__cursor.y < self.__height:
                # TODO: 画面スクロール処理を実装する
                # 画面スクロールが実装できたらここの処理を変更する
                self.__cursor.down()
                if self.__cursor.y > self.__window_start_y + self.__height:
                    self.__window_start_y += 1
        elif k == "k" or k == key.UP:
            if self.__cursor.y > 0:
                self.__cursor.up()
                if self.__cursor.y < self.__window_start_y:
                    self.__window_start_y -= 1
        elif k == "l" or k == key.RIGHT:
            if self.__cursor.x < self.__width:
                self.__cursor.right()
        elif k == "h" or k == key.LEFT:
            if self.__cursor.x > 0:
                self.__cursor.left()

    def clear(self):
        cmd = "clear"
        if self.__platform == "Windows":
            cmd = "cls"
        # TODO: 実行結果を取得してどうにかする
        # コマンドの実行がエラーになった場合に例外を送出する
        subprocess.run(cmd, shell=True)

    def print(self):
        if self.__cursor.y + self.__height > len(self.__buffer):
            # 範囲外なので何もせずに return
            return
        for i in range(self.__window_start_y, self.__window_start_y + self.__height):
            if self.__set_number:
                if self.__cursor.y == i:
                    text = self.__buffer[i]
                    pos_x = self.__cursor.x
                    if len(text) == 0:
                        # 行の要素数が 0 のときはスペースを代入する
                        print(f"{i} {Back.WHITE}{Fore.BLACK} {Style.RESET_ALL}")
                        continue
                    elif len(text) < pos_x:
                        pos_x = len(text) - 1
                        cursor_pos_text = f"{Back.WHITE}{Fore.BLACK}{text[pos_x]}{Style.RESET_ALL}"
                    else:
                        cursor_pos_text = f"{Back.WHITE}{Fore.BLACK}{text[pos_x]}{Style.RESET_ALL}"

                    text = text[:pos_x] + cursor_pos_text + text[pos_x + 1 :]
                    print(f"{i} {text}")
                else:
                    print(f"{i} {self.__buffer[i]}")
            else:
                print(self.__buffer[i])
