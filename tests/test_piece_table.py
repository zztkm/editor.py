import pytest

from src.piece_table import PieceTable

insert_only_once_data = [
    ("world", "hello ", 0, "hello world"),
    ("hello world", "vim ", 6, "hello vim world"),
    ("tkm", " is darts player", 3, "tkm is darts player"),
]


@pytest.mark.parametrize("original, add, index, expect", insert_only_once_data)
def test_insert_only_once(original: str, add: str, index: int, expect: str):
    table = PieceTable(original)
    table.insert(add, index)
    result = table.get_text()
    assert result == expect
