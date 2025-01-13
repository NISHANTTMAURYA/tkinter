import tkinter as tk
from tkinter import filedialog

from tkinter.filedialog import SaveFileDialog 
root = tk.Tk()
root.title("Sharing window")
import os


def import_file():
    try:
        # files = [('All Files', '*.*'),  
        #         ('Python Files', '*.py'), 
        #         ('Text Document', '*.txt')] 
        # file = SaveFileDialog(filetypes = files, defaultextension = files) 
        file_path = filedialog.askopenfilename(title="Select a file to open", filetypes=[("All files", "*.*")])
        with open(file_path,'r',encoding="utf8") as file:
            content = file.read()
        with open("/files", 'w',encoding="utf8") as new_file:
            new_file.write(content)
        
    except Exception as e:
        print(e)
    if file_path:
        # Process the selected file (you can replace this with your own logic)
        print("file exists")

class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x900")
        self.login()
    
    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame1 = tk.Frame(self.master, width=500, height=900)
        self.frame1.pack()
        self.reg_txt = tk.Label(self.frame1, text='login').pack()
        self.reg_txt
        self.register_btn = tk.Button(self.frame1, text="Go to Register", command=self.register)
        self.register_btn.pack()
        import_button = tk.Button(root, text="Import File", command=import_file)
        import_button.pack(pady=100)
    
    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = tk.Frame(self.master, width=500, height=900)
        self.frame2.pack()
        self.reg_txt2 = tk.Label(self.frame2, text='register')
        self.reg_txt2.pack()
        self.login_btn = tk.Button(self.frame2, text="Go to Login", command=self.login)
        self.login_btn.pack()


app(root)

root.mainloop()