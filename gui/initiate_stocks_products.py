from tkinter import *
from typing import Dict

from buttons import DeleteAddColumn

class InitiateStockProduct(Frame):

    def __init__(self, parent: Tk) -> None:
        super(InitiateStockProduct, self).__init__(master= parent)

        self.create_gui()

    def create_gui(self) -> None:
        input_stocks = InputFrame(parent=self, material="Stock")
        input_stocks.grid(row=0, column=0)

        input_product = InputFrame(parent=self, material="Product")
        input_product.grid(row=0, column=1)

class InputFrame(Frame):
    
    def __init__(self, parent: Tk, material: str) -> None:
        super(InputFrame, self).__init__(master=parent, width=400, height=500)
        
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
        self.canvas = Canvas(self, width=500, height=300, 
                            yscrollcommand=self.scroll.set, highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=12, padx=12, sticky=NSEW)
        self.scroll.config(command=self.canvas.yview)
        self.frame = Frame(self.canvas)

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

    def __init__(self, parent: Tk, material: str, id: str) -> None:
        super(MaterialColumn, self).__init__(master=parent)
        label = Label(master=self, text=f"{material}-{id}")
        label.grid(row=0, column=0, columnspan=3)

        self.create_column()

    def create_column(self) -> None:
        self.len_column()
        self.amt_column()
    
    def len_column(self) -> None:
        label_len = Label(master=self, text="Length")
        label_len.grid(row=1, column=0)

        self.entry_len = Entry(master=self)
        self.entry_len.grid(row=1, column=1)

        label_cm = Label(master=self, text="cm")
        label_cm.grid(row=1, column=2)

        label_max_len = Label(master=self, text="Maximum 5000 cm (50 m)")
        label_max_len.grid(row=2, column=0, columnspan=3)
        
    def amt_column(self) -> None:    
        label_amt = Label(master=self, text="Amount")
        label_amt.grid(row=1, column=3)

        self.entry_amt = Entry(master=self)
        self.entry_amt.grid(row=1, column=4)

        label_pcs = Label(master=self, text="pcs")
        label_pcs.grid(row=1, column=5)

        label_max_len = Label(master=self, text="Maximum 2000 pcs")
        label_max_len.grid(row=2, column=3, columnspan=3)


if __name__ == "__main__":
    main = Tk()
    main.title("Input Frame")
    inp_frm = InitiateStockProduct(parent=main)
    inp_frm.pack()
    main.mainloop()