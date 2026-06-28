"""
Thuật toán sinh mê cung ngẫu nhiên bằng thuật toán Prim ngẫu nhiên hóa (Randomized Prim's Algorithm).

Thuật toán Prim bắt đầu từ một ô đường đi ngẫu nhiên, sau đó duy trì tập hợp các ô biên
(frontiers) là các ô có thể nối vào phần mê cung đã sinh. Mỗi bước, chọn ngẫu nhiên
một ô biên, nếu nó chưa được nối vào mê cung thì nối nó bằng cách phá bức tường ở giữa,
đánh dấu nó là một phần của mê cung, và thêm các ô biên mới của nó vào tập hợp.

Độ phức tạp:
    - Thời gian: O(rows * cols) do mỗi ô được duyệt qua và thêm/bớt khỏi tập hợp biên một vài lần.
    - Không gian: O(rows * cols) để lưu tập biên và tập đã duyệt.
"""

import random
from models.Maze import Maze, Point
from models.Robot import Directions


def prim_maze_generation(
    row: int,
    col: int,
    start_pos: Point,
    end_pos: Point,
) -> Maze:
    """
    Sinh ngẫu nhiên một mê cung bằng thuật toán Prim cải tiến.

    Quy ước:
        - 0: Đường đi (Path)
        - 1: Tường (Wall)

    Args:
        row: Số hàng của mê cung.
        col: Số cột của mê cung.
        start_pos: Vị trí bắt đầu.
        end_pos: Vị trí kết thúc.

    Returns:
        Maze: Đối tượng Maze đã được tạo cấu trúc đường đi/tường.
    """
    # Đảm bảo kích thước mê cung là số lẻ để cấu trúc tường/đường đi đẹp mắt
    if row % 2 == 0:
        row += 1
    if col % 2 == 0:
        col += 1

    # Khởi tạo lưới toàn tường (1)
    grid: list[list[int]] = [[1 for _ in range(col)] for _ in range(row)]

    # Chọn ô bắt đầu sinh mê cung (tương ứng với start_pos nếu là lẻ, không thì chuyển sang ô lẻ gần nhất)
    start_cell = Point(
        x=start_pos.x if start_pos.x % 2 == 1 else start_pos.x + 1,
        y=start_pos.y if start_pos.y % 2 == 1 else start_pos.y + 1,
    )

    # Đánh dấu ô bắt đầu là đường đi (0) và thêm vào tập đã duyệt
    grid[start_cell.x][start_cell.y] = 0
    visited: set[Point] = {start_cell}

    # Hàng đợi biên lưu các tuple: (ô biên, ô cha đã duyệt kết nối với nó)
    frontiers: list[tuple[Point, Point]] = []

    def add_frontiers(cell: Point) -> None:
        """Thêm các ô biên ở khoảng cách 2 bước chưa được duyệt."""
        for direction in Directions:
            dx, dy = direction.value
            next_cell = cell + (2 * Point(dx, dy))

            # Ranh giới mê cung loại trừ phần viền ngoài cùng
            if (
                1 <= next_cell.x < row - 1
                and 1 <= next_cell.y < col - 1
                and next_cell not in visited
            ):
                frontiers.append((next_cell, cell))

    # Thêm các biên của ô xuất phát
    add_frontiers(start_cell)

    while frontiers:
        # Chọn ngẫu nhiên một ô biên từ danh sách
        idx = random.randrange(len(frontiers))
        frontier_cell, parent_cell = frontiers.pop(idx)

        if frontier_cell not in visited:
            # Phá bức tường nằm giữa ô biên và ô cha
            wall_x = (frontier_cell.x + parent_cell.x) // 2
            wall_y = (frontier_cell.y + parent_cell.y) // 2
            grid[wall_x][wall_y] = 0
            grid[frontier_cell.x][frontier_cell.y] = 0

            # Đánh dấu ô biên là đã duyệt và mở rộng biên từ đó
            visited.add(frontier_cell)
            add_frontiers(frontier_cell)

    # Đảm bảo start_pos và end_pos được giải phóng làm đường đi
    grid[start_pos.x][start_pos.y] = 0
    grid[end_pos.x][end_pos.y] = 0

    return Maze(
        rows=row,
        cols=col,
        grid=grid,
        start_pos=start_pos,
        end_pos=end_pos,
    )
