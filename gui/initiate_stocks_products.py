from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from typing import Dict
from typing import List
from typing import Tuple
from typing import Literal

from utils.theme import Colors
from utils.theme import Fonts
from utils.validate import validate_entry_len
from utils.validate import validate_entry_amt
from utils.load_json import load_json_data
from .widgets import ButtonThemed
from .widgets import DeleteAddColumn
from .widgets import EntryThemed
from .pattern_result import PatternResult


class InitiateStockProduct(Frame):

    def __init__(self, parent: Tk, **kwargs) -> None:
        super(InitiateStockProduct, self).__init__(master=parent, bg=Colors.white, **kwargs)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.create_gui()

    def create_gui(self) -> None:
        self.create_title()

        self.create_input_column()

        self.generate_icon = PhotoImage(file="assets/generate icon.png").subsample(3, 3)

        self.button_generate = ButtonThemed(parent=self, text="Generate Cutting Pattern", bg=Colors.green1,
                                fg=Colors.white, image=self.generate_icon, command=self.get_stocks_products_input, width=200)
        self.button_generate.grid(row=2, column=0, columnspan=2, pady=24)

    def create_title(self) -> None:
        self.frame_title = Frame(self, bg=self["bg"])
        self.frame_title.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.upper_frame_title = Frame(self.frame_title, bg=self["bg"])
        self.upper_frame_title.pack(padx=12, pady=12, anchor=NW, fill=X, expand=TRUE)

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

        Label(master=self.frame_title, text="Input Stock and Product Data", font=Fonts.h1,
            bg=self["bg"], fg=Colors.green2).pack(padx=48, pady=(4, 6), anchor=CENTER)
        
        Label(master=self.frame_title, text="Enter the stock and product details to generate cutting patterns. "
                                            "This tool is designed to minimize waste by creating optimized cutting layouts.\n"
                                            "You can also load existing metadata for a faster setup.",
            font=Fonts.h5, bg=self["bg"], fg=Colors.light_grey2, justify=CENTER).pack(padx=48, pady=(0, 6), anchor=CENTER)
        
        self.load_data_icon = PhotoImage(file="assets/load data icon.png").subsample(4, 4)

        self.button_load_input = ButtonThemed(parent=self.frame_title, text="Load from Metadata",
                                              font=Fonts.h5, bg=Colors.green1, fg=Colors.white,
                                              image=self.load_data_icon, command=self.load_data_input, width=150)
        self.button_load_input.pack(padx=12, pady=12, anchor=E)
        
    def create_input_column(self) -> None:
        self.input_stocks = InputFrame(parent=self, material="Stock")
        self.input_stocks.grid(row=1, column=0, padx=10, sticky=E)

        self.input_products = InputFrame(parent=self, material="Product")
        self.input_products.grid(row=1, column=1, padx=10, sticky=W)

    def load_data_input(self) -> None:
        path = askopenfilename(title="Load from Metadata", filetypes=[("JSON File", "*.json")],
                            initialdir="results")
        self.metadata = load_json_data(path)

        if self.metadata:
            self.load_stock()
            self.load_products()
            
    def load_stock(self) -> None:
        for id in self.input_stocks.input_material_frames.keys():
            self.input_stocks.input_material_frames[id].destroy()
        
        self.input_stocks.input_material_frames = {}

        for (idx, len_stock) in enumerate(self.metadata["len_stocks_list"]):
            self.input_stocks.button_del_add.add_frame()
            self.input_stocks.input_material_frames[idx+1].entry_len.delete(0, END)
            self.input_stocks.input_material_frames[idx+1].entry_len.insert(0, str(len_stock))
            self.input_stocks.input_material_frames[idx+1].entry_len["fg"] = Colors.black

            self.input_stocks.input_material_frames[idx+1].color["bg"] = self.metadata["stock_color_label"][idx]
    
    def load_products(self) -> None:
        for id in self.input_products.input_material_frames.keys():
            self.input_products.input_material_frames[id].destroy()
        
        self.input_products.input_material_frames = {}

        for (idx, len_product) in enumerate(self.metadata["len_products"]):
            self.input_products.button_del_add.add_frame()
            self.input_products.input_material_frames[idx+1].entry_len.delete(0, END)
            self.input_products.input_material_frames[idx+1].entry_len.insert(0, str(len_product))
            self.input_products.input_material_frames[idx+1].entry_len["fg"] = Colors.black

            self.input_products.input_material_frames[idx+1].entry_amt.delete(0, END)
            self.input_products.input_material_frames[idx+1].entry_amt.insert(0, str(self.metadata["amt_products"][idx]))
            self.input_products.input_material_frames[idx+1].entry_amt["fg"] = Colors.black

            self.input_products.input_material_frames[idx+1].color["bg"] = self.metadata["product_color_label"][idx]

    def get_stocks_products_input(self) -> None:
        try:
            # Validasi dan pengambilan input stok
            self.master.stocks = self.get_stocks_input(self.input_stocks.input_material_frames)
            if not self.master.stocks[0] or not all(isinstance(stock, (int, float)) and stock > 0 for stock in self.master.stocks[0]):
                raise ValueError("Stock length inputs must be a list of positive numbers.")
            
            # Validasi dan pengambilan input produk
            self.master.products = self.get_products_input(self.input_products.input_material_frames)
            if not self.master.products[0] or not all(isinstance(product, (float, int)) and product > 0 for product in self.master.products[0]):
                raise ValueError("Product length inputs must be a list of positive numbers.")
            
            if not self.master.products[1] or not all(isinstance(product, int) and product > 0 for product in self.master.products[1]):
                raise ValueError("Product amount inputs must be a list of positive integers.")
            
            # Validasi tambahan: apakah produk dapat dipotong dari stok
            if any(product > max(self.master.stocks[0]) for product in self.master.products[2]):
                raise ValueError("One or more products exceed the maximum stock length.")

            # Berpindah ke frame hasil
            self.master.switch_frame(name_frame="Pattern Result", new_frame=PatternResult)
        
        except ValueError as ve:
            # Tangkap ValueError untuk validasi input
            showerror("Input Error", str(ve))
        
        except Exception as e:
            # Tangkap error lain yang tidak terduga
            showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")


    # def get_stocks_products_input(self) -> None:
        # self.master.stocks = self.get_stocks_input(self.input_stocks.input_material_frames)
        # self.master.products = self.get_products_input(self.input_products.input_material_frames)
        # self.master.switch_frame(name_frame="Pattern Result", new_frame=PatternResult)
    #     

    def get_stocks_input(self, input_material_frames: Dict[int, Frame]) -> List[float]|List[str]|None:
        material_list: List[float] = []
        color_list: List[str] = []

        for material in input_material_frames.values():
            len_material = material.entry_len.get()

            if len_material == '':
                return None
            
            len_material = float(len_material)

            if (len_material > 0 and len_material <= 10000):
                material_list.append(len_material)
                color_list.append(material.color["bg"])
            else:
                return None

        return material_list, color_list
    
    def get_products_input(self, input_material_frames: Dict[int, Frame]) -> Tuple[List[float]|List[int]|List[str]]|None:
        material_list: List[float] = []
        material_lengths: List[float] = []
        material_amounts: List[int] = []
        color_list: List[str] = []

        for material in input_material_frames.values():
            len_material = material.entry_len.get()
            amt_material = material.entry_amt.get()

            if len_material == '' or amt_material == '':
                return None
            
            len_material = float(len_material)
            amt_material = int(amt_material)

            if (len_material > 0 and len_material <= 10000) and (amt_material > 0 and amt_material <= 1000):
                cur_material = [len_material] * amt_material
                material_list += cur_material

                material_lengths.append(len_material)
                material_amounts.append(amt_material)
                color_list.append(material.color["bg"])

            else:
                return None
    
        return material_lengths, material_amounts, material_list, color_list
    
        
