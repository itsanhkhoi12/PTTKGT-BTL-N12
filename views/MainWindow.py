import tkinter as tk
from typing import Callable

from views.ControlPanel import ControlPanel
from views.MazeLayout import MazeLayout


class MainWindow:
    APP_TITLE = "🧩 Ứng dụng Sinh mê cung & Tìm đường đi"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.controller = None

        self.control_panel: ControlPanel | None = None
        self.maze_layout: MazeLayout | None = None

        self._configure_window()
        self._build_layout()
        self._bind_view_events()

    def _configure_window(self) -> None:
        self.root.title(self.APP_TITLE)
        self._set_fullscreen()

    def _build_layout(self) -> None:
        self.control_panel = ControlPanel(parent=self.root)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.maze_layout = MazeLayout(parent=self.root)
        self.maze_layout.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def _bind_view_events(self) -> None:
        self.control_panel.bind_event_handler(self._handle_control_event)
        self.maze_layout.bind_event_handler(self._handle_maze_event)

    def set_controller(self, controller) -> None:
        self.controller = controller

    def _handle_control_event(self, event_name: str) -> None:
        if self.controller is None:
            return

        actions: dict[str, Callable[[], None]] = {
            "generate_maze": self.controller.generate_maze,
            "import_maze": self.controller.import_maze,
            "save_maze": self.controller.save_maze,
            "find_all_paths": self.controller.find_all_paths,
            "find_shortest_path": self.controller.find_shortest_path,
            "reset_paths": self.controller.reset_paths,
        }

        action = actions.get(event_name)

        if action is not None:
            action()

    def _handle_maze_event(self, event_name: str, row: int, col: int) -> None:
        if self.controller is None:
            return

        actions: dict[str, Callable[[int, int], None]] = {
            "add_wall": self.controller.add_wall,
            "remove_wall": self.controller.remove_wall,
        }

        action = actions.get(event_name)

        if action is not None:
            action(row, col)

    def _set_fullscreen(self) -> None:
        try:
            self.root.state("zoomed")
            return
        except tk.TclError:
            pass

        try:
            self.root.attributes("-zoomed", True)
            return
        except tk.TclError:
            pass

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")