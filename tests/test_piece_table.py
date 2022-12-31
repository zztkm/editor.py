from dataclasses import dataclass

import pytest

from src.piece_table import PieceTable


@dataclass
class InsertData:
    index: int
    text: str


insert_only_once_data = [
    ("hello", " world", 5, "hello world"),
    ("hello", "oo", 4, "hellooo"),
    ("world", "hello ", 0, "hello world"),
    ("hello world", "vim ", 6, "hello vim world"),
    ("zztkm", " is darts player", 5, "zztkm is darts player"),
]


@pytest.mark.parametrize("original, add, index, expect", insert_only_once_data)
def test_insert_only_once(original: str, add: str, index: int, expect: str):
    table = PieceTable(original)
    table.insert(add, index)
    result = table.get_text()
    assert result == expect


insert_twice_data = [
    ("hello", [InsertData(5, " world"), InsertData(11, " vim")], "hello world vim"),
    ("hello", [InsertData(5, " world"), InsertData(6, "vim ")], "hello vim world"),
]


@pytest.mark.parametrize("original, insert_list, expect", insert_twice_data)
def test_insert_twice(original: str, insert_list: list[InsertData], expect: str):
    table = PieceTable(original)
    for data in insert_list:
        table.insert(data.text, data.index)
    result = table.get_text()
    assert result == expect


delete_test_data = [
    ("hello", 0, 2, "llo"),
    ("hello", 4, 1, "hell"),
    ("hello", 2, 2, "heo"),
]


@pytest.mark.parametrize("original, index, length, expect", delete_test_data)
def test_delete(original: str, index: int, length: int, expect: str):
    table = PieceTable(original)
    table.delete(index, length)
    result = table.get_text()
    assert result == expect


delete_across_pieces_data = [
    ("hello", [InsertData(5, " world")], 4, 3, "hellorld"),
    ("hello", [InsertData(5, " world")], 5, 6, "hello"),
    ("hello", [InsertData(5, " world"), InsertData(11, " vim")], 4, 11, "hell"),
    ("hello", [InsertData(5, " world"), InsertData(11, " vim")], 5, 10, "hello"),
]


@pytest.mark.parametrize("original, insert_list, index, length, expect", delete_across_pieces_data)
def test_delete_across_pieces(original: str, insert_list: list[InsertData], index: int, length: int, expect: str):
    table = PieceTable(original)
    for data in insert_list:
        table.insert(data.text, data.index)
    table.delete(index, length)
    result = table.get_text()
    assert result == expect
