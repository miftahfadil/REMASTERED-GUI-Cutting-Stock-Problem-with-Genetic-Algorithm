from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from typing import Dict
from typing import List
from typing import Any
import json

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

    def __init__(self, parent: Tk, bg:str = Colors.white,  **kwargs) -> None:
        super(PatternResult, self).__init__(master=parent, bg=bg, **kwargs)

        if self.master.stocks and self.master.products:

            self.metadata: Dict[str, List[int]|List[float]|Any] = genetic_algorithm(len_stock_list=self.master.stocks[0],
                                                                len_product_list=self.master.products[2])

            self.metadata["len_products"] = self.master.products[0].copy()
            self.metadata["amt_products"] = self.master.products[1].copy()
            self.metadata["len_products_list"] = self.master.products[2].copy()
            self.metadata["product_color_label"] = self.master.products[3].copy()
            self.metadata["stock_color_label"] = self.master.stocks[1].copy()
        
        elif self.master.metadata:
            self.metadata = self.master.metadata

        self.create_gui()

    def create_gui(self) -> None:
        self.frame_title = Frame(self, bg=self["bg"])
        self.frame_title.pack(anchor=NW, fill=BOTH)

        self.upper_frame_title = Frame(self.frame_title, bg=self["bg"])
        self.upper_frame_title.pack(padx=12, pady=12, anchor=NW, fill=X)

        self.back_icon = PhotoImage(file="assets/back icon.png").subsample(4, 4)

        self.button_back = ButtonThemed(parent=self.upper_frame_title, text="Menu", bg=Colors.green1, fg=Colors.white, width=50,
                                    image=self.back_icon, font=Fonts.h5, command=self.master.create_gui)
        self.button_back.grid(row=0, column=0, padx=(0, 24), sticky=W)

        Label(self.upper_frame_title, text="Wasteless", bg=self["bg"], fg=Colors.black,
              font=Fonts.h5).grid(row=0, column=1, sticky=NS)
        
        Label(self.upper_frame_title, text="", bg=Colors.green1,
              font=Fonts.h5).grid(row=0, column=2, padx=2)
        
        Label(self.upper_frame_title, text="Cut", bg=self["bg"], fg=Colors.black,
              font=Fonts.h5).grid(row=0, column=3, sticky=NS)

        Label(master=self.frame_title, text="Cutting Pattern Result", font=Fonts.h1,
            bg=self["bg"], fg=Colors.green2).pack(anchor=N, pady=(24, 4))
        
        Label(master=self.frame_title, text=f"Here the optimized cutting patterns that reduce the unused stock ratio. "
                                             "You can also save the plot and metadata to keep track or use them later.",
              font=Fonts.h5, bg=self["bg"], fg=Colors.light_grey2).pack(anchor=N, pady=(4, 24))

        pattern_plot = PatternPlot(parent=self)
        pattern_plot.pack(padx=10, pady=10, anchor=N, fill=BOTH)


