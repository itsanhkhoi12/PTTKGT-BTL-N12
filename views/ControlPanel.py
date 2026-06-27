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
        )

        self.pack_propagate(False)
        self._event_handler: Callable[[str], None] | None = None
        
        self.mouse_mode = tk.StringVar(value="wall")

        # --- Scrollable setup ---
        self._canvas = tk.Canvas(self, bg=self.BG_COLOR, highlightthickness=0)
        self._scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._inner_frame = tk.Frame(self._canvas, bg=self.BG_COLOR, padx=16, pady=16)

        self._inner_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )

        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._inner_frame, anchor="nw"
        )

        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Đồng bộ chiều rộng inner_frame với canvas
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        # Hỗ trợ cuộn bằng chuột
        self._inner_frame.bind("<Enter>", self._bind_mousewheel)
        self._inner_frame.bind("<Leave>", self._unbind_mousewheel)

        self._build_ui()

    def _on_canvas_configure(self, event) -> None:
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _bind_mousewheel(self, event) -> None:
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event) -> None:
        self._canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_event_handler(self, handler: Callable[[str], None]) -> None:
        self._event_handler = handler

    def _emit(self, event_name: str) -> None:
        if self._event_handler:
            self._event_handler(event_name)

    def _build_ui(self) -> None:
        self._create_title("🎛️ BẢNG ĐIỀU KHIỂN", 14)

        self._build_mouse_mode_section()
        self._separator()

        self._build_maze_generation_section()
        self._separator()

        self._build_pathfinding_section()
        self._separator()

        self._build_file_section()
        self._separator()

        self._build_action_section()
        self._separator()

        self._build_metrics_section()

    def _build_mouse_mode_section(self) -> None:
        self._create_section_title("🖱️ Chế độ chuột")
        
        frame = tk.Frame(self._inner_frame, bg=self.BG_COLOR)
        frame.pack(fill=tk.X, pady=(4, 8))
        
        tk.Radiobutton(
            frame, text="🧱 Vẽ tường\n(Trái: Thêm, Phải: Xoá)", 
            variable=self.mouse_mode, value="wall",
            bg=self.BUTTON_BG, fg=self.TEXT_COLOR, 
            selectcolor="#D1D8E0", activebackground=self.BUTTON_ACTIVE_BG, 
            cursor="hand2", indicatoron=False, 
            relief=tk.FLAT, bd=1, padx=10, pady=8, font=("Arial", 10)
        ).pack(fill=tk.X, pady=(0, 4))
        
        tk.Radiobutton(
            frame, text="📍 Đặt điểm\n(Trái: Bắt đầu, Phải: Đích)", 
            variable=self.mouse_mode, value="point",
            bg=self.BUTTON_BG, fg=self.TEXT_COLOR, 
            selectcolor="#D1D8E0", activebackground=self.BUTTON_ACTIVE_BG, 
            cursor="hand2", indicatoron=False, 
            relief=tk.FLAT, bd=1, padx=10, pady=8, font=("Arial", 10)
        ).pack(fill=tk.X)

    def _build_maze_generation_section(self) -> None:
        self._create_section_title("📦 Sinh mê cung ngẫu nhiên")

        self.gen_rows_entry = self._create_labeled_entry(self._inner_frame, "Số hàng:", "21")
        self.gen_cols_entry = self._create_labeled_entry(self._inner_frame, "Số cột:", "21")

        self._create_button(
            text="Sinh mê cung",
            command=lambda: self._emit("generate_maze"),
        )

    def _build_pathfinding_section(self) -> None:
        self._create_section_title("🧭 Tìm đường đi")

        self._create_button(
            text="Tìm đường theo DFS",
            command=lambda: self._emit("find_all_paths"),
        )

        self._create_button(
            text="Tìm đường theo BFS",
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
            self._inner_frame,
            text=text,
            font=("Arial", size, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        ).pack(anchor=tk.W, pady=(0, 16))

    def _create_section_title(self, text: str) -> None:
        tk.Label(
            self._inner_frame,
            text=text,
            font=("Arial", 11, "bold"),
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
        ).pack(anchor=tk.W, pady=(0, 8))

    def _create_inline_entries(
    self,
    parent: tk.Widget,
    fields: list[tuple[str, str]],
) -> list[tk.Entry]:
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(fill=tk.X, pady=(2, 4))

        entries: list[tk.Entry] = []

        for label, default in fields:
            tk.Label(
                frame,
                text=label,
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR,
                font=("Arial", 10),
            ).pack(side=tk.LEFT)

            entry = tk.Entry(
                frame,
                width=5,
                font=("Arial", 10),
                relief=tk.SOLID,
                bd=1,
                justify="center",
            )
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, padx=(5, 12))

            entries.append(entry)

        return entries

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

        row_entry, col_entry = self._create_inline_entries(
            parent=box,
            fields=[
                ("Hàng:", default_row),
                ("Cột:", default_col),
            ],
        )

        return row_entry, col_entry

    def _create_button(self, text: str, command: Callable[[], None]) -> None:
        tk.Button(
            self._inner_frame,
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
            self._inner_frame,
            text=text,
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            anchor=tk.W,
        )
        label.pack(fill=tk.X, pady=2)
        return label

    def _separator(self) -> None:
        ttk.Separator(self._inner_frame, orient="horizontal").pack(fill=tk.X, pady=12)

    def get_generation_input(self) -> dict:
        return {
            "rows": int(self.gen_rows_entry.get()),
            "cols": int(self.gen_cols_entry.get()),
        }

    def get_mouse_mode(self) -> str:
        return self.mouse_mode.get()

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