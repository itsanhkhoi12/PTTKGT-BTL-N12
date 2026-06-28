"""
Thuật toán tìm đường đi ngắn nhất Dijkstra trong mê cung.

Dijkstra hoạt động bằng cách luôn chọn đỉnh có khoảng cách ngắn nhất tính từ nguồn.
Trong mê cung không có trọng số (hoặc trọng số các bước đều = 1), thuật toán Dijkstra
sẽ cho kết quả tương đương BFS nhưng sử dụng hàng đợi ưu tiên (Priority Queue).

Độ phức tạp:
    - Thời gian: O(E * log(V)) với V = rows * cols, E là số cạnh.
    - Không gian: O(V) lưu trữ dist và parent map.
"""

import heapq
from models.Maze import Maze, Point
from models.Robot import Robot, Directions
from utils.utils import is_valid_path


def dijkstra_solve(maze: Maze) -> Robot:
    """
    Tìm đường đi ngắn nhất bằng thuật toán Dijkstra.

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

    # Hàng đợi ưu tiên chứa tuple (distance, tie_breaker_counter, point)
    counter = 0
    open_set = []
    heapq.heappush(open_set, (0, counter, start))

    # parent[child] = parent_node
    parent: dict[Point, Point | None] = {start: None}

    # dist[node] = chi phí đường đi thực tế từ start đến node
    dist: dict[Point, int] = {start: 0}

    # Thứ tự duyệt các ô để vẽ animation
    visited_order: list[Point] = []
    visited_set: set[Point] = set()

    found = False

    while open_set:
        d, _, current = heapq.heappop(open_set)

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

            # Chi phí mỗi bước di chuyển là 1
            tentative_dist = dist[current] + 1

            if neighbor not in dist or tentative_dist < dist[neighbor]:
                dist[neighbor] = tentative_dist
                parent[neighbor] = current

                counter += 1
                heapq.heappush(open_set, (tentative_dist, counter, neighbor))

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
