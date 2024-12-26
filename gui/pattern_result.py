from tkinter import *
from tkinter import ttk
from typing import Dict
from typing import List
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle

from .widgets import ButtonThemed
from utils.theme import Colors
from utils.theme import Fonts
from algorithm.genetic_algorithm import genetic_algorithm


class PatternResult(Frame):

    def __init__(self, parent: Tk, bg:str = Colors.white, **kwargs) -> None:
        super(PatternResult, self).__init__(master=parent, bg=bg)

        self.metadata: Dict[str, List[int]|List[float]|Any] = genetic_algorithm(len_stock_list=self.master.stocks,
                                                            len_product_list=self.master.products[2])
        # self.metadata = self.master.metadata

        self.create_gui()

    def create_gui(self) -> None:
        Label(master=self, text="Pattern Result", font=Fonts.h1,
            bg=Colors.white, fg=Colors.green2).pack(fill=X, pady=(4, 24))

        pattern_plot = PatternPlot(parent=self)
        pattern_plot.pack(fill=BOTH, expand=1)

        self.button_back = ButtonThemed(parent=self, text="Back to Input Data",
                                    bg=Colors.yellow1, fg=Colors.white, command=self.master.create_gui)
        self.button_back.pack(fill=X, pady=(12, 0))

class PatternPlot(Frame):

    def __init__(self, parent: Widget, **kwargs) -> None:
        super(PatternPlot, self).__init__(master=parent, **kwargs)
        self.stocks: List[float] = self.master.metadata["len_stocks_list"].copy()
        self.num_used_stock: List[float] = self.master.metadata["num_used_stock"].copy()
        self.patterns: List[List[List[float]]] = self.master.metadata["patterns"].copy()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.create_scrollable()
        self.display_plot()
        self.display_stat()

    def create_scrollable(self) -> None:
        self.canvas = Canvas(master=self, height=500, width=700)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        y_scrollbar = ttk.Scrollbar(master=self, orient=VERTICAL, command=self.canvas.yview)
        y_scrollbar.grid(row=0, column=1, sticky=NS)

        x_scrollbar = ttk.Scrollbar(master=self, orient=HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.grid(row=1, column=0, sticky=EW)

        self.canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        self.inner_canvas = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner_canvas, anchor=NW)

        self.inner_canvas.bind("<Configure>", self.update_scroll_region)
    
    def update_scroll_region(self, e) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_plot(self) -> None:
        fig = self.create_cutting_pattern()
        canvas_plot = FigureCanvasTkAgg(fig, master=self.inner_canvas)
        canvas_plot.draw()
        widget = canvas_plot.get_tk_widget()
        widget.pack(fill=BOTH, anchor=N)

    def create_cutting_pattern(self) -> Figure:
        total_pattern: int = sum(self.num_used_stock)
        col_size: int = max(5, total_pattern * 2)
        fig, ax = plt.subplots(figsize=(7, col_size))

        digit = self.get_num_digits(num=max(self.stocks))

        y_offset: float = 0.
        width: float = 10 ** (digit - 1)
        margin: float = width / 2
        for idx_stock, patterns_by_stock in enumerate(self.patterns):
            
            len_stock: float = self.stocks[idx_stock]

            for pattern in patterns_by_stock:

                if len(pattern) == 0:
                    break

                ax.add_patch(Rectangle((0, y_offset), len_stock, width,
                                    edgecolor="black", facecolor='lightgrey', lw=1))
                x_offset: float = 0.
                for len_product in pattern:
                    len_label: str = str(len_product)
                    ax.add_patch(Rectangle((x_offset, y_offset), len_product, width,
                                       edgecolor="blue", facecolor='skyblue', lw=1))
                    ax.text((x_offset + (len_product / 2)), (y_offset + (width / 2)), len_label,
                            ha='center', va='center', fontsize=10)
                    
                    x_offset += len_product
                
                y_offset += (width + margin)
        
        x_bound: float = margin * .1
        y_bound: float = margin * 10
        ax.set_xlim(-x_bound, max(self.stocks) + x_bound)
        ax.set_ylim(-y_bound, y_offset)
        ax.set_title("Cutting Pattern Plot")
        # ax.set_aspect('equal')
        ax.axis('off')

        fig.tight_layout(pad = 2)

        return fig

    def display_stat(self) -> None:
        self.stat_frame = Frame(master=self)
        self.stat_frame.grid(row=0, column=2, rowspan=2)

        yield_rate : float = self.master.metadata["yield rate"] * 100
        pattern: List[List[List[float]]] = self.master.metadata["patterns"]

        Label(master=self.stat_frame, text="Pattern Stat").pack(padx=10, pady=4, anchor=N)

        Label(master=self.stat_frame, text="Used Stock Rate:").pack(padx=10, pady=4)
        Label(master=self.stat_frame, text=f"{yield_rate:.2f}%").pack(padx=10)

        Label(master=self.stat_frame, text="Unused Stock Rate:").pack(padx=10, pady=4)
        Label(master=self.stat_frame, text=f"{100-yield_rate:.2f}%").pack(padx=10)

        # ubah jadi textbox
        Label(master=self.stat_frame, text="Pattern").pack(padx=10, pady=4)
        Label(master=self.stat_frame, text=f"{pattern}", wraplength=80).pack(padx=10)


    @staticmethod
    def get_num_digits(num: float) -> int:
        str_num: str = str(int(num))
        return len(str_num)


if __name__ == "__main__":
    main = Tk()
    main.geometry("1000x500")
    main.resizable(False, False)

    main.metadata = {
        "len_stocks_list" : [3.0, 4.0, 6.0],
        "num_used_stock" : [1, 2, 1],
        "patterns" : [[[2.7]],[[2.2, 1.7], [2.2, 1.5]], [[3.5, 1.9]]]
    }

    main.create_gui = lambda : None


    pattern_plot = PatternResult(main)
    pattern_plot.pack(fill=BOTH, expand=1)

    main.mainloop()