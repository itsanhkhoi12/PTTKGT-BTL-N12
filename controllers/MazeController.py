import time
import copy
import tkinter as tk
from tkinter import messagebox

from models.Maze import Maze
from models.Point import Point
from algorithms.bfs import bfs_solve
from algorithms.dfs import finding_valid_paths, maze_generation
from algorithms.a_star import a_star_solve
from algorithms.dijkstra import dijkstra_solve
from algorithms.prim import prim_maze_generation


class MazeController:
    """Controller kết nối View (MainWindow) với Algorithms (BFS, DFS)
    và quản lý trạng thái mê cung hiện tại.
    """

    # Trạng thái ô trên grid hiển thị
    CELL_PATH = 0
    CELL_WALL = 1
    CELL_VISITED = 2
    CELL_START = 3
    CELL_END = 4
    CELL_SOLUTION = 5

    def __init__(self, view) -> None:
        self.view = view
        self.maze: Maze | None = None

        # Gắn controller vào view
        self.view.set_controller(self)

    # ================================================================
    #  SINH MÊ CUNG
    # ================================================================

    def generate_maze(self) -> None:
        """Sinh mê cung ngẫu nhiên từ thông số người dùng nhập."""
        try:
            params = self.view.control_panel.get_generation_input()

            rows = params["rows"]
            cols = params["cols"]
            start = Point(x=1, y=1)
            end = Point(x=rows - 2, y=cols - 2)

            algo = self.view.control_panel.get_maze_gen_algorithm()
            if algo == "prim":
                self.maze = prim_maze_generation(
                    row=rows,
                    col=cols,
                    start_pos=start,
                    end_pos=end,
                )
            else:
                self.maze = maze_generation(
                    row=rows,
                    col=cols,
                    start_pos=start,
                    end_pos=end,
                )

            self._render_maze()
            self.view.control_panel.update_metrics(status="Đã sinh mê cung")

        except Exception as e:
            messagebox.showerror("Lỗi sinh mê cung", str(e))

    # ================================================================
    #  TÌM ĐƯỜNG ĐI
    # ================================================================

    def find_shortest_path(self) -> None:
        """Tìm đường đi ngắn nhất bằng BFS (có animation)."""
        self._solve_and_animate(bfs_solve, "BFS")

    def find_shortest_path_astar(self) -> None:
        """Tìm đường đi ngắn nhất bằng A* (có animation)."""
        self._solve_and_animate(a_star_solve, "A*")

    def find_shortest_path_dijkstra(self) -> None:
        """Tìm đường đi ngắn nhất bằng Dijkstra (có animation)."""
        self._solve_and_animate(dijkstra_solve, "Dijkstra")

    def solve_maze(self) -> None:
        """Tìm đường đi bằng thuật toán đã chọn trong bảng điều khiển."""
        if self.maze is None:
            messagebox.showwarning("Chưa có mê cung", "Vui lòng sinh hoặc nhập mê cung trước!")
            return

        algo = self.view.control_panel.get_solve_algorithm()
        if algo == "bfs":
            self.find_shortest_path()
        elif algo == "dfs":
            self.find_all_paths()
        elif algo == "astar":
            self.find_shortest_path_astar()
        elif algo == "dijkstra":
            self.find_shortest_path_dijkstra()

    def _solve_and_animate(self, solver_func, algo_name: str) -> None:
        """Phương thức dùng chung để giải mê cung và vẽ hoạt ảnh đường đi ngắn nhất."""
        if self.maze is None:
            messagebox.showwarning("Chưa có mê cung", "Vui lòng sinh hoặc nhập mê cung trước!")
            return

        # Dừng animation cũ nếu đang chạy
        self.view.maze_layout.stop_animation()

        try:
            # Xoá đường đi cũ trước khi tìm mới
            self._render_maze()

            start_time = time.perf_counter()
            robot = solver_func(self.maze)
            solve_elapsed = time.perf_counter() - start_time

            if robot.shortest_solution:
                final_elapsed = {"value": solve_elapsed}

                self.view.control_panel.update_metrics(
                    visited_count=len(robot.visited_order),
                    path_length=len(robot.shortest_solution),
                    runtime=solve_elapsed,
                    status=f"{algo_name} — Đang hiển thị...",
                )

                # Bước 1: Animation tô màu các ô đã duyệt
                visited_cells = [
                    (p.x, p.y, self.CELL_VISITED)
                    for p in robot.visited_order
                    if p != self.maze.start_pos and p != self.maze.end_pos
                ]

                # Bước 2: Animation tô màu đường đi ngắn nhất
                solution_cells = [
                    (p.x, p.y, self.CELL_SOLUTION)
                    for p in robot.shortest_solution
                    if p != self.maze.start_pos and p != self.maze.end_pos
                ]

                # Bước 3: Animation vẽ đường nối
                path_tuples = [(p.x, p.y) for p in robot.shortest_solution]

                def on_visited_done():
                    self.view.maze_layout.animate_solution_path_with_robot(
                        solution_cells,
                        path_tuples,
                        delay_ms=40,
                        on_cells_complete=on_solution_done,
                        on_complete=on_path_done,
                    )

                def on_solution_done():
                    final_elapsed["value"] = time.perf_counter() - start_time
                    self.view.control_panel.update_metrics(
                        visited_count=len(robot.visited_order),
                        path_length=len(robot.shortest_solution),
                        runtime=final_elapsed["value"],
                        status=f"{algo_name} — Đã chạm đích",
                    )

                def on_path_done():
                    self.view.control_panel.update_metrics(
                        visited_count=len(robot.visited_order),
                        path_length=len(robot.shortest_solution),
                        runtime=final_elapsed["value"],
                        status=f"{algo_name} — Tìm thấy đường ngắn nhất!",
                    )

                # Tính delay tự động: nhanh hơn nếu mê cung lớn
                visit_delay = max(5, min(50, 1000 // max(len(visited_cells), 1)))

                self.view.maze_layout.animate_cells(
                    visited_cells,
                    delay_ms=visit_delay,
                    on_complete=on_visited_done,
                )
            else:
                self.view.control_panel.update_metrics(
                    visited_count=len(robot.visited_order),
                    path_length=0,
                    runtime=solve_elapsed,
                    status=f"{algo_name} — Không tìm thấy đường đi!",
                )
                messagebox.showinfo("Kết quả", "Không tìm thấy đường đi!")

        except Exception as e:
            messagebox.showerror(f"Lỗi {algo_name}", str(e))

    def find_all_paths(self) -> None:
        """Tìm tất cả đường đi bằng DFS + Backtracking (có animation)."""
        if self.maze is None:
            messagebox.showwarning("Chưa có mê cung", "Vui lòng sinh hoặc nhập mê cung trước!")
            return

        # Dừng animation cũ nếu đang chạy
        self.view.maze_layout.stop_animation()

        try:
            # Xoá đường đi cũ
            self._render_maze()

            # DFS thay đổi grid (đánh dấu tường) nên dùng bản copy
            maze_copy = Maze(
                rows=self.maze.rows,
                cols=self.maze.cols,
                grid=copy.deepcopy(self.maze.grid),
                start_pos=self.maze.start_pos,
                end_pos=self.maze.end_pos,
            )

            possible_solutions: list[list[Point]] = []

            start_time = time.perf_counter()
            finding_valid_paths(
                maze=maze_copy,
                current_pos=maze_copy.start_pos,
                path=[],
                possible_solutions=possible_solutions,
            )
            solve_elapsed = time.perf_counter() - start_time

            if possible_solutions:
                # Tìm đường ngắn nhất trong tất cả đường đi
                shortest = min(possible_solutions, key=len)

                final_elapsed = {"value": solve_elapsed}

                # Tập hợp tất cả ô đã duyệt
                all_visited = set()
                for sol in possible_solutions:
                    for p in sol:
                        all_visited.add(p)

                self.view.control_panel.update_metrics(
                    visited_count=len(all_visited),
                    path_length=len(shortest),
                    runtime=solve_elapsed,
                    status=f"DFS — Đang hiển thị {len(possible_solutions)} đường đi...",
                )

                # Bước 1: Animation tô ô đã duyệt
                visited_cells = [
                    (p.x, p.y, self.CELL_VISITED)
                    for p in all_visited
                    if p != self.maze.start_pos and p != self.maze.end_pos
                ]

                # Bước 2: Animation tô đường ngắn nhất
                solution_cells = [
                    (p.x, p.y, self.CELL_SOLUTION)
                    for p in shortest
                    if p != self.maze.start_pos and p != self.maze.end_pos
                ]

                # Bước 3: Animation vẽ đường nối
                path_tuples = [(p.x, p.y) for p in shortest]

                def on_visited_done():
                    self.view.maze_layout.animate_solution_path_with_robot(
                        solution_cells,
                        path_tuples,
                        delay_ms=40,
                        on_cells_complete=on_solution_done,
                        on_complete=on_path_done,
                    )

                def on_solution_done():
                    final_elapsed["value"] = time.perf_counter() - start_time
                    self.view.control_panel.update_metrics(
                        visited_count=len(all_visited),
                        path_length=len(shortest),
                        runtime=final_elapsed["value"],
                        status=f"DFS — Đã chạm đích",
                    )

                def on_path_done():
                    self.view.control_panel.update_metrics(
                        visited_count=len(all_visited),
                        path_length=len(shortest),
                        runtime=final_elapsed["value"],
                        status=f"DFS — Tìm thấy {len(possible_solutions)} đường đi",
                    )

                visit_delay = max(5, min(50, 1000 // max(len(visited_cells), 1)))

                self.view.maze_layout.animate_cells(
                    visited_cells,
                    delay_ms=visit_delay,
                    on_complete=on_visited_done,
                )
            else:
                self.view.control_panel.update_metrics(
                    visited_count=0,
                    path_length=0,
                    runtime=solve_elapsed,
                    status="DFS — Không tìm thấy đường đi!",
                )
                messagebox.showinfo("Kết quả", "Không tìm thấy đường đi!")

        except Exception as e:
            messagebox.showerror("Lỗi DFS", str(e))

    # ================================================================
    #  XỬ LÝ CLICK CHUỘT
    # ================================================================

    def handle_left_click(self, row: int, col: int) -> None:
        """Xử lý click chuột trái dựa trên chế độ hiện tại."""
        mode = self.view.control_panel.get_mouse_mode()
        if mode == "wall":
            self.add_wall(row, col)
        elif mode == "point":
            self.set_start_point(row, col)

    def handle_right_click(self, row: int, col: int) -> None:
        """Xử lý click chuột phải dựa trên chế độ hiện tại."""
        mode = self.view.control_panel.get_mouse_mode()
        if mode == "wall":
            self.remove_wall(row, col)
        elif mode == "point":
            self.set_end_point(row, col)

    def set_start_point(self, row: int, col: int) -> None:
        if self.maze is None:
            return
        # Chỉ cho phép đặt ở ô đường đi
        if self.maze.grid[row][col] != self.CELL_WALL:
            self.maze.start_pos = Point(x=row, y=col)
            self.reset_paths()

    def set_end_point(self, row: int, col: int) -> None:
        if self.maze is None:
            return
        # Chỉ cho phép đặt ở ô đường đi
        if self.maze.grid[row][col] != self.CELL_WALL:
            self.maze.end_pos = Point(x=row, y=col)
            self.reset_paths()

    def add_wall(self, row: int, col: int) -> None:
        """Thêm tường tại ô (row, col)."""
        if self.maze is None:
            return

        p = Point(x=row, y=col)
        if p == self.maze.start_pos or p == self.maze.end_pos:
            return  # Không cho đặt tường lên start/end

        self.maze.grid[row][col] = 1
        self.view.maze_layout.update_cell(row, col, self.CELL_WALL)

    def remove_wall(self, row: int, col: int) -> None:
        """Xoá tường tại ô (row, col)."""
        if self.maze is None:
            return

        self.maze.grid[row][col] = 0
        self.view.maze_layout.update_cell(row, col, self.CELL_PATH)

    # ================================================================
    #  XOÁ ĐƯỜNG ĐI CŨ
    # ================================================================

    def reset_paths(self) -> None:
        """Xoá toàn bộ đường đi đã vẽ, giữ nguyên cấu trúc mê cung."""
        if self.maze is None:
            return

        self._render_maze()
        self.view.control_panel.update_metrics(status="Đã xoá đường đi")

    # ================================================================
    #  HELPER — Vẽ lại mê cung lên canvas
    # ================================================================

    def _render_maze(self) -> None:
        """Vẽ mê cung lên MazeLayout, bao gồm tô màu start/end."""
        if self.maze is None:
            return

        # Tạo bản copy grid để tô màu start/end mà không ảnh hưởng dữ liệu gốc
        display_grid = copy.deepcopy(self.maze.grid)

        start = self.maze.start_pos
        end = self.maze.end_pos

        display_grid[start.x][start.y] = self.CELL_START
        display_grid[end.x][end.y] = self.CELL_END

        self.view.maze_layout.draw_maze(display_grid)
