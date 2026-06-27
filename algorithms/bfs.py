"""
Thuật toán BFS (Breadth-First Search) tìm đường đi ngắn nhất trong mê cung.

BFS duyệt theo chiều rộng, đảm bảo tìm được đường đi ngắn nhất
(ít bước nhất) từ điểm bắt đầu đến điểm kết thúc trong mê cung.

Độ phức tạp:
    - Thời gian : O(rows * cols) — mỗi ô được duyệt tối đa 1 lần
    - Không gian: O(rows * cols) — lưu trữ visited và hàng đợi
"""

from collections import deque

from models.Maze import Maze, Point
from models.Robot import Robot, Directions
from utils.utils import is_valid_path

def bfs_solve(maze: Maze) -> Robot:
    """
    Tìm đường đi ngắn nhất trong mê cung bằng thuật toán BFS.

    Args:
        maze: Đối tượng Maze chứa grid, start_pos và end_pos.

    Returns:
        Robot: Đối tượng Robot chứa:
            - current_pos : vị trí hiện tại (end_pos nếu tìm thấy đường)
            - visited_order: thứ tự các ô đã duyệt qua
            - shortest_solution     : đường đi ngắn nhất từ start đến end
                             (rỗng nếu không tìm thấy đường)
    """
    start = maze.start_pos
    end = maze.end_pos

    # Khởi tạo Robot tại vị trí bắt đầu
    robot = Robot(current_pos=start)

    # ---- Kiểm tra đầu vào ----
    # Nếu start hoặc end nằm trên tường → không có đường đi
    if maze.grid[start.x][start.y] == 1 or maze.grid[end.x][end.y] == 1:
        return robot

    # Nếu start trùng end → đã đến đích
    if start == end:
        robot.shortest_solution = [start]
        robot.visited_order = [start]
        return robot

    # ---- BFS ----
    # Hàng đợi (queue) chứa các ô cần duyệt
    queue: deque[Point] = deque([start])

    # Tập hợp các ô đã thăm — tránh duyệt lại
    visited: set[Point] = {start}

    # Lưu ô cha (parent) để truy vết đường đi sau khi tìm thấy đích
    # parent[child] = ô trước đó trên đường đi ngắn nhất
    parent: dict[Point, Point | None] = {start: None}

    # Danh sách thứ tự các ô được duyệt (dùng để minh hoạ)
    visited_order: list[Point] = [start]

    found = False

    while queue:
        # Lấy ô đầu hàng đợi ra để xử lý
        current = queue.popleft()
        robot.current_pos = current

        # Duyệt 4 hướng: LÊN, XUỐNG, TRÁI, PHẢI
        for direction in Directions:
            dx, dy = direction.value
            neighbor = Point(x=current.x + dx, y=current.y + dy)

            # Kiểm tra hàng xóm có hợp lệ không
            if not is_valid_path(maze, neighbor):
                continue

            # Bỏ qua ô đã thăm
            if neighbor in visited:
                continue

            # Đánh dấu đã thăm & ghi nhận ô cha
            visited.add(neighbor)
            parent[neighbor] = current
            visited_order.append(neighbor)

            # Thêm vào hàng đợi để duyệt tiếp
            queue.append(neighbor)

            # Kiểm tra đã đến đích chưa
            if neighbor == end:
                found = True
                break

        if found:
            break

    # ---- Truy vết đường đi ----
    robot.visited_order = visited_order

    if found:
        robot.current_pos = end
        robot.shortest_solution = _reconstruct_path(parent, start, end)
    # Nếu không tìm thấy → solution giữ nguyên rỗng

    return robot


def _reconstruct_path(
    parent: dict[Point, Point | None],
    end: Point,
) -> list[Point]:
    """
    Truy vết đường đi từ end về start dựa trên bản đồ parent,
    sau đó đảo ngược để có đường đi từ start → end.

    Args:
        parent: Dict lưu ô cha của mỗi ô trên đường đi.
        start : Điểm bắt đầu.
        end   : Điểm kết thúc.

    Returns:
        Danh sách các Point tạo thành đường đi ngắn nhất.
    """
    path: list[Point] = []
    current: Point | None = end

    while current is not None:
        path.append(current)
        current = parent[current]

    # Đảo ngược vì ta đang truy vết từ end → start
    path.reverse()
    return path
