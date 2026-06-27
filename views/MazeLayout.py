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

    def __init__(self, parent: tk.Widget, cell_size: int = 28):
        super().__init__(parent, bg="white", padx=10, pady=10)

        self.cell_size = cell_size
        self.grid: list[list[int]] = []
        self.rect_matrix: list[list[int | None]] = []
        self.path_line_id = None

        self._event_handler: Callable[[str, int, int], None] | None = None

        self.canvas = tk.Canvas(
            self,
            bg="white",
            highlightthickness=1,
            highlightbackground="#DCDDE1",
        )
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas.bind("<Button-1>", self._handle_left_click)
        self.canvas.bind("<Button-3>", self._handle_right_click)

    def bind_event_handler(
        self,
        handler: Callable[[str, int, int], None],
    ) -> None:
        self._event_handler = handler

    def _emit(self, event_name: str, row: int, col: int) -> None:
        if self._event_handler:
            self._event_handler(event_name, row, col)

    def draw_maze(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.canvas.delete("all")
        self.path_line_id = None

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        width = cols * self.cell_size
        height = rows * self.cell_size

        self.canvas.config(
            width=width,
            height=height,
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
            width=5,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    def clear_final_path(self) -> None:
        if self.path_line_id:
            self.canvas.delete(self.path_line_id)
            self.path_line_id = None

    def _handle_left_click(self, event) -> None:
        row, col = self._event_to_cell(event)

        if self._is_inside(row, col):
            self._emit("add_wall", row, col)

    def _handle_right_click(self, event) -> None:
        row, col = self._event_to_cell(event)

        if self._is_inside(row, col):
            self._emit("remove_wall", row, col)

    def _event_to_cell(self, event) -> tuple[int, int]:
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        return row, col

    def _is_inside(self, row: int, col: int) -> bool:
        return (
            0 <= row < len(self.grid)
            and len(self.grid) > 0
            and 0 <= col < len(self.grid[0])
        )