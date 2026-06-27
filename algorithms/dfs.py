from models.Maze import Point, Maze
from models.Robot import Directions
from utils.utils import is_valid_path
import random


def finding_valid_paths(
    maze: Maze,
    current_pos: Point,
    path: list[Point],
    possible_solutions: list[list[Point]] = [],
) -> None:
    """Tìm kiếm tất cả các đường đi khả thi trong mê cung với điểm đầu và điểm kết thúc đã cho trước.

    Sử dụng thuật toán DFS + Backtracking

    Args:
        maze: Mê cung cho trước
        current_pos: Vị trí hiện tại đang xét (Init = điểm bắt đầu của mê cung)
        possible_solutions: Danh sách các đường đi khả thi
        path: Danh sách các Point theo thứ tự thể hiện đường đi
    """
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


def maze_generation(
    row: int,
    col: int,
    start_pos: Point,
    end_pos: Point,
) -> Maze:
    """
    Sinh ngẫu nhiên một mê cung sử dụng thuật toán Recursive Backtracking
    (Depth First Search Maze Generation).

    Thuật toán bắt đầu từ một ô xuất phát, sau đó duyệt DFS qua các ô
    chưa được thăm. Mỗi lần mở rộng, thuật toán sẽ phá bỏ bức tường nằm
    giữa ô hiện tại và ô kế tiếp để tạo thành đường đi hợp lệ.

    Quy ước:
        - 0: Đường đi (Path)
        - 1: Tường (Wall)

    Để đảm bảo cấu trúc mê cung hợp lệ, kích thước mê cung nên là số lẻ.
    Nếu người dùng nhập số chẵn, kích thước sẽ được tự động tăng thêm 1.

    Args:
        row (int):
            Số hàng của mê cung.

        col (int):
            Số cột của mê cung.

        start_pos (Point):
            Vị trí bắt đầu của mê cung.

        end_pos (Point):
            Vị trí kết thúc của mê cung.

    Returns:
        Maze
    """

    # Nên dùng kích thước lẻ để DFS generation đẹp hơn
    if row % 2 == 0:
        row += 1

    if col % 2 == 0:
        col += 1

    # 1 = wall, 0 = path
    grid: list[list[int]] = [[1 for _ in range(col)] for _ in range(row)]

    visited: set[Point] = set()

    def dfs(current: Point) -> None:
        visited.add(current)
        grid[current.x][current.y] = 0

        directions = list(Directions)
        random.shuffle(directions)

        for direction in directions:
            dx, dy = direction.value

            next_cell = current + ( 2 * Point(dx, dy) )

            wall_between = current + Point(dx,dy)

            if (
                1 <= next_cell.x < row - 1
                and 1 <= next_cell.y < col - 1
                and next_cell not in visited
            ):
                grid[wall_between.x][wall_between.y] = 0
                dfs(next_cell)

    # DFS generation nên bắt đầu từ cell lẻ
    start_cell = Point(
        x=start_pos.x if start_pos.x % 2 == 1 else start_pos.x + 1,
        y=start_pos.y if start_pos.y % 2 == 1 else start_pos.y + 1,
    )

    dfs(start_cell)

    grid[start_pos.x][start_pos.y] = 0
    grid[end_pos.x][end_pos.y] = 0

    return Maze(
        rows=row,
        cols=col,
        grid=grid,
        start_pos=start_pos,
        end_pos=end_pos,
    )
