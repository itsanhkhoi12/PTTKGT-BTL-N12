import tkinter as tk
from tkinter import ttk
from typing import Callable


class ControlPanel(tk.Frame):
    BG_COLOR = "#F8F9FA"
    TEXT_COLOR = "#212529"
    SUBTEXT_COLOR = "#343A40"
    BUTTON_BG = "#E9ECEF"
    BUTTON_ACTIVE_BG = "#DEE2E6"

    def __init__(self, parent: tk.Widget):
        super().__init__(
            parent,
            width=360,
            bg=self.BG_COLOR,
            padx=16,
            pady=16,
        )

        self.pack_propagate(False)
        self._event_handler: Callable[[str], None] | None = None

        self._build_ui()

    def bind_event_handler(self, handler: Callable[[str], None]) -> None:
        self._event_handler = handler

    def _emit(self, event_name: str) -> None:
        if self._event_handler:
            self._event_handler(event_name)

    def _build_ui(self) -> None:
        self._create_title("🎛️ BẢNG ĐIỀU KHIỂN", 14)

        self._build_maze_generation_section()
        self._separator()

        self._build_pathfinding_section()
        self._separator()

        self._build_file_section()
        self._separator()

        self._build_action_section()
        self._separator()

        self._build_metrics_section()

    def _build_maze_generation_section(self) -> None:
        self._create_section_title("📦 Sinh mê cung ngẫu nhiên")

        self.gen_rows_entry = self._create_labeled_entry(self, "Số hàng:", "21")
        self.gen_cols_entry = self._create_labeled_entry(self, "Số cột:", "21")

        point_frame = self._create_point_pair_frame(self)

        self.gen_start_row_entry, self.gen_start_col_entry = self._create_point_box(
            point_frame, "Điểm bắt đầu", "1", "1"
        )

        self.gen_end_row_entry, self.gen_end_col_entry = self._create_point_box(
            point_frame, "Điểm kết thúc", "19", "19"
        )

        self._create_button(
            text="Sinh mê cung",
            command=lambda: self._emit("generate_maze"),
        )

    def _build_pathfinding_section(self) -> None:
        self._create_section_title("🧭 Tìm đường đi")

        point_frame = self._create_point_pair_frame(self)

        self.find_start_row_entry, self.find_start_col_entry = self._create_point_box(
            point_frame, "Điểm bắt đầu", "1", "1"
        )

        self.find_end_row_entry, self.find_end_col_entry = self._create_point_box(
            point_frame, "Điểm kết thúc", "19", "19"
        )

        self._create_button(
            text="Hiển thị tất cả đường đi",
            command=lambda: self._emit("find_all_paths"),
        )

        self._create_button(
            text="Tìm đường ngắn nhất",
            command=lambda: self._emit("find_shortest_path"),
        )

    def _build_file_section(self) -> None:
        self._create_section_title("💾 Nhập / lưu mê cung")

        self._create_button(
            text="Nhập mê cung từ JSON",
            command=lambda: self._emit("import_maze"),
        )

        self._create_button(
            text="Lưu mê cung ra JSON",
            command=lambda: self._emit("save_maze"),
        )

    def _build_action_section(self) -> None:
        self._create_section_title("⚙️ Thao tác khác")

        self._create_button(
            text="Xóa đường đi cũ",
            command=lambda: self._emit("reset_paths"),
        )

    def _build_metrics_section(self) -> None:
        self._create_section_title("📈 Thông số đánh giá")

        self.lbl_visited = self._create_metric_label("Số ô đã duyệt: 0")
        self.lbl_length = self._create_metric_label("Độ dài đường đi: 0")
        self.lbl_time = self._create_metric_label("Thời gian chạy: 0.0000s")
        self.lbl_status = self._create_metric_label("Trạng thái: Sẵn sàng")

    def _create_title(self, text: str, size: int) -> None:
        tk.Label(
            self,
            text=text,
            font=("Arial", size, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        ).pack(anchor=tk.W, pady=(0, 16))

    def _create_section_title(self, text: str) -> None:
        tk.Label(
            self,
            text=text,
            font=("Arial", 11, "bold"),
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
        ).pack(anchor=tk.W, pady=(0, 8))

    def _create_labeled_entry(
        self,
        parent: tk.Widget,
        label: str,
        default: str,
    ) -> tk.Entry:
        tk.Label(
            parent,
            text=label,
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            font=("Arial", 10),
        ).pack(anchor=tk.W)

        entry = tk.Entry(
            parent,
            font=("Arial", 10),
            relief=tk.SOLID,
            bd=1,
        )
        entry.insert(0, default)
        entry.pack(fill=tk.X, pady=(2, 8))

        return entry

    def _create_point_pair_frame(self, parent: tk.Widget) -> tk.Frame:
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(fill=tk.X, pady=(4, 10))
        return frame

    def _create_point_box(
        self,
        parent: tk.Widget,
        title: str,
        default_row: str,
        default_col: str,
    ) -> tuple[tk.Entry, tk.Entry]:
        box = tk.LabelFrame(
            parent,
            text=title,
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Arial", 10, "bold"),
            padx=8,
            pady=6,
            bd=1,
            relief=tk.GROOVE,
        )
        box.pack(fill=tk.X, pady=(0, 8))

        row_entry = self._create_labeled_entry(box, "Hàng:", default_row)
        col_entry = self._create_labeled_entry(box, "Cột:", default_col)

        return row_entry, col_entry

    def _create_button(self, text: str, command: Callable[[], None]) -> None:
        tk.Button(
            self,
            text=text,
            command=command,
            font=("Arial", 10),
            bg=self.BUTTON_BG,
            fg=self.TEXT_COLOR,
            activebackground=self.BUTTON_ACTIVE_BG,
            activeforeground=self.TEXT_COLOR,
            relief=tk.FLAT,
            bd=1,
            pady=7,
            cursor="hand2",
        ).pack(fill=tk.X, pady=4)

    def _create_metric_label(self, text: str) -> tk.Label:
        label = tk.Label(
            self,
            text=text,
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            anchor=tk.W,
        )
        label.pack(fill=tk.X, pady=2)
        return label

    def _separator(self) -> None:
        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, pady=12)

    def get_generation_input(self) -> dict:
        return {
            "rows": int(self.gen_rows_entry.get()),
            "cols": int(self.gen_cols_entry.get()),
            "start_row": int(self.gen_start_row_entry.get()),
            "start_col": int(self.gen_start_col_entry.get()),
            "end_row": int(self.gen_end_row_entry.get()),
            "end_col": int(self.gen_end_col_entry.get()),
        }

    def get_pathfinding_input(self) -> dict:
        return {
            "start_row": int(self.find_start_row_entry.get()),
            "start_col": int(self.find_start_col_entry.get()),
            "end_row": int(self.find_end_row_entry.get()),
            "end_col": int(self.find_end_col_entry.get()),
        }

    def update_metrics(
        self,
        visited_count: int = 0,
        path_length: int = 0,
        runtime: float = 0.0,
        status: str = "Sẵn sàng",
    ) -> None:
        self.lbl_visited.config(text=f"Số ô đã duyệt: {visited_count}")
        self.lbl_length.config(text=f"Độ dài đường đi: {path_length}")
        self.lbl_time.config(text=f"Thời gian chạy: {runtime:.4f}s")
        self.lbl_status.config(text=f"Trạng thái: {status}")