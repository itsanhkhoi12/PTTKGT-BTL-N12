from pydantic import BaseModel, Field
from typing import Enum
from models.maze import Point


class Direction(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    LEFT = (0,-1)
    RIGHT = (0,1)

class Robot(BaseModel):
    current_pos: Point
    solution: list[Point] = Field(default_factory = list)
    
