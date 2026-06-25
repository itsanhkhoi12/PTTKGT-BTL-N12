import json
from models.maze import Maze, Point
from typing import Any

def is_valid_path(maze: Maze, point: Point) -> bool:
    """
    Kiểm tra một điểm được xét có phải là đường đi khả thi hay không.
    
    Điều kiện kiểm tra:

        Có nằm trong mê cung.
        Có phải là tường hay không.

    Args:
        maze : Đối tượng Maze.
        point: Điểm cần kiểm tra.

    Returns:
        True nếu điểm hợp lệ (trong biên và là đường đi), False nếu không.
    """


    
    # Kiểm tra điểm đó lọt ngoài biên hay không
    if point.x < 0 or point.x >= maze.rows:
        return False
    if point.y < 0 or point.y >= maze.cols:
        return False

    # Kiểm tra không phải tường (1 = tường)
    if maze.grid[point.x][point.y] == 1:
        return False

    return True


def json_file_load(json_file)->Any:
    with open(json_file,'r',encoding='utf-8') as f:
        return json.load(f)