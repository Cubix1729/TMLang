from TMLang_interpreter import interpret_from_code
from customtkinter import (
    CTk,
    BOTH,

)

from tkinter import Menu
from chlorophyll import CodeView
from TMLang_lexer import TMLangLexer


CODE_COLOR_SCHEME = "dracula"


class TMLangGUI(CTk):
    def __init__(self):
        super().__init__()
        self.title("TMLang GUI")
        self.geometry("1000x800")

        self.code_entry = CodeView(self, lexer=TMLangLexer, color_scheme=CODE_COLOR_SCHEME, default_context_menu=True)
        self.code_entry.pack(expand=True, fill=BOTH)

        self.main_menu = Menu(self)
        self.config(menu=self.main_menu)
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl-N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl-O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl-S")
        self.file_menu.add_command(label="Save As", command=self.save_as, accelerator="Ctrl-Shift-S")
        self.main_menu.add_cascade(label="File", menu=self.file_menu)

      
    

    def new_file(self):
        print("New")

    def save_file(self):
        pass

    def open_file(self):
        pass

    def save_as(self):
        print("Worked!")
        
        




if __name__ == "__main__":
    app = TMLangGUI()
    app.mainloop()