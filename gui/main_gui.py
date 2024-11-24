from tkinter import *


class MainWindow(Tk):

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)

        self.title(string="AppName")
        self._width = 900
        self._height = 500

        self.resizable(width=False, height=False)
        self.centering_window()

    def centering_window(self) -> None:
        _width = self._width
        _height = self._height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_corner = int((screen_width / 2) - (_width / 2))
        y_corner = int((screen_height / 2) - (_height / 2))
        self.geometry(f"{_width}x{_height}+{x_corner}+{y_corner}")



if __name__ == "__main__":
    main_app = MainWindow()
    main_app.mainloop()
