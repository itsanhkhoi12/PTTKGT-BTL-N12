from pydantic import BaseModel, Field
from enum import Enum
from models.Point import Point


class Directions(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Robot(BaseModel):

    current_pos: Point

    # Danh sách các ô đã duyệt qua (thứ tự BFS)
    visited_order: list[Point] = Field(default_factory=list)

    # Tất cả các đường đi khả thi
    possible_solutions: list[Point] = Field(default_factory=list)

    # Đường đi ngắn nhất từ start đến end
    shortest_solution: list[Point] = Field(default_factory=list)
    
