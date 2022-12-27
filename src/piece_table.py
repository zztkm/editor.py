from dataclasses import dataclass
from enum import Enum


class Target(Enum):
    ORIGINAL = 0
    ADD = 1


@dataclass
class Piece:
    which: Target
    start_index: int
    length: int


class PieceTable:

    def __init__(self, original_content: str):
        self.__original_content = original_content
        self.__add_content = ""
        self.pieces = [Piece(Target.ORIGINAL, 0, len(self.__original_content))]

    def get_index(self, index: int) -> int:
        """returns the piece containing the position of index.

        Args:
            index(int): index into the text

        Returs:
            int: piece index
        """
        if index < 0:
            raise IndexError("Not allowed to be less than 0")

        for i in range(len(self.pieces)):
            if index <= self.pieces[i].length:
                return i
            index -= self.pieces[i].length

        raise IndexError("...")

    def insert(self, text: str, index: int):
        if text == "":
            return

        piece_index = self.get_index(index)
        target_piece = self.pieces[piece_index]

        # 書き込み用バッファに文字列を追加
        added_index = len(self.__add_content)
        self.__add_content += text

        # text が piece の内側に位置する場合は3分割する
        splited_pieces = [
            Piece(target_piece.which, target_piece.start_index, index - target_piece.start_index),
            Piece(Target.ADD, added_index, len(text)),
            Piece(target_piece.which, index, target_piece.length - (index - target_piece.start_index)),
        ]
        self.pieces = self.pieces[:piece_index] + splited_pieces + self.pieces[piece_index + 1:]


    def delete(self, index: int, length: int):
        print(index)
        print(length)

    def get_text(self):
        text = ""
        for piece in self.pieces:
            if piece.which == Target.ORIGINAL:
                text += self.__original_content[piece.start_index:piece.start_index + piece.length]
            else:
                text += self.__add_content[piece.start_index:piece.start_index + piece.length]
        return text

