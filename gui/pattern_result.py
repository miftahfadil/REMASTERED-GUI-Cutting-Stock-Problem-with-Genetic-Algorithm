from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showinfo
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
from utils.theme import darken_hex_color
from algorithm.genetic_algorithm import genetic_algorithm


class PatternResult(Frame):

    def __init__(self, parent: Tk, bg:str = Colors.white, **kwargs) -> None:
        super(PatternResult, self).__init__(master=parent, bg=bg)

        self.raw_data: Dict[str, List[int]|List[float]|Any] = {
            "len_stocks_list" : self.master.stocks[0],
            "stock_color_label" : self.master.stocks[1],
            "len_products" : self.master.products[0],
            "len_products_list" : self.master.products[2],
            "product_color_label" : self.master.products[3]
        }
        self.metadata: Dict[str, List[int]|List[float]|Any] = genetic_algorithm(len_stock_list=self.raw_data["len_stocks_list"],
                                                            len_product_list=self.raw_data["len_products_list"])
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
        self.products: List[float] = self.master.raw_data["len_products"].copy()
        self.num_used_stock: List[float] = self.master.metadata["num_used_stock"].copy()
        self.patterns: List[List[List[float]]] = self.master.metadata["patterns"].copy()

        self.color_stock: List[str] = self.master.raw_data["stock_color_label"].copy()
        self.color_product: List[str] = self.master.raw_data["product_color_label"].copy()

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
        self.fig = self.create_cutting_pattern()
        canvas_plot = FigureCanvasTkAgg(self.fig, master=self.inner_canvas)
        canvas_plot.draw()
        widget = canvas_plot.get_tk_widget()
        widget.pack(fill=BOTH, anchor=N)
        plt.close(self.fig)

    def create_cutting_pattern(self) -> Figure:
        total_pattern: int = sum(self.num_used_stock)
        max_len_stock:int = max(self.stocks)
        col_size: int = max(5, total_pattern * 2)
        fig, ax = plt.subplots(figsize=(7, col_size))

        digit = self.get_num_digits(num=max(self.stocks))

        y_offset: float = 0.
        width: float = 10 ** (digit - 1)
        margin: float = width / 2
        for idx_stock, patterns_by_stock in enumerate(self.patterns):
            
            len_stock: float = self.stocks[idx_stock]

            stock_face_color: str = self.color_stock[idx_stock]
            stock_edge_color: str = darken_hex_color(hex_color=stock_face_color, reduction=0.4)

            for pattern in patterns_by_stock:

                if len(pattern) == 0:
                    break

                ax.add_patch(
                    Rectangle(
                        (max_len_stock + width/10, y_offset + width / 4),
                        width/10, width / 2, 
                        edgecolor=stock_edge_color,
                        facecolor=stock_face_color,
                        lw=1
                    )
                )
                ax.text(
                    max_len_stock + width / 4,  # Posisi teks label
                    y_offset + width / 2,  # Vertikalnya tepat di tengah stok
                    f"Stock-{idx_stock + 1} ({len_stock})",
                    ha="left", va="center", fontsize=8
                )

                ax.add_patch(Rectangle((0, y_offset), len_stock, width,
                                    edgecolor=stock_edge_color, facecolor=stock_face_color, lw=1))
                
                x_offset: float = 0.
                for len_product in pattern:
                    
                    idx_product: int = self.products.index(len_product)
                    product_face_color: str = self.color_product[idx_product]
                    product_edge_color: str = darken_hex_color(hex_color=product_face_color, reduction=0.4)
                    
                    len_label: str = str(len_product)
                    ax.add_patch(Rectangle((x_offset, y_offset), len_product, width,
                                       edgecolor=product_edge_color, facecolor=product_face_color, lw=1))
                    ax.text((x_offset + (len_product / 2)), (y_offset + (width / 2)), len_label,
                            ha=CENTER, va=CENTER, fontsize=10)
                    
                    x_offset += len_product
                
                y_offset += (width + margin)
        
        x_bound: float = margin * .1
        y_bound: float = margin
        ax.set_xlim(-x_bound, max_len_stock + width/2)
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

        Label(master=self.stat_frame, text="Used Stock Ratio:").pack(padx=10, pady=4)
        Label(master=self.stat_frame, text=f"{yield_rate:.2f}%").pack(padx=10)

        Label(master=self.stat_frame, text="Unused Stock Ratio:").pack(padx=10, pady=4)
        Label(master=self.stat_frame, text=f"{100-yield_rate:.2f}%").pack(padx=10)

        self.button_save_plot = ButtonThemed(parent=self.stat_frame, text="Save Plot",
                                             bg=Colors.green1, fg=Colors.white,
                                             command=self.save_pattern_fig) 
        self.button_save_plot.pack(padx=4, pady=8)

    def save_pattern_fig(self) -> None:
        path = asksaveasfilename(title="Save Pattern Plot", initialdir="assets",
                                 initialfile="pattern.png", defaultextension= ".png",
                                 filetypes=[("Image files", "*.png")])
        if path:
            self.fig.savefig(path, dpi=300, bbox_inches='tight')
            showinfo(title="Save status", message=f"Saved at {path}")
        else:
            showinfo(title="Save status", message=f"Failed to save")
            

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