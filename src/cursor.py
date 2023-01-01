class Cursor:
    def __init__(self, x: int, y: int):
        # 現在のカーソル位置
        self._x = x
        self._y = y
        # 前のカーソル位置
        self._befor_x = x
        self._befor_y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def befor_x(self) -> int:
        return self._befor_x

    @property
    def befor_y(self) -> int:
        return self._befor_y

    def up(self):
        self._befor_y = self._y
        self._y -= 1

    def down(self):
        self._befor_y = self._y
        self._y += 1

    def right(self):
        self._befor_x = self._x
        self._x += 1

    def left(self):
        self._befor_x = self._x
        self._x -= 1
