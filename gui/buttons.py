from tkinter import *

class DeleteAddColumn(Frame):
        
    def __init__(self, parent: Tk, column_frame: Frame):
        super(DeleteAddColumn, self).__init__(master=parent)
        self.parent = parent
        self.column_frame = column_frame

        self.create_button()

    def create_button(self) -> None:
        self.button_del = Button(master=self, text="Delete Previous", command=self.delete_frame)
        self.button_del.grid(row=0, column=0)

        self.button_add = Button(master=self, text="Add Next", command=self.add_frame)
        self.button_add.grid(row=0, column=1)
    
    def delete_frame(self) -> None:
        id = len(self.parent.input_material_frames)

        if id >= 1:
            self.parent.input_material_frames[id].destroy()
            del self.parent.input_material_frames[id]
    
    def add_frame(self) -> None:
        id = len(self.parent.input_material_frames)
        id += 1

        if id <= 100:
            self.parent.input_material_frames[id] = self.column_frame(parent=self.parent.frame,
                                                                      material=self.parent.material, id=id)
            self.parent.input_material_frames[id].pack(pady=8)