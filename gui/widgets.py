from tkinter import *
from collections.abc import Callable
from typing import Optional
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb


from utils.theme import Colors
from utils.theme import Fonts


class ButtonThemed(Button):

    def __init__(self, parent: Widget, text:str, bg: str, fg: str, command: Callable, **kw):
        super(ButtonThemed, self).__init__(master=parent, text=text, bg=bg, fg=fg,
                                        command=command, font=Fonts.h4, relief=FLAT, **kw)
        
        self.defaultBG = self['bg']
        self.hoverBG = darken_hex_color(self['bg'])

        self.bind('<Enter>', self.on_button_hover)
        self.bind('<Leave>', self.on_button_leave)

    def on_button_hover(self, event):
        event.widget['bg'] = self.hoverBG
                               
    def on_button_leave(self, event):
        event.widget['bg'] = event.widget.defaultBG

class DeleteAddColumn(Frame):
        
    def __init__(self, parent: Tk, column_frame: Frame, bg: str = Colors.white, **kwargs) -> None:
        super(DeleteAddColumn, self).__init__(master=parent, bg=bg, **kwargs)
        self.parent = parent
        self.column_frame = column_frame

        self.create_button()

    def create_button(self) -> None:
        self.button_del = ButtonThemed(parent=self, text="Delete Previous", bg=Colors.red,
                                       fg=Colors.white, command=self.delete_frame, width=15)
        self.button_del.grid(row=0, column=0, padx=4, pady=4)

        self.button_add = ButtonThemed(parent=self, text="Add Next", bg=Colors.green1,
                                       fg=Colors.white, command=self.add_frame, width=15)
        self.button_add.grid(row=0, column=1, padx=4, pady=4)
    
    def delete_frame(self) -> None:
        id = len(self.parent.input_material_frames)

        if id >= 1:
            self.parent.input_material_frames[id].destroy()
            del self.parent.input_material_frames[id]
    
    def add_frame(self) -> None:
        id = len(self.parent.input_material_frames)
        id += 1

        if id <= 20:
            self.parent.input_material_frames[id] = self.column_frame(parent=self.parent.frame,
                                                                      material=self.parent.material, id=id)
            self.parent.input_material_frames[id].pack(pady=8)
        

from typing import Callable, Optional


class EntryThemed(Entry):

    def __init__(self, parent: Widget, placeholder: str = "", highlight_color: str = Colors.yellow1, 
                 border_color: str = "#CCCCCC", command: Optional[Callable] = None, **kw):
        super(EntryThemed, self).__init__(parent, **kw)

        self.placeholder = placeholder
        self.default_fg_color = self['fg']
        self.default_bg_color = self['bg']
        self.highlight_color = highlight_color
        self.border_color = border_color
        self.command = command

        self.placeholder_active = True
        self['fg'] = 'grey'
        self.insert(0, self.placeholder)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        # Initial border style
        self.configure(highlightthickness=2, highlightbackground=self.border_color)

    def on_focus_in(self, event):
        if self.placeholder_active:
            self.delete(0, END)
            self['fg'] = self.default_fg_color
            self.placeholder_active = False
        self.configure(highlightbackground=self.highlight_color)

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = 'grey'
            self.placeholder_active = True
        self.configure(highlightbackground=self.border_color)

    def on_key_release(self, event):
        if self.command:
            if self.command(self.get()):
                self.config(highlightcolor=self.border_color)
            else:
                self.config(highlightcolor=Colors.red)

    def on_hover(self, event):
        self.configure(highlightbackground=self.highlight_color)

    def on_leave(self, event):
        self.configure(highlightbackground=self.border_color)

def darken_hex_color(hex_color: str, reduction: float = 0.2) -> str:
    """
    Mengurangi kecerahan (lightness) dari warna heksadesimal.
    
    Args:
        hex_color (str): Warna dalam format heksadesimal (misalnya "#RRGGBB").
        reduction (float): Proporsi penurunan kecerahan (default: 0.2, yaitu 20%).
    
    Returns:
        str: Warna hasil yang lebih gelap dalam format heksadesimal.
    """
    # Validasi input
    if not (hex_color.startswith("#") and len(hex_color) == 7):
        raise ValueError("Format warna harus berupa '#RRGGBB'.")
    
    # Konversi warna dari heksadesimal ke nilai RGB
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    # Konversi RGB ke HLS
    h, l, s = rgb_to_hls(r, g, b)

    # Kurangi kecerahan (lightness)
    l = max(0, l * (1 - reduction))

    # Konversi kembali dari HLS ke RGB
    r, g, b = hls_to_rgb(h, l, s)

    # Konversi RGB ke heksadesimal
    darkened_hex = "#{:02X}{:02X}{:02X}".format(
        int(r * 255), int(g * 255), int(b * 255)
    )
    
    return darkened_hex

