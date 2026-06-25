from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Literal


# Định nghĩa vị trí theo ô (x;y)

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    # Phép cộng hai điểm
    def __add__(self, p1: "Point")-> "Point":
        return Point(self.x + p1.x, self.y + p1.y)
    

    # Nhân tọa độ với một số thực vô hướng
    def __mul__(self, scalar: int) -> "Point":
        return Point(self.x * scalar, self.y * scalar)
    

    __radd__ = __add__
    __rmul__ = __mul__


class Maze(BaseModel):
    id: str = ''
    rows: int 
    cols: int 
    
    # Grid tức là field định nghĩa map của mê cung
        # 0 là đường đi
        # 1 là tường
    grid: list[list[int]] = Field(default_factory = list)

    # Điểm bắt đầu của mê cung
    start_pos: Point

    # Điểm kết thúc của mê cung
    end_pos: Point
    