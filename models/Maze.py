from pydantic import BaseModel, Field
from models.Point import Point

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
    