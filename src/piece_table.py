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
        self.__buffer = ""
        self.pieces = [Piece(Target.ORIGINAL, 0, len(self.__original_content))]

    def index(self, index: int) -> str:
        """return the character at position index.

        Args:
            index(int): index into the text

        Returs:
            str: character at position index
        """
        piece_index, offset = self._get_piece_index_and_offset(index)
        text = self._get_piece_text(piece_index)
        return text[self.pieces[piece_index].length - (offset - index)]

    def _add_buffer(self, text: str) -> int:
        """return the position added to buffer

        Args:
            text(str): string to be added

        Returs:
            int: position added to buffer
        """
        added_index = len(self.__buffer)
        self.__buffer += text
        return added_index

    def _insert_last(self, added_index: int, text_len: int):
        last_piece = self.pieces[-1]
        if last_piece.which == Target.ORIGINAL:
            self.pieces.append(Piece(Target.ADD, added_index, text_len))
        else:
            # 最後の piece が Target.ADD だった場合
            # 追加する文字の長さを length に足す
            last_piece.length += text_len

    def insert(self, text: str, index: int):
        """
        NOTE: 実装方針

        INSERT 処理上必要な条件分岐は基本的にこの関数内で対応する

        INSERTの仕方をユースケースと見て、ユースケースごとの関数にわける
        """

        # TODO: input の検証関数を実装する
        if text == "":
            return

        # 書き込み用バッファに文字列を追加
        added_index = self._add_buffer(text)

        piece_index, offset = self._get_piece_index_and_offset(index)
        if len(self.pieces) == piece_index:
            self._insert_last(added_index, len(text))
            return

        target_piece = self.pieces[piece_index]

        # text が piece の内側に位置する場合は3分割する
        splited_pieces = [
            Piece(target_piece.which, target_piece.start_index, offset - target_piece.start_index),
            Piece(Target.ADD, added_index, len(text)),
            Piece(target_piece.which, offset, target_piece.length - (offset - target_piece.start_index)),
        ]
        splited_pieces = list(filter(lambda p: p.length > 0, splited_pieces))
        self.pieces = self.pieces[:piece_index] + splited_pieces + self.pieces[piece_index + 1 :]

    def delete(self, index: int, length: int):
        if length <= 0:
            return

        piece_index, offset = self._get_piece_index_and_offset(index)

        if len(self.pieces) == piece_index:
            # 存在しない位置からの削除
            print("存在しない")
            return

        if self.pieces[piece_index].length - offset >= length:
            # 取り回しやすいように変数化
            piece = self.pieces[piece_index]
            if piece.start_index == offset:
                piece.start_index += length
                piece.length -= length
                return
            elif piece.length == offset + length:
                piece.length -= length
                return

    def get_text(self):
        text = ""
        for i in range(len(self.pieces)):
            text += self._get_piece_text(i)
        return text

    def _get_piece_text(self, index: int):
        piece = self.pieces[index]
        if piece.which == Target.ORIGINAL:
            return self.__original_content[piece.start_index : piece.start_index + piece.length]
        else:
            return self.__buffer[piece.start_index : piece.start_index + piece.length]

    def _get_piece_index_and_offset(self, index: int) -> tuple[int, int]:
        """return the piece index and offset.

        Args:
            index(int): index into the text

        Returs:
            tuple[int, int]: [piece index, offset]
        """
        if index < 0:
            raise IndexError("Not allowed to be less than 0")

        offset = 0
        for i in range(len(self.pieces)):
            offset += self.pieces[i].length
            if index < offset:
                return i, self.pieces[i].length - (offset - index)
            elif index == offset:
                return i + 1, 0

        raise IndexError("Index out of range")