class InputFrame(Frame):
    
    def __init__(self, parent: Widget, material: Literal["Stock", "Product"], bg: str = Colors.white, **kwargs) -> None:
        super(InputFrame, self).__init__(master=parent, bg=bg, **kwargs)
        
        self.input_material_frames: Dict[int, Frame] = {}
        self.material = material

        self.create_gui()
        
    def create_gui(self) -> None:
        self.create_scrollable()

        self.input_material_frames[1] = MaterialColumn(parent=self.frame, material=self.material, id=1)
        self.input_material_frames[1].pack(padx=4, pady=2)

        self.button_del_add = DeleteAddColumn(parent=self, column_frame=MaterialColumn)
        self.button_del_add.grid(row=1, column=0)
    
    def create_scrollable(self) -> None:
        self.scroll = Scrollbar(self, orient=VERTICAL)
        self.scroll.grid(row=0, column=1, sticky='NSW')
        self.canvas = Canvas(self, bg=Colors.white, height=300, yscrollcommand=self.scroll.set, highlightthickness=0)
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

    def __init__(self, parent: Widget, material: str, id: str, bg:str = Colors.white) -> None:
        super(MaterialColumn, self).__init__(master=parent, bg=bg)
        self.material = material
        label = Label(master=self, text=f"{self.material}-{id}",
                      font=Fonts.h5, bg=Colors.white, fg=Colors.black)
        label.grid(row=0, column=0, padx=4, pady=(4, 2), sticky=W)

        self.color = Button(master=self, bg="#CFCFCF", font=Fonts.p3, relief=FLAT,
                           width=2, command=self.change_color_label)
        self.color.grid(row=0, column=1, padx=4, pady=2, sticky=W)

        self.create_column()

    def create_column(self) -> None:
        self.len_column()
        if self.material == "Product":
            self.color["bg"] = "#6d9773"
            self.amt_column()
    
    def len_column(self) -> None:
        Label(master=self, text="Length",
            font=Fonts.p3, bg=Colors.white, fg=Colors.black).grid(row=1, column=0, padx=4, pady=4, sticky=W)

        self.entry_len = EntryThemed(parent=self, placeholder="Enter length here",
                                     command=validate_entry_len, font=Fonts.p3)
        self.entry_len.grid(row=1, column=1, padx=4, pady=4)
        
    def amt_column(self) -> None:    
        Label(master=self, text="Amount",
            font=Fonts.p3, bg=Colors.white, fg=Colors.black).grid(row=1, column=2, padx=4, pady=4)

        self.entry_amt = EntryThemed(parent=self, placeholder="Enter amount here",
                                     command=validate_entry_amt, font=Fonts.p3)
        self.entry_amt.grid(row=1, column=3, padx=4, pady=4)

        Label(master=self, text="pcs",
            font=Fonts.p3, bg=Colors.white, fg=Colors.black).grid(row=1, column=4, padx=4, pady=4)

    def change_color_label(self) -> None:
        choosen_color = colorchooser.askcolor(parent=self, title="Choose Color Label")[1]
        if choosen_color:
            self.color["bg"] = choosen_color


if __name__ == "__main__":
    main = Tk()
    main.title("Input Frame")
    inp_frm = InitiateStockProduct(parent=main)
    inp_frm.pack()
    main.mainloop()