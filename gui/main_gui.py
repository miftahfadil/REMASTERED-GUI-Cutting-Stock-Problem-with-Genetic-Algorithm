from tkinter import *
from typing import Dict
from typing import List
from typing import Tuple

from utils.theme import Colors
from .menu import MainMenu


class MainWindow(Tk):

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)

        self.title(string="Wasteless Cut")
        self.configure(bg=Colors.white)
        self._width = 1200
        self._height = 700
        self._frames: Dict[str, Frame] = {}

        self.resizable(width=False, height=False)
        self.centering_window()
        self.create_gui()

    def centering_window(self) -> None:
        _width = self._width
        _height = self._height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_corner = int((screen_width / 2) - (_width / 2))
        y_corner = int((screen_height / 2) - (_height / 2))
        self.geometry(f"{_width}x{_height}+{x_corner}+{y_corner}")
    
    def create_gui(self) -> None:
        self.switch_frame(name_frame="Menu", new_frame=MainMenu)
        

    def switch_frame(self, name_frame:str, new_frame: Frame) -> None:
        for frame in self._frames.values():
            frame.destroy()
        self._frames[name_frame] = new_frame(parent=self)
        self._frames[name_frame].pack(fill=BOTH, expand=TRUE)

    



if __name__ == "__main__":
    main_app = MainWindow()
    main_app.mainloop()
