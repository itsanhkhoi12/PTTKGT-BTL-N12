import tkinter as tk
from tkinter import ttk
import random
import time
import heapq
from collections import deque

# 1. Định nghĩa trạng thái và bảng màu trực quan
PATH = 0        # Đường đi (Trắng)
WALL = 1        # Tường (Xám đậm)
START = 2       # Điểm bắt đầu A (Xanh lá)
END = 3         # Điểm đích B (Đỏ)
VISITED = 4     # Ô đã duyệt qua (Vàng nhạt)
CURRENT_PATH = 5  # Đường đi hiện tại của DFS đang thử nghiệm (Xanh dương nhạt)

COLOR_MAP = {
    PATH: "#FFFFFF",
    WALL: "#2C3E50",
    START: "#2ECC71",
    END: "#E74C3C",
    VISITED: "#F8EFBA",      # Vàng nhạt nhã nhặn hơn, không bị chói
    CURRENT_PATH: "#AED6F1"  # Xanh dương nhạt cho các ô đang nằm trong Stack/Queue
}


class AdvancedMazeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống trực quan hóa thuật toán Tìm Đường cao cấp")
        self.root.geometry("1000x620")

        # Cấu hình kích thước mê cung (Có thể tăng lên kích thước lớn)
        self.rows = 15
        self.cols = 20
        self.cell_size = 32
        self.matrix = []
        self.rect_matrix = [[None for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.path_line_id = None  # Lưu ID của sợi dây đường đi kết quả

        # --- LAYOUT CHÍNH ---
        self.control_frame = tk.Frame(
            root, width=280, bg="#F5F6FA", padx=15, pady=15)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.maze_frame = tk.Frame(root, bg="white", padx=10, pady=10)
        self.maze_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.create_control_panel()

        self.canvas = tk.Canvas(
            self.maze_frame,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white", highlightthickness=1, highlightbackground="#DCDDE1"
        )
        self.canvas.pack(expand=True)

        self.generate_random_maze()

    def create_control_panel(self):
        tk.Label(self.control_frame, text="BẢNG ĐIỀU KHIỂN", font=(
            "Arial", 14, "bold"), bg="#F5F6FA", fg="#2F3640").pack(pady=(0, 15))

        # 1. Bộ chọn thuật toán (Đã thêm A*)
        tk.Label(self.control_frame, text="Chọn thuật toán:",
                 font=("Arial", 11), bg="#F5F6FA").pack(anchor=tk.W)
        self.algo_box = ttk.Combobox(self.control_frame, values=[
            "Depth-First Search (DFS)",
            "Breadth-First Search (BFS)",
            "A* Search (Tối ưu nhất)"
        ], state="readonly", font=("Arial", 10))
        self.algo_box.pack(fill=tk.X, pady=(0, 12))
        self.algo_box.current(2)  # Mặc định chọn luôn A* cho xịn

        # 2. Thanh chỉnh tốc độ mô phỏng (Nâng cấp UX)
        tk.Label(self.control_frame, text="Tốc độ mô phỏng (giây/bước):",
                 font=("Arial", 11), bg="#F5F6FA").pack(anchor=tk.W)
        self.speed_slider = tk.Scale(self.control_frame, from_=0.001, to=0.15,
                                     resolution=0.005, orient=tk.HORIZONTAL, bg="#F5F6FA", bd=0)
        self.speed_slider.set(0.02)  # Tốc độ mặc định chạy khá nhanh
        self.speed_slider.pack(fill=tk.X, pady=(0, 15))

        # 3. Các nút điều hướng
        self.btn_gen = tk.Button(self.control_frame, text="🎲 Sinh mê cung ngẫu nhiên", command=self.generate_random_maze, font=(
            "Arial", 10), bg="#353B48", fg="white", pady=6, bd=0, cursor="hand2")
        self.btn_gen.pack(fill=tk.X, pady=4)

        self.btn_start = tk.Button(self.control_frame, text="▶️ Bắt đầu tìm đường", command=self.start_pathfinding, font=(
            "Arial", 10, "bold"), bg="#4CD137", fg="white", pady=6, bd=0, cursor="hand2")
        self.btn_start.pack(fill=tk.X, pady=4)

        self.btn_reset = tk.Button(self.control_frame, text="🔄 Xóa đường đi cũ", command=self.reset_maze_paths, font=(
            "Arial", 10), bg="#E1B12C", fg="white", pady=6, bd=0, cursor="hand2")
        self.btn_reset.pack(fill=tk.X, pady=4)

        ttk.Separator(self.control_frame, orient='horizontal').pack(
            fill=tk.X, pady=15)

        # 4. Bảng thông số hiệu năng
        tk.Label(self.control_frame, text="THÔNG SỐ ĐÁNH GIÁ", font=(
            "Arial", 12, "bold"), bg="#F5F6FA", fg="#2F3640").pack(pady=(0, 10))
        self.lbl_visited = tk.Label(self.control_frame, text="Số ô đã duyệt: 0", font=(
            "Arial", 11), bg="#F5F6FA", anchor=tk.W)
        self.lbl_visited.pack(fill=tk.X, pady=2)
        self.lbl_length = tk.Label(self.control_frame, text="Độ dài đường đi: 0 ô", font=(
            "Arial", 11), bg="#F5F6FA", anchor=tk.W)
        self.lbl_length.pack(fill=tk.X, pady=2)
        self.lbl_time = tk.Label(self.control_frame, text="Thời gian chạy: 0.0000s", font=(
            "Arial", 11), bg="#F5F6FA", anchor=tk.W)
        self.lbl_time.pack(fill=tk.X, pady=2)
        self.lbl_status = tk.Label(self.control_frame, text="Trạng thái: Sẵn sàng", font=(
            "Arial", 11, "italic"), fg="#4CD137", bg="#F5F6FA", anchor=tk.W)
        self.lbl_status.pack(fill=tk.X, pady=10)

    def draw_maze_on_canvas(self):
        self.canvas.delete("all")
        self.path_line_id = None
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = COLOR_MAP[self.matrix[r][c]]
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="#EEDDCC" if color == "#FFFFFF" else "#DCDDE1")
                self.rect_matrix[r][c] = rect_id

    def generate_random_maze(self):
        # Khung viền ngoài là tường, bên trong rải 25% tường ngẫu nhiên để mê cung thông thoáng hơn
        self.matrix = [[WALL if (r == 0 or r == self.rows-1 or c == 0 or c == self.cols-1 or random.random() < 0.25) else PATH
                        for c in range(self.cols)] for r in range(self.rows)]

        self.start_pos = (1, 1)
        self.end_pos = (self.rows - 2, self.cols - 2)

        self.matrix[self.start_pos[0]][self.start_pos[1]] = START
        self.matrix[self.end_pos[0]][self.end_pos[1]] = END

        # Mở đường thông thoáng quanh điểm đầu và cuối
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 < self.start_pos[0]+dr < self.rows-1 and 0 < self.start_pos[1]+dc < self.cols-1:
                self.matrix[self.start_pos[0]+dr][self.start_pos[1]+dc] = PATH
            if 0 < self.end_pos[0]+dr < self.rows-1 and 0 < self.end_pos[1]+dc < self.cols-1:
                self.matrix[self.end_pos[0]+dr][self.end_pos[1]+dc] = PATH

        self.clear_stats()
        self.draw_maze_on_canvas()

    def reset_maze_paths(self):
        if self.path_line_id:
            self.canvas.delete(self.path_line_id)
            self.path_line_id = None
        for r in range(self.rows):
            for c in range(self.cols):
                if self.matrix[r][c] in (VISITED, CURRENT_PATH):
                    self.matrix[r][c] = PATH
        self.clear_stats()
        self.draw_maze_on_canvas()

    def clear_stats(self):
        self.lbl_visited.config(text="Số ô đã duyệt: 0")
        self.lbl_length.config(text="Độ dài đường đi: 0 ô")
        self.lbl_time.config(text="Thời gian chạy: 0.0000s")
        self.lbl_status.config(text="Trạng thái: Sẵn sàng", fg="#4CD137")

    def update_cell_color(self, r, c, state_type):
        """Cập nhật giao diện động, lấy thời gian delay từ thanh trượt Slider"""
        if (r, c) == self.start_pos or (r, c) == self.end_pos:
            return
        self.matrix[r][c] = state_type
        self.canvas.itemconfig(
            self.rect_matrix[r][c], fill=COLOR_MAP[state_type])
        self.root.update()
        time.sleep(self.speed_slider.get())  # Tốc độ động từ Slider

    def draw_final_path_line(self, path):
        """NÂNG CẤP CỐT LÕI: Vẽ sợi dây kết quả chạy xuyên qua tâm các ô vuông"""
        if not path:
            return

        points = []
        # Điểm bắt đầu A
        points.append((self.start_pos[1] * self.cell_size + self.cell_size //
                      2, self.start_pos[0] * self.cell_size + self.cell_size // 2))
        # Các ô trung gian trong hành trình
        for r, c in path:
            points.append((c * self.cell_size + self.cell_size //
                          2, r * self.cell_size + self.cell_size // 2))
        # Điểm đích B
        points.append((self.end_pos[1] * self.cell_size + self.cell_size //
                      2, self.end_pos[0] * self.cell_size + self.cell_size // 2))

        # Làm phẳng mảng tọa độ để truyền vào hàm create_line
        flat_points = [coord for pt in points for coord in pt]

        # Vẽ một đường line màu đỏ cam (Neon) cực kỳ rõ ràng đè lên trên nền lưới
        self.path_line_id = self.canvas.create_line(
            flat_points,
            fill="#FF4757",
            width=5,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND
        )

    def start_pathfinding(self):
        self.reset_maze_paths()
        selected_algo = self.algo_box.get()
        self.lbl_status.config(
            text=f"Đang chạy {selected_algo}...", fg="#00A8FF")

        self.btn_start.config(state=tk.DISABLED)
        self.btn_gen.config(state=tk.DISABLED)

        start_time = time.time()

        if "DFS" in selected_algo:
            success, visited_count, path = self.run_dfs()
        elif "BFS" in selected_algo:
            success, visited_count, path = self.run_bfs()
        else:
            success, visited_count, path = self.run_astar()

        end_time = time.time()

        self.lbl_time.config(
            text=f"Thời gian chạy: {end_time - start_time:.4f}s")
        self.lbl_visited.config(text=f"Số ô đã duyệt: {visited_count}")

        if success:
            self.lbl_status.config(
                text="Tìm thấy đường đi tối ưu!", fg="#4CD137")
            self.lbl_length.config(text=f"Độ dài đường đi: {len(path) + 1} ô")
            self.draw_final_path_line(path)  # Vẽ sợi chỉ đỏ chỉ đường rõ ràng
        else:
            self.lbl_status.config(
                text="Không tồn tại đường đi!", fg="#FF4757")
            self.lbl_length.config(text="Độ dài đường đi: 0 ô")

        self.btn_start.config(state=tk.NORMAL)
        self.btn_gen.config(state=tk.NORMAL)

    def run_dfs(self):
        stack = [self.start_pos]
        visited = set([self.start_pos])
        parent = {}
        visited_counter = 0

        while stack:
            curr = stack[-1]
            if curr == self.end_pos:
                return True, visited_counter, self.reconstruct_path(parent)

            r, c = curr
            has_neighbor = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if self.matrix[nr][nc] != WALL and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    stack.append((nr, nc))
                    visited_counter += 1
                    self.lbl_visited.config(
                        text=f"Số ô đã duyệt: {visited_counter}")
                    self.update_cell_color(nr, nc, CURRENT_PATH)
                    has_neighbor = True
                    break
            if not has_neighbor:
                back = stack.pop()
                self.update_cell_color(
                    back[0], backtrack_node := back[1], VISITED)
        return False, visited_counter, []

    def run_bfs(self):
        queue = deque([self.start_pos])
        visited = set([self.start_pos])
        parent = {}
        visited_counter = 0

        while queue:
            curr = queue.popleft()
            if curr == self.end_pos:
                return True, visited_counter, self.reconstruct_path(parent)

            r, c = curr
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if self.matrix[nr][nc] != WALL and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    queue.append((nr, nc))
                    visited_counter += 1
                    self.lbl_visited.config(
                        text=f"Số ô đã duyệt: {visited_counter}")
                    self.update_cell_color(nr, nc, VISITED)
        return False, visited_counter, []

    def run_astar(self):
        """THUẬT TOÁN NÂNG CẤP A* (Sử dụng hàng đợi ưu tiên heapq)"""
        def heuristic(p1, p2):
            # Khoảng cách Manhattan từ ô hiện tại tới đích B
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        count = 0
        # Lưu: (f_score, count, tọa_độ_hiện_tại)
        open_set = []
        heapq.heappush(open_set, (0, count, self.start_pos))

        parent = {}
        g_score = {(r, c): float("inf") for r in range(self.rows)
                   for c in range(self.cols)}
        g_score[self.start_pos] = 0

        f_score = {(r, c): float("inf") for r in range(self.rows)
                   for c in range(self.cols)}
        f_score[self.start_pos] = heuristic(self.start_pos, self.end_pos)

        open_set_hash = {self.start_pos}
        visited_counter = 0

        while open_set:
            curr = heapq.heappop(open_set)[2]
            open_set_hash.remove(curr)

            if curr == self.end_pos:
                return True, visited_counter, self.reconstruct_path(parent)

            r, c = curr
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if self.matrix[nr][nc] != WALL:
                    temp_g_score = g_score[curr] + 1

                    if temp_g_score < g_score.get((nr, nc), float("inf")):
                        parent[(nr, nc)] = curr
                        g_score[(nr, nc)] = temp_g_score
                        f_score[(nr, nc)] = temp_g_score + \
                            heuristic((nr, nc), self.end_pos)

                        if (nr, nc) not in open_set_hash:
                            count += 1
                            heapq.heappush(
                                open_set, (f_score[(nr, nc)], count, (nr, nc)))
                            open_set_hash.add((nr, nc))
                            visited_counter += 1
                            self.lbl_visited.config(
                                text=f"Số ô đã duyệt: {visited_counter}")
                            self.update_cell_color(nr, nc, VISITED)

        return False, visited_counter, []

    def reconstruct_path(self, parent):
        path = []
        curr = self.end_pos
        while curr in parent:
            curr = parent[curr]
            if curr != self.start_pos:
                path.append(curr)
        path.reverse()
        return path


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedMazeVisualizer(root)
    root.mainloop()
