import tkinter as tk
from typing import Callable


class MazeLayout(tk.Frame):
    COLOR_MAP = {
        0: "#FFFFFF",  # path
        1: "#212529",  # wall
        2: "#74B9FF",  # visited
        3: "#00B894",  # start
        4: "#D63031",  # end
        5: "#FDCB6E",  # final path
    }

    MIN_CELL_SIZE = 4
    MAX_CELL_SIZE = 60
    DEFAULT_CELL_SIZE = 28

    def __init__(self, parent: tk.Widget, cell_size: int = 28):
        super().__init__(parent, bg="white", padx=10, pady=10)

        self.cell_size = cell_size
        self.grid: list[list[int]] = []
        self.rect_matrix: list[list[int | None]] = []
        self.path_line_id = None

        # Animation state
        self._anim_after_id: str | None = None  # ID của after() đang chạy
        self._is_animating: bool = False

        self._event_handler: Callable[[str, int, int], None] | None = None

        # --- Scrollable canvas setup ---
        self._h_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self._v_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.canvas = tk.Canvas(
            self,
            bg="white",
            highlightthickness=1,
            highlightbackground="#DCDDE1",
            xscrollcommand=self._h_scrollbar.set,
            yscrollcommand=self._v_scrollbar.set,
        )

        self._h_scrollbar.config(command=self.canvas.xview)
        self._v_scrollbar.config(command=self.canvas.yview)

        self._v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # --- Bindings ---
        self.canvas.bind("<Button-1>", self._handle_left_click)
        self.canvas.bind("<Button-3>", self._handle_right_click)

        # Ctrl + cuộn chuột để zoom
        self.canvas.bind("<Control-MouseWheel>", self._handle_zoom)

        # Cuộn chuột bình thường để scroll dọc
        self.canvas.bind("<MouseWheel>", self._handle_scroll)
        # Shift + cuộn để scroll ngang
        self.canvas.bind("<Shift-MouseWheel>", self._handle_scroll_horizontal)

    def bind_event_handler(
        self,
        handler: Callable[[str, int, int], None],
    ) -> None:
        self._event_handler = handler

    def _emit(self, event_name: str, row: int, col: int) -> None:
        if self._event_handler:
            self._event_handler(event_name, row, col)

    # ================================================================
    #  ZOOM
    # ================================================================

    def _handle_zoom(self, event) -> None:
        """Ctrl + cuộn chuột để zoom to/nhỏ mê cung."""
        if not self.grid:
            return

        old_size = self.cell_size

        if event.delta > 0:
            # Zoom in
            self.cell_size = min(self.cell_size + 2, self.MAX_CELL_SIZE)
        else:
            # Zoom out
            self.cell_size = max(self.cell_size - 2, self.MIN_CELL_SIZE)

        if self.cell_size != old_size:
            self._redraw_current_grid()

    def _handle_scroll(self, event) -> None:
        """Cuộn chuột bình thường để scroll dọc."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _handle_scroll_horizontal(self, event) -> None:
        """Shift + cuộn chuột để scroll ngang."""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _redraw_current_grid(self) -> None:
        """Vẽ lại toàn bộ mê cung với cell_size mới (dùng khi zoom)."""
        if self.grid:
            self.draw_maze(self.grid)

    # ================================================================
    #  VẼ MÊ CUNG
    # ================================================================

    def draw_maze(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.canvas.delete("all")
        self.path_line_id = None

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        width = cols * self.cell_size
        height = rows * self.cell_size

        self.canvas.config(
            scrollregion=(0, 0, width, height),
        )

        self.rect_matrix = [[None for _ in range(cols)] for _ in range(rows)]

        for row in range(rows):
            for col in range(cols):
                self._draw_cell(row, col, grid[row][col])

    def _draw_cell(self, row: int, col: int, state: int) -> None:
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        rect_id = self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=self.COLOR_MAP.get(state, "#FFFFFF"),
            outline="#DCDDE1",
        )

        self.rect_matrix[row][col] = rect_id

    def update_cell(self, row: int, col: int, state: int) -> None:
        if not self._is_inside(row, col):
            return

        self.grid[row][col] = state

        rect_id = self.rect_matrix[row][col]
        if rect_id is None:
            return

        self.canvas.itemconfig(
            rect_id,
            fill=self.COLOR_MAP.get(state, "#FFFFFF"),
        )

    def draw_final_path(self, path: list[tuple[int, int]]) -> None:
        if not path:
            return

        self.clear_final_path()

        points = []
        for row, col in path:
            points.append(
                (
                    col * self.cell_size + self.cell_size // 2,
                    row * self.cell_size + self.cell_size // 2,
                )
            )

        flat_points = [coord for point in points for coord in point]

        self.path_line_id = self.canvas.create_line(
            flat_points,
            fill="#FF4757",
            width=max(2, self.cell_size // 5),
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    def clear_final_path(self) -> None:
        if self.path_line_id:
            self.canvas.delete(self.path_line_id)
            self.path_line_id = None

    # ================================================================
    #  ANIMATION
    # ================================================================

    @property
    def is_animating(self) -> bool:
        return self._is_animating

    def stop_animation(self) -> None:
        """Dừng animation đang chạy."""
        if self._anim_after_id is not None:
            self.after_cancel(self._anim_after_id)
            self._anim_after_id = None
        self._is_animating = False

    def animate_cells(
        self,
        cells: list[tuple[int, int, int]],
        delay_ms: int = 20,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        """
        Tô màu từng ô một theo thứ tự, tạo hiệu ứng animation.

        Args:
            cells: Danh sách (row, col, state) cần tô.
            delay_ms: Thời gian chờ giữa mỗi ô (ms).
            on_complete: Callback khi animation hoàn tất.
        """
        self.stop_animation()
        self._is_animating = True
        self._animate_cells_step(cells, 0, delay_ms, on_complete)

    def _animate_cells_step(
        self,
        cells: list[tuple[int, int, int]],
        index: int,
        delay_ms: int,
        on_complete: Callable[[], None] | None,
    ) -> None:
        """Bước đệ quy của animation tô màu ô."""
        if not self._is_animating:
            return

        if index >= len(cells):
            self._is_animating = False
            self._anim_after_id = None
            if on_complete:
                on_complete()
            return

        row, col, state = cells[index]
        self.update_cell(row, col, state)

        self._anim_after_id = self.after(
            delay_ms,
            self._animate_cells_step,
            cells,
            index + 1,
            delay_ms,
            on_complete,
        )

    def animate_path_line(
        self,
        path: list[tuple[int, int]],
        delay_ms: int = 40,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        """
        Vẽ đường đi ngắn nhất từng đoạn một (animation).

        Args:
            path: Danh sách (row, col) tạo thành đường đi.
            delay_ms: Thời gian chờ giữa mỗi đoạn (ms).
            on_complete: Callback khi animation hoàn tất.
        """
        self.clear_final_path()

        if len(path) < 2:
            if on_complete:
                on_complete()
            return

        self._is_animating = True
        self._path_segments: list[int] = []
        self._animate_line_step(path, 1, delay_ms, on_complete)

    def _animate_line_step(
        self,
        path: list[tuple[int, int]],
        index: int,
        delay_ms: int,
        on_complete: Callable[[], None] | None,
    ) -> None:
        """Bước đệ quy vẽ từng đoạn đường."""
        if not self._is_animating:
            return

        if index >= len(path):
            self._is_animating = False
            self._anim_after_id = None
            if on_complete:
                on_complete()
            return

        r1, c1 = path[index - 1]
        r2, c2 = path[index]

        x1 = c1 * self.cell_size + self.cell_size // 2
        y1 = r1 * self.cell_size + self.cell_size // 2
        x2 = c2 * self.cell_size + self.cell_size // 2
        y2 = r2 * self.cell_size + self.cell_size // 2

        seg_id = self.canvas.create_line(
            x1, y1, x2, y2,
            fill="#FF4757",
            width=max(2, self.cell_size // 5),
            capstyle=tk.ROUND,
        )
        self._path_segments.append(seg_id)

        self._anim_after_id = self.after(
            delay_ms,
            self._animate_line_step,
            path,
            index + 1,
            delay_ms,
            on_complete,
        )

    # ================================================================
    #  CLICK HANDLERS
    # ================================================================

    def _handle_left_click(self, event) -> None:
        row, col = self._event_to_cell(event)

        if self._is_inside(row, col):
            self._emit("left_click", row, col)

    def _handle_right_click(self, event) -> None:
        row, col = self._event_to_cell(event)

        if self._is_inside(row, col):
            self._emit("right_click", row, col)

    def _event_to_cell(self, event) -> tuple[int, int]:
        # Chuyển đổi toạ độ canvas (có tính scroll offset)
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        col = int(canvas_x) // self.cell_size
        row = int(canvas_y) // self.cell_size
        return row, col

    def _is_inside(self, row: int, col: int) -> bool:
        return (
            0 <= row < len(self.grid)
            and len(self.grid) > 0
            and 0 <= col < len(self.grid[0])
        )