from tkinter import *
from typing import Dict
from typing import List
from typing import Any

from algorithm.genetic_algorithm import genetic_algorithm

class PatternResult(Frame):

    def __init__(self, parent: Tk) -> None:
        super(PatternResult, self).__init__(master=parent)

        metadata: Dict[str, List[int]|List[float]|Any] = genetic_algorithm(len_stock_list=self.master.stocks,
                                                            len_product_list=self.master.products[2])
        print(metadata)

        self.create_gui()

    def create_gui(self) -> None:
        Label(master=self, text="Pattern Result").pack()
        self.button_back = Button(master=self, text="Back",
                                  command=self.master.create_gui)
        self.button_back.pack()


if __name__ == "__main__":
    pass