from TMLang_interpreter import interpret_from_code
from customtkinter import (
    CTk,
    BOTH,
    END,
)

from tkinter import Menu, PhotoImage
from chlorophyll import CodeView
from TMLang_lexer import TMLangLexer
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askokcancel
import os


CODE_COLOR_SCHEME = "dracula"


class TMLangGUI(CTk):
    def __init__(self):
        super().__init__()
        self.title("TMLang GUI")
        self.geometry("1000x800")
        #self.iconphoto(False, PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)) + "\\TMLang_gui_icon.jpg")))

        # Setting objet's variables
        self.is_saved = True
        self.file_name = None

        # Code editor widget
        self.code_entry = CodeView(self, lexer=TMLangLexer, color_scheme=CODE_COLOR_SCHEME, default_context_menu=True)
        self.code_entry.pack(expand=True, fill=BOTH)
        self.code_entry.bind("<<Modified>>", lambda event: self.code_modified())
        self.code_entry.focus_set()

        # Making the main menu
        self.main_menu = Menu(self)
        self.config(menu=self.main_menu)
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl-N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl-O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl-S")
        self.file_menu.add_command(label="Save As", command=self.save_as, accelerator="Ctrl-Shift-S")
        self.file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl-Q")
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
    
    def get_current_code(self) -> str:
        return self.code_entry.get("1.0", END)

    def new_file(self):
        self.save_before_closing()
        self.code_entry.delete("1.0", END)
        self.is_saved = True
        self.file_name = None

    def save_file(self):
        if self.file_name is None:
            self.save_as()
        else:
            with open(self.file_name, "w") as file:
                file.write(self.get_current_code())
            self.is_saved = True

    def open_file(self):
        file_to_open = askopenfilename()
        if not file_to_open:
            return
        self.save_before_closing()
        with open(file_to_open, "r") as file:
            code_to_open = file.read()
        self.code_entry.delete("1.0", END)
        self.code_entry.insert(END, code_to_open)

    def save_as(self):
        file_to_save_to = asksaveasfilename()
        if not file_to_save_to:
            return
        with open(file_to_save_to, "w") as file:
            file.write(self.get_current_code())
        self.file_name = file_to_save_to
    
    def code_modified(self):
        self.is_saved = False
    
    def save_before_closing(self):
        if not self.is_saved:
            awnser = askokcancel(message=f"The current file ({self.file_name if self.file_name else "unsaved"}).\nDo you want to save it?")
            if awnser:
                self.save_file()
    
    def quit(self):
        self.save_before_closing()
        self.destroy()
        



if __name__ == "__main__":
    app = TMLangGUI()
    app.mainloop()