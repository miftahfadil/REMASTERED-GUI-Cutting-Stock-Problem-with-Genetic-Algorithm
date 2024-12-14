from tkinter import *
from tkinter import ttk
from typing import Dict
from typing import List
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle

from algorithm.genetic_algorithm import genetic_algorithm

class PatternResult(Frame):

    def __init__(self, parent: Tk) -> None:
        super(PatternResult, self).__init__(master=parent)

        self.metadata: Dict[str, List[int]|List[float]|Any] = genetic_algorithm(len_stock_list=self.master.stocks,
                                                            len_product_list=self.master.products[2])
        # self.metadata = self.master.metadata

        self.create_gui()

    def create_gui(self) -> None:
        Label(master=self, text="Pattern Result").pack(fill=X)

        pattern_plot = PatternPlot(parent=self, bg="blue")
        pattern_plot.pack(fill=BOTH, expand=1)

        self.button_back = Button(master=self, text="Back",
                                  command=self.master.create_gui)
        self.button_back.pack(fill=X)

class PatternPlot(Frame):

    def __init__(self, parent: Tk, **kwargs) -> None:
        super(PatternPlot, self).__init__(master=parent, **kwargs)
        self.stocks: List[float] = self.master.metadata["len_stocks_list"].copy()
        self.num_used_stock: List[float] = self.master.metadata["num_used_stock"].copy()
        self.patterns: List[List[List[float]]] = self.master.metadata["patterns"].copy()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.create_scrollable()
        self.display_plot()

    def create_scrollable(self) -> None:
        self.canvas = Canvas(master=self)
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
        widget.pack(side=TOP, fill=BOTH, expand=1, anchor=NW, padx=10, pady=10)

    def create_cutting_pattern(self) -> Figure:
        fig, ax = plt.subplots(figsize=(10, 6))

        y_offset: float = 0.
        width: float = .3
        margin: float = .1
        for idx_stock, patterns_by_stock in enumerate(self.patterns):
            len_stock: float = self.stocks[idx_stock]

            for pattern in patterns_by_stock:
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
        
        ax.set_xlim(-margin, max(self.stocks) + 1)
        ax.set_ylim(-margin, sum(self.num_used_stock) * (width + margin) + 1)
        ax.set_xlabel("Length")
        ax.set_title("Cutting Pattern Representation")
        ax.set_aspect('equal')
        ax.axis('off')

        return fig


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