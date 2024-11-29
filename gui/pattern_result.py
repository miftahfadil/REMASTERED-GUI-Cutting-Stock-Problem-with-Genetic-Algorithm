from tkinter import *


class PatternResult(Frame):

    def __init__(self, parent: Tk) -> None:
        super(PatternResult, self).__init__(master=parent)

        Label(master=self, text="Pattern Result").pack()


if __name__ == "__main__":
    pass