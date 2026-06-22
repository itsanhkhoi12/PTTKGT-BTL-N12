from models.maze import Point, Maze
from models.robot import Directions
from utils.utils import is_valid_path


def finding_valid_paths(
    maze: Maze,
    possible_solutions: list[list[Point]],
    current_pos: Point,
    path: list[Point],
) -> None:
    
    # Thêm vị trí hiện tại vào path
    path.append(current_pos)

    # Nếu đã đến đích
    if current_pos.x == maze.end_pos.x and current_pos.y == maze.end_pos.y:
        possible_solutions.append(path.copy())
        path.pop()
        return

    # Đánh dấu ô hiện tại là đã đi
    maze.grid[current_pos.x][current_pos.y] = 1

    for direction in Directions:
        dx, dy = direction.value

        next_pos = Point(
            x=current_pos.x + dx,
            y=current_pos.y + dy,
        )

        if is_valid_path(maze, next_pos):
            finding_valid_paths(
                maze=maze,
                possible_solutions=possible_solutions,
                current_pos=next_pos,
                path=path,
            )

    # Backtracking: khôi phục trạng thái
    maze.grid[current_pos.x][current_pos.y] = 0
    path.pop()


