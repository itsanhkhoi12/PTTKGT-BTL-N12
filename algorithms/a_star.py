"""
Thuật toán tìm đường đi ngắn nhất A* (A-Star) trong mê cung.

Sử dụng hàm đánh giá f(n) = g(n) + h(n):
    - g(n): Chi phí đường đi thực tế từ điểm bắt đầu đến ô hiện tại n (mỗi bước = 1).
    - h(n): Ước lượng chi phí từ ô n đến đích (sử dụng khoảng cách Manhattan).
    - f(n): Tổng chi phí ước lượng nhỏ nhất đi qua n.

Độ phức tạp:
    - Thời gian: O(E * log(V)) với V = rows * cols, E là số cạnh (số ô hàng xóm).
    - Không gian: O(V) lưu trữ cấu trúc tìm kiếm và parent map.
"""

import heapq
from models.Maze import Maze, Point
from models.Robot import Robot, Directions
from utils.utils import is_valid_path


def a_star_solve(maze: Maze) -> Robot:
    """
    Tìm đường đi ngắn nhất bằng thuật toán A* Search.

    Args:
        maze: Đối tượng Maze chứa grid, start_pos và end_pos.

    Returns:
        Robot: Đối tượng Robot chứa kết quả tìm kiếm.
    """
    start = maze.start_pos
    end = maze.end_pos

    robot = Robot(current_pos=start)

    # Kiểm tra điểm đầu/cuối có nằm trên tường không
    if maze.grid[start.x][start.y] == 1 or maze.grid[end.x][end.y] == 1:
        return robot

    # Nếu start trùng end → đã đến đích
    if start == end:
        robot.shortest_solution = [start]
        robot.visited_order = [start]
        return robot

    # Hàng đợi ưu tiên chứa tuple (f_score, tie_breaker_counter, point)
    # tie_breaker_counter dùng để tránh so sánh trực tiếp hai đối tượng Point khi f_score bằng nhau
    counter = 0
    open_set = []
    heapq.heappush(open_set, (0, counter, start))

    # parent[child] = parent_node
    parent: dict[Point, Point | None] = {start: None}

    # g_score[node] = chi phí từ start tới node
    g_score: dict[Point, int] = {start: 0}

    # Thứ tự duyệt các ô để vẽ animation
    visited_order: list[Point] = []
    visited_set: set[Point] = set()

    found = False

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current in visited_set:
            continue

        visited_set.add(current)
        visited_order.append(current)

        if current == end:
            found = True
            break

        # Duyệt 4 hướng: LÊN, XUỐNG, TRÁI, PHẢI
        for direction in Directions:
            dx, dy = direction.value
            neighbor = Point(x=current.x + dx, y=current.y + dy)

            # Kiểm tra hàng xóm có hợp lệ không
            if not is_valid_path(maze, neighbor):
                continue

            # Bước đi có trọng số là 1
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                # Khoảng cách Manhattan đến đích làm Heuristic h(n)
                h_score = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
                f_score = tentative_g_score + h_score
                parent[neighbor] = current

                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

    robot.visited_order = visited_order

    if found:
        robot.current_pos = end
        robot.shortest_solution = _reconstruct_path(parent, end)

    return robot


def _reconstruct_path(
    parent: dict[Point, Point | None],
    end: Point,
) -> list[Point]:
    """
    Truy vết ngược từ đích về điểm xuất phát.
    """
    path: list[Point] = []
    current: Point | None = end

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path
