#%% ===============================================================================================
# 
# Programa que recopila varias herramientas para hacer la actualización de las series
# 
# VERSION : 0.1a
# STATE   : Working 1/2
# 
# =================================================================================================

import tkinter as tk
# this is a test
# other test
from tkinter.ttk import Notebook
from Tasks.rename_headers import RenameTab
from Tasks.update_seires import UpdateTab

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Actualización de Series')
        self.resizable(False,False)
        
        self.notebook = Notebook(self)
        self.notebook.pack(expand=True,fill='both')

        self.tabs()

    def tabs(self):
        self.rename = RenameTab(self)
        self.update = UpdateTab(self)

        self.notebook.bind("<<NotebookTabChanged>>", self.resize)

    def resize(self,event):
        selected = self.notebook.index(self.notebook.select())
        if selected == 0:
            width, heigth = [780,250]
        elif selected == 1:
            width, heigth = [780,280]
        self.geometry(f"{width}x{heigth}+{self.winfo_screenwidth()//2-width//2}+{self.winfo_screenheight()//2-heigth//2}")

if __name__ == '__main__':
    window = Window()
    window.mainloop()
# %%
