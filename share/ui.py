import tkinter as tk
from tkinter import filedialog

from tkinter.filedialog import SaveFileDialog,askdirectory
root = tk.Tk()
root.title("Sharing window")
import os,shutil
filename = 'http_server.py'



def import_folder():
    try:
        options = {
            "initialdir": "C:/Users/Username/Documents",
            "title": "Select a Folder"
        }

        global file_path
        file_path = askdirectory(**options)
        if not file_path:  # If user cancels selection
            return
            
        print(f"Selected path: {file_path}")
        
        try:
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(script_dir, 'http_server.py')
            # Pass the file_path and type as command line arguments
            subprocess.Popen(['python3', server_path, file_path, 'folder'])
            
            # Only change page after successful server start
            change_page = app(root)
            change_page.page2()
            
        except Exception as e:
            print(f"Error starting server: {e}")
        
    except Exception as e:
        print(f"Error in import_folder: {e}")

def import_file():
    try:
        global file_path
        file_path = filedialog.askopenfilename(title="Select a file to share", filetypes=[("All files", "*.*")])
        if not file_path:  # If user cancels selection
            return
            
        print(f"Selected file: {file_path}")
        
        try:
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(script_dir, 'http_server.py')
            # Pass the file_path and type as command line arguments
            subprocess.Popen(['python3', server_path, file_path, 'file'])
            
            # Only change page after successful server start
            change_page = app(root)
            change_page.page2()
            
        except Exception as e:
            print(f"Error starting server: {e}")
        
    except Exception as e:
        print(f"Error in import_file: {e}")





class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x900")
        self.page1()
    
    def page1(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame1 = tk.Frame(self.master, width=500, height=900)
        self.frame1.pack()
        self.reg_txt = tk.Label(self.frame1, text='First Page').pack()
        self.reg_txt

        button1= tk.Button(root, text= "Share a file", command=import_file)
        button1.pack(side= tk.LEFT)
        button2= tk.Button(root, text= "share a folder", command= import_folder)
        button2.pack(side=tk.RIGHT)

        # self.register_btn = tk.Button(self.frame1, text="Go to Register", command=self.register)
        # self.register_btn.pack()

        # import_button = tk.Button(root, text="Choose location of file to share", command=import_folder)
        # import_button.pack(pady=100)
    
    def page2(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = tk.Frame(self.master, width=500, height=900)
        self.frame2.pack()
        self.reg_txt2 = tk.Label(self.frame2, text='register')
        self.reg_txt2.pack()
        self.login_btn = tk.Button(self.frame2, text="Back", command=self.page1)
        self.login_btn.pack()


app(root)

root.mainloop()

