from tkinter import filedialog, messagebox

from models.Maze import Maze
from models.Point import Point
from utils.FileProcessor import FileProcessor


class FileController:
    """Controller quản lý các thao tác xuất/nhập file."""

    def __init__(self, maze_controller) -> None:
        self.maze_controller = maze_controller

    def import_maze(self) -> None:
        """Nhập mê cung từ file JSON."""
        file_path = filedialog.askopenfilename(
            title="Chọn file mê cung JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if not file_path:
            return

        try:
            success, data = FileProcessor.read_json(file_path)

            if not success:
                messagebox.showerror("Lỗi đọc file", data)
                return

            self.maze_controller.maze = Maze(
                rows=data["rows"],
                cols=data["cols"],
                grid=data["grid"],
                start_pos=Point(x=data["start_pos"]["x"], y=data["start_pos"]["y"]),
                end_pos=Point(x=data["end_pos"]["x"], y=data["end_pos"]["y"]),
            )

            self.maze_controller.reset_paths()
            self.maze_controller.view.control_panel.update_metrics(status="Đã nhập mê cung từ file")

        except Exception as e:
            messagebox.showerror("Lỗi nhập mê cung", str(e))

    def save_maze(self) -> None:
        """Lưu mê cung hiện tại ra file JSON."""
        if self.maze_controller.maze is None:
            messagebox.showwarning("Chưa có mê cung", "Vui lòng sinh hoặc nhập mê cung trước!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Lưu mê cung",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if not file_path:
            return

        try:
            maze = self.maze_controller.maze
            data = {
                "rows": maze.rows,
                "cols": maze.cols,
                "grid": maze.grid,
                "start_pos": {"x": maze.start_pos.x, "y": maze.start_pos.y},
                "end_pos": {"x": maze.end_pos.x, "y": maze.end_pos.y},
            }

            success, msg = FileProcessor.write_json(file_path, data)

            if success:
                messagebox.showinfo("Thành công", "Đã lưu mê cung!")
                self.maze_controller.view.control_panel.update_metrics(status="Đã lưu mê cung")
            else:
                messagebox.showerror("Lỗi lưu file", msg)

        except Exception as e:
            messagebox.showerror("Lỗi lưu mê cung", str(e))
