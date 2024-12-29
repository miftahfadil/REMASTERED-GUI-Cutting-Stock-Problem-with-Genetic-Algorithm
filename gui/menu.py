from tkinter import *

from utils.theme import Colors
from utils.theme import Fonts
from .widgets import ButtonThemed
from .initiate_stocks_products import InitiateStockProduct
from .load_metadata import LoadMetadata


class MainMenu(Frame):

    def __init__(self, parent: Tk) -> None:
        super(MainMenu, self).__init__(master=parent, bg=Colors.white)

        self.master.stocks = None
        self.master.products = None
        self.master.metadata = None

        self.create_title()
        self.create_content()
    
    def create_title(self):
        self.title_frame = Frame(self, bg=self["bg"])
        self.title_frame.pack(padx=100, side=LEFT, fill=X, expand=TRUE)
        self.title_frame.grid_columnconfigure(3, weight=1)

        Label(self.title_frame, text="Wasteless", bg=self["bg"], fg=Colors.black,
              font=Fonts.h1).grid(row=0, column=0, sticky=NS)
        
        Label(self.title_frame, text="", bg=Colors.green1,
              font=Fonts.h1).grid(row=0, column=1, padx=2, sticky=NS)
        
        Label(self.title_frame, text="Cut", bg=self["bg"], fg=Colors.black,
              font=Fonts.h1).grid(row=0, column=2, sticky=NS)
        
        Label(self.title_frame, text="Optimizing every cut, minimizing every waste.", bg=self["bg"], fg=Colors.light_grey2,
              font=Fonts.h4, justify=LEFT, anchor=W).grid(row=1, column=0, columnspan=4, pady=4, sticky=W)

    def create_content(self):
        self.content_frame = Frame(self, bg=self["bg"])
        self.content_frame.pack(side=LEFT, fill=X, expand=TRUE)

        self.button1_frame = Frame(self.content_frame, bg=Colors.black)
        self.button1_frame.pack(pady=4, fill=X, expand=TRUE)

        
        self.button2_frame = Frame(self.content_frame, bg=Colors.black)
        self.button2_frame.pack(pady=4, fill=X, expand=TRUE)

        self.create_new_icon = PhotoImage(file="assets/create new icon.png").subsample(2, 2)
        self.button_create_new = ButtonThemed(self.button1_frame, text="", bg=Colors.green1, fg=Colors.white,
                                              image=self.create_new_icon, width=64, height=64,
                                              command=lambda: self.master.switch_frame(name_frame="Input Data Frame", new_frame=InitiateStockProduct))
        self.button_create_new.grid(row=0, column=0, sticky=W)
       
        self.button1_frame.text = Label(self.button1_frame, text="", font=Fonts.h4, width=20, anchor=W,
                                        justify=LEFT, bg=Colors.black, fg=Colors.white)
        self.button1_frame.text.grid(row=0, column=1, padx=12, sticky=W)

        self.load_metadata_icon = PhotoImage(file="assets/load metadata icon.png").subsample(2, 2)
        self.button_load_metadata = ButtonThemed(self.button2_frame, text="", bg=Colors.green1, fg=Colors.white,
                                              image=self.load_metadata_icon, width=64, height=64,
                                              command=lambda: self.master.switch_frame(name_frame="Load Data Frame", new_frame=LoadMetadata))
        self.button_load_metadata.grid(row=0, column=0, sticky=W)

        self.button2_frame.text = Label(self.button2_frame, text="", font=Fonts.h4, width=20, anchor=W,
                                        justify=LEFT, bg=Colors.black, fg=Colors.white)
        self.button2_frame.text.grid(row=0, column=1, padx=12, sticky=W)


        self.button_create_new.bind("<Enter>", lambda e: self.hover_button_menu(e, "Create New"), add="+")
        self.button_create_new.bind("<Leave>", lambda e: self.hover_button_menu(e, ""), add="+")

        self.button_load_metadata.bind("<Enter>", lambda e: self.hover_button_menu(e, "Load Metadata"), add="+")
        self.button_load_metadata.bind("<Leave>", lambda e: self.hover_button_menu(e, ""), add="+")


    def hover_button_menu(self, event, text) -> None:
        event.widget.master.text.configure(text=text)

    def leave_button_menu(self, event, text) -> None:
        event.widget.master.text.configure(text=text)

    