class PatternPlot(Frame):

    def __init__(self, parent: Widget, **kwargs) -> None:
        super(PatternPlot, self).__init__(master=parent, bg=Colors.black, **kwargs)
        self.stocks: List[float] = self.master.metadata["len_stocks_list"].copy()
        self.products: List[float] = self.master.metadata["len_products"].copy()
        self.num_used_stock: List[float] = self.master.metadata["num_used_stock"].copy()
        self.patterns: List[List[List[float]]] = self.master.metadata["patterns"].copy()

        self.color_stock: List[str] = self.master.metadata["stock_color_label"].copy()
        self.color_product: List[str] = self.master.metadata["product_color_label"].copy()

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        self.create_scrollable()
        self.display_plot()
        self.display_stat()

    def create_scrollable(self) -> None:
        self.canvas = Canvas(master=self, height=500, width=800, bg="white")
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        y_scrollbar = ttk.Scrollbar(master=self, orient=VERTICAL, command=self.canvas.yview)
        y_scrollbar.grid(row=0, column=1, sticky=NS)

        self.canvas.configure(yscrollcommand=y_scrollbar.set)

        self.inner_canvas = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_canvas, anchor=NW)

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
        fig, ax = plt.subplots(figsize=(8, col_size))

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
        self.stat_frame = Frame(master=self, bg=Colors.black)
        self.stat_frame.grid(row=0, column=2, sticky=NSEW, padx=30)

        self.yield_rate : float = self.master.metadata["yield_rate"] * 100

        Label(master=self.stat_frame, text="Cutting Pattern Stat", font=Fonts.h3,
              bg=Colors.black, fg=Colors.white).pack(padx=12, pady=24, anchor=CENTER)

        Label(master=self.stat_frame, text="Used Stock Ratio:", font=Fonts.h4,
              bg=Colors.black, fg=Colors.white).pack(pady=4, anchor=NW)
        Label(master=self.stat_frame, text=f"{self.yield_rate:.2f}%", font=Fonts.h5,
              bg=Colors.black, fg=Colors.white).pack(pady=(4, 12), anchor=NW)

        Label(master=self.stat_frame, text="Unused Stock Ratio:", font=Fonts.h4,
              bg=Colors.black, fg=Colors.white).pack(pady=(12, 4), anchor=NW)
        Label(master=self.stat_frame, text=f"{100-self.yield_rate:.2f}%", font=Fonts.h5,
              bg=Colors.black, fg=Colors.white).pack(pady=(4, 12), anchor=NW)

        self.save_icon = PhotoImage(file="assets/save icon.png").subsample(4, 4)

        self.button_save_plot = ButtonThemed(parent=self.stat_frame, text="Save Plot",
                                             bg=Colors.green2, fg=Colors.white, image=self.save_icon,
                                             command=self.save_pattern_fig) 
        self.button_save_plot.pack(side=BOTTOM, padx=12, pady=(0, 24), anchor=S, fill=X)

        self.button_save_metadata = ButtonThemed(parent=self.stat_frame, text="Save Metadata",
                                             bg=Colors.green2, fg=Colors.white, image=self.save_icon,
                                             command=self.save_metadata) 
        self.button_save_metadata.pack(side=BOTTOM, padx=12, pady=(0, 24), anchor=S, fill=X)

    def save_pattern_fig(self) -> None:
        path = asksaveasfilename(title="Save Cutting Pattern Plot", initialdir="results",
                                 initialfile="pattern.png", defaultextension= ".png",
                                 filetypes=[("Image files", "*.png")])
        if path:
            self.fig.savefig(path, dpi=300, bbox_inches='tight')
            showinfo(title="Save status", message=f"Saved at {path}")
        else:
            showinfo(title="Save status", message=f"Failed to save")

    def save_metadata(self) -> None:
        self.__metadata = {}
        path = asksaveasfilename(title="Save Metadata", initialdir="results",
                                 initialfile="metadata.json", defaultextension= ".json",
                                 filetypes=[("JSON File", "*.json")])
        try:
            if path:
                self.__metadata = {
                    "len_stocks_list" : self.stocks.copy(),
                    "len_products_list" : self.master.metadata["len_products_list"].copy(),
                    "len_products" : self.products.copy(),
                    "amt_products" : self.master.metadata["amt_products"].copy(),
                    "num_used_stock" : self.num_used_stock.copy(),
                    "patterns" : self.patterns.copy(),
                    "stock_color_label" : self.color_stock.copy(),
                    "product_color_label" : self.color_product.copy(),
                    "yield_rate" : self.yield_rate / 100
                }

                with open(path, "w") as json_file:
                    json.dump(obj=self.__metadata, fp=json_file)

                showinfo(title="Save status", message=f"Saved at {path}")
            else:
                showinfo(title="Save status", message=f"Failed to save")

        except AttributeError as ae:
            showerror(title="Save Error", message=f"Attribute Error: {ae}")
        except KeyError as ke:
            showerror(title="Save Error", message=f"Key Error: Missing key in metadata: {ke}")
        except IOError as io:
            showerror(title="Save Error", message=f"File Error: Unable to write file: {io}")
        except Exception as e:
            showerror(title="Save Error", message=f"An unexpected error occurred: {e}")
            

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