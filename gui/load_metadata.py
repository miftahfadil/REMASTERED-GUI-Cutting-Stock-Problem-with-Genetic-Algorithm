from tkinter import *
from tkinter.filedialog import askopenfilename

from utils.theme import Colors
from utils.theme import Fonts
from utils.load_json import load_json_data
from .pattern_result import PatternResult
from .widgets import ButtonThemed


class LoadMetadata(Frame):

    def __init__(self, parent: Tk, **kwargs) -> None:
        super().__init__(master=parent, bg=Colors.white, **kwargs)

        self.create_gui()
    
    def create_gui(self) -> None:
        self.create_frame_title()
        self.create_left_content()
        self.create_right_content()

    def create_frame_title(self) -> None:
        self.frame_title = Frame(self, bg=self["bg"])
        self.frame_title.pack(anchor=N, fill=X)

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

        Label(master=self.frame_title, text="Load Cutting Pattern from Metadata", font=Fonts.h1,
            bg=self["bg"], fg=Colors.green2).pack(anchor=N, pady=(12, 4))
        
        Label(master=self.frame_title, text=f"Load previously saved metadata to quickly visualize cutting patterns. "
                                            "This feature helps you review or continue working with existing data.\n"
                                            "Simply select a file, and the plot will be generated automatically for you.",
              font=Fonts.h5, bg=self["bg"], fg=Colors.light_grey2).pack(anchor=N, pady=(4, 12))
        
    def create_left_content(self) -> None:
        self.frame_left_content = Frame(self, bg=self["bg"])
        self.frame_left_content.pack(side=LEFT, fill=X, expand=TRUE)

        self.button_left_frame = Frame(self.frame_left_content, bg=Colors.black)
        self.button_left_frame.pack(anchor=E, fill=X, expand=TRUE)
        self.button_left_frame.grid_columnconfigure((0), weight=1)

        self.load_data_icon = PhotoImage(file="assets/load data icon.png").subsample(2, 2)
        self.button_load_data = ButtonThemed(self.button_left_frame, text="", bg=Colors.green1, fg=Colors.white,
                                              image=self.load_data_icon, width=64, height=64,
                                              command=self.get_load_data)
        self.button_load_data.grid(row=0, column=1, sticky=E)
       
        self.button_left_frame.text = Label(self.button_left_frame, text="", font=Fonts.h4, width=20, anchor=W,
                                        justify=RIGHT, bg=Colors.black, fg=Colors.white)
        self.button_left_frame.text.grid(row=0, column=0, padx=12, sticky=E)

        self.button_load_data.bind("<Enter>", lambda e: self.hover_button_menu(e, "Load Metadata"), add="+")
        self.button_load_data.bind("<Leave>", lambda e: self.hover_button_menu(e, ""), add="+")

    def create_right_content(self) -> None:
        self.frame_right_content = Frame(self, bg=self["bg"])
        self.frame_right_content.pack(side=LEFT, expand=TRUE)

        Label(self.frame_right_content, text="Metadata Path", bg=self.frame_right_content["bg"], fg=Colors.black,
              font=Fonts.h4).pack(padx=12, pady=(64, 12), anchor=W)
        
        self.label_path = Label(self.frame_right_content, text="Select Path First", bg=self.frame_right_content["bg"], fg=Colors.light_grey3,
                                font=Fonts.p3, justify=LEFT, anchor=NW, wraplength=300, width=48, height=16)
        self.label_path.pack(padx=12, anchor=NW)

        self.generate_icon = PhotoImage(file="assets/generate icon.png").subsample(3, 3)

        self.button_generate = ButtonThemed(parent=self.frame_right_content, text="Generate Cutting Pattern", bg=Colors.black,
                                fg=Colors.white, image=self.generate_icon, state = DISABLED, font=Fonts.h5, hover_reduction=-1.2,
                                command=lambda: self.master.switch_frame(name_frame="Pattern Result", new_frame=PatternResult), width=180)
        self.button_generate.pack(padx=12, pady=24, anchor=W)

    def get_load_data(self) -> None:
        path = askopenfilename(title="Load from Metadata", filetypes=[("JSON File", "*.json")],
                            initialdir="results")
        self.metadata = load_json_data(path=path)

        if self.metadata:
            self.master.metadata = self.metadata
            self.label_path.configure(text=path)

            self.button_generate.configure(state=NORMAL)

    def hover_button_menu(self, event, text) -> None:
        event.widget.master.text.configure(text=text)

    def leave_button_menu(self, event, text) -> None:
        event.widget.master.text.configure(text=text)
    