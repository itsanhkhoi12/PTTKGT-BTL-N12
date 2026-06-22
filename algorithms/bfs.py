"""
Thuật toán BFS (Breadth-First Search) tìm đường đi ngắn nhất trong mê cung.

BFS duyệt theo chiều rộng, đảm bảo tìm được đường đi ngắn nhất
(ít bước nhất) từ điểm bắt đầu đến điểm kết thúc trong mê cung.

Độ phức tạp:
    - Thời gian : O(rows * cols) — mỗi ô được duyệt tối đa 1 lần
    - Không gian: O(rows * cols) — lưu trữ visited và hàng đợi
"""

from collections import deque

from models.maze import Maze, Point
from models.robot import Robot, Direction


def bfs_solve(maze: Maze) -> Robot:
    """
    Tìm đường đi ngắn nhất trong mê cung bằng thuật toán BFS.

    Args:
        maze: Đối tượng Maze chứa grid, start_pos và end_pos.

    Returns:
        Robot: Đối tượng Robot chứa:
            - current_pos : vị trí hiện tại (end_pos nếu tìm thấy đường)
            - visited_order: thứ tự các ô đã duyệt qua
            - solution     : đường đi ngắn nhất từ start đến end
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
        robot.solution = [start]
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
        for direction in Direction:
            dx, dy = direction.value
            neighbor = Point(x=current.x + dx, y=current.y + dy)

            # Kiểm tra hàng xóm có hợp lệ không
            if not _is_valid(maze, neighbor):
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
        robot.solution = _reconstruct_path(parent, start, end)
    # Nếu không tìm thấy → solution giữ nguyên rỗng

    return robot


def _is_valid(maze: Maze, point: Point) -> bool:
    """
    Kiểm tra một điểm có nằm trong mê cung và không phải tường hay không.

    Args:
        maze : Đối tượng Maze.
        point: Điểm cần kiểm tra.

    Returns:
        True nếu điểm hợp lệ (trong biên và là đường đi), False nếu không.
    """
    # Kiểm tra nằm trong biên
    if point.x < 0 or point.x >= maze.rows:
        return False
    if point.y < 0 or point.y >= maze.cols:
        return False

    # Kiểm tra không phải tường (1 = tường)
    if maze.grid[point.x][point.y] == 1:
        return False

    return True


def _reconstruct_path(
    parent: dict[Point, Point | None],
    start: Point,
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
