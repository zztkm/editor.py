import logging
import platform
import subprocess
import sys
import unicodedata

from readchar import key

logger = logging.getLogger(__name__)


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

        self.__cursor_pos_x = 0
        self.__cursor_pos_y = 0
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
            if self.__cursor_pos_y < self.__height:
                # TODO: 画面スクロール処理を実装する
                # 画面スクロールが実装できたらここの処理を変更する
                self.__cursor_pos_y += 1
        elif k == "k" or k == key.UP:
            if self.__cursor_pos_y > 0:
                self.__cursor_pos_y -= 1
        elif k == "l" or k == key.RIGHT:
            if self.__cursor_pos_x < self.__width:
                self.__cursor_pos_x += 1
        elif k == "h" or k == key.LEFT:
            if self.__cursor_pos_x > 0:
                self.__cursor_pos_x -= 1

    def clear(self):
        cmd = "clear"
        if self.__platform == "Windows":
            cmd = "cls"
        # TODO: 実行結果を取得してどうにかする
        # コマンドの実行がエラーになった場合に例外を送出する
        subprocess.run(cmd, shell=True)

    def print(self):
        if self.__cursor_pos_y + self.__height > len(self.__buffer):
            # 範囲外なので何もせずに return
            return
        for i in range(self.__cursor_pos_y, self.__cursor_pos_y + self.__height):
            if self.__set_number:
                print(f"{i} {self.__buffer[i]}")
            else:
                print(self.__buffer[i])
