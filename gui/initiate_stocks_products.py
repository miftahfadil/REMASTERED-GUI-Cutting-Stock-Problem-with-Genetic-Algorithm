from tkinter import *
from typing import Dict
from typing import List
from typing import Tuple

from utils.theme import Colors
from utils.theme import Fonts
from utils.validate import validate_entry_len
from utils.validate import validate_entry_amt
from .widgets import ButtonThemed
from .widgets import DeleteAddColumn
from .widgets import EntryThemed
from .pattern_result import PatternResult


class InitiateStockProduct(Frame):

    def __init__(self, parent: Tk) -> None:
        super(InitiateStockProduct, self).__init__(master=parent, bg=Colors.white)

        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)

        self.create_gui()

    def create_gui(self) -> None:
        Label(master=self, text="Input Stock and Product Data", font=Fonts.h1,
              bg=Colors.white, fg=Colors.green2).grid(row=0, column=0, columnspan=2, pady=(4, 28))

        self.input_stocks = InputFrame(parent=self, material="Stock")
        self.input_stocks.grid(row=1, column=0, padx=10, sticky=NSEW)

        self.input_products = InputFrame(parent=self, material="Product")
        self.input_products.grid(row=1, column=1, padx=10, sticky=NSEW)

        self.button_generate = ButtonThemed(parent=self, text="Generate Cutting Pattern", bg=Colors.yellow1,
                                fg=Colors.white, command=self.get_stocks_products_input, width=30)
        self.button_generate.grid(row=2, column=0, columnspan=2, pady=24)
    
    def get_stocks_products_input(self) -> None:
        self.master.stocks = self.get_stocks_input(self.input_stocks.input_material_frames)
        self.master.products = self.get_products_input(self.input_products.input_material_frames)
        self.master.switch_frame(name_frame="Pattern Result", new_frame=PatternResult)

    def get_stocks_input(self, input_material_frames: Dict[int, Frame]) -> List[float]|None:
        material_list: List[float] = []

        for material in input_material_frames.values():
            len_material = material.entry_len.get()

            if len_material == '':
                return None
            
            len_material = float(len_material)

            if (len_material > 0 and len_material <= 10000):
                material_list.append(len_material)
            else:
                return None

        return material_list
    
    def get_products_input(self, input_material_frames: Dict[int, Frame]) -> Tuple[List[float]|List[int]]|None:
        material_list: List[float] = []
        material_lengths: List[float] = []
        material_amounts: List[int] = []

        for material in input_material_frames.values():
            len_material = material.entry_len.get()
            amt_material = material.entry_amt.get()

            if len_material == '' or amt_material == '':
                return None
            
            len_material = float(len_material)
            amt_material = int(amt_material)

            if (len_material > 0 and len_material <= 10000) and (amt_material > 0 and amt_material <= 200):
                cur_material = [len_material] * amt_material
                material_list += cur_material

                material_lengths.append(len_material)
                material_amounts.append(amt_material)

            else:
                return None

        return material_lengths, material_amounts, material_list
        
class InputFrame(Frame):
    
    def __init__(self, parent: Tk, material: str, bg: str = Colors.white, **kwargs) -> None:
        super(InputFrame, self).__init__(master=parent, bg=bg, **kwargs)
        
        self.input_material_frames: Dict[int, Frame] = {}
        self.material = material

        self.create_gui()
        
    def create_gui(self) -> None:
        self.create_scrollable()

        self.input_material_frames[1] = MaterialColumn(parent=self.frame, material=self.material, id=1)
        self.input_material_frames[1].pack()

        self.button_del_add = DeleteAddColumn(parent=self, column_frame=MaterialColumn)
        self.button_del_add.grid(row=1, column=0)
    
    def create_scrollable(self) -> None:
        self.scroll = Scrollbar(self, orient=VERTICAL)
        self.scroll.grid(row=0, column=1, sticky='NSW')
        self.canvas = Canvas(self, bg=Colors.white, height=400, yscrollcommand=self.scroll.set, highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=12, padx=12, sticky=NSEW)
        self.scroll.config(command=self.canvas.yview)
        self.frame = Frame(self.canvas, bg=self["bg"])

        self.frame.bind('<Configure>', self._configure_frame)
        self.canvas.bind('<Configure>', self._configure_canvas)

        self.inside_frame = self.canvas.create_window(0, 0, window=self.frame, anchor=NW)

    def _configure_frame(self, e) -> None:
        widget_req_width = self.frame.winfo_reqwidth()
        widget_req_height = self.frame.winfo_reqheight()

        self.canvas.config(scrollregion=(0, 0, widget_req_width, widget_req_height))

        if widget_req_width != self.canvas.winfo_width():
            self.canvas.config(width=widget_req_width)
    
    def _configure_canvas(self, e) -> None:
        widget_req_width = self.frame.winfo_reqwidth()

        if widget_req_width != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.inside_frame, width=self.canvas.winfo_width())

class MaterialColumn(Frame):

    def __init__(self, parent: Tk, material: str, id: str, bg:str = Colors.white) -> None:
        super(MaterialColumn, self).__init__(master=parent, bg=bg)
        self.material = material
        label = Label(master=self, text=f"{self.material}-{id}",
                      font=Fonts.h5, bg=Colors.white, fg=Colors.black)
        label.grid(row=0, column=0, columnspan=5, pady=(4, 0))

        self.create_column()

    def create_column(self) -> None:
        self.len_column()
        if self.material == "Product":
            self.amt_column()
    
    def len_column(self) -> None:
        label_len = Label(master=self, text="Length",
                          font=Fonts.p3, bg=Colors.white, fg=Colors.black)
        label_len.grid(row=1, column=0, padx=4, pady=4)

        self.entry_len = EntryThemed(parent=self, placeholder="Enter length here",
                                     command=validate_entry_len, font=Fonts.p3)
        self.entry_len.grid(row=1, column=1, padx=4, pady=4)
        
    def amt_column(self) -> None:    
        label_amt = Label(master=self, text="Amount",
                          font=Fonts.p3, bg=Colors.white, fg=Colors.black)
        label_amt.grid(row=1, column=2, padx=4, pady=4)

        self.entry_amt = EntryThemed(parent=self, placeholder="Enter amount here",
                                     command=validate_entry_amt, font=Fonts.p3)
        self.entry_amt.grid(row=1, column=3, padx=4, pady=4)

        label_pcs = Label(master=self, text="pcs",
                          font=Fonts.p3, bg=Colors.white, fg=Colors.black)
        label_pcs.grid(row=1, column=4, padx=4, pady=4)


if __name__ == "__main__":
    main = Tk()
    main.title("Input Frame")
    inp_frm = InitiateStockProduct(parent=main)
    inp_frm.pack()
    main.mainloop()