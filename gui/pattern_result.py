from tkinter import *


class PatternResult(Frame):

    def __init__(self, parent: Tk) -> None:
        super(PatternResult, self).__init__(master=parent)

        Label(master=self, text="Pattern Result").pack()
        self.button_back = Button(master=self, text="Back",
                                  command=self.master.create_gui)
        self.button_back.pack()


if __name__ == "__main__":
    pass