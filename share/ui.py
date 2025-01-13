import tkinter as tk
from tkinter import filedialog

from tkinter.filedialog import SaveFileDialog,askdirectory
root = tk.Tk()
root.title("Sharing window")
import os,shutil
filename = 'http_server.py'



def import_folder():
    try:
        change_page = app(root)
        change_page.page2()
        options = {
            "initialdir": "C:/Users/Username/Documents",
            "title": "Select a Folder"
        }

        global file_path
        file_path = askdirectory(**options)
        print(file_path)
        
        with open(filename) as file:
            script = file.read()
            exec(script)

        

        # try:
        #     import subprocess
        #     subprocess.run(['python3', 'http_server.py'])
        #     # get_path(file_path)
            
        # except Exception as e:
        #     print(e)
        
    except Exception as e:
        print(e)

def import_file():
    try:
        change_page = app(root)
        change_page.page2()
        global file_path
        file_path = filedialog.askopenfilename(title="Select a file to share", filetypes=[("All files", "*.*")])
        print(file_path)

        # filename = 'http_server.py'
        # with open(filename) as file:
        #     exec(file.read())

          

        try:
            import subprocess
            subprocess.run(['python3', 'http_server.py'])
            # get_path(file_path)
            
        except Exception as e:
            print(e)
        
    except Exception as e:
        print(e)





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


        # file_name = os.path.basename(file_path)  # Get the file name from the path
        # destination_path = os.path.join(os.getcwd(), file_name)

        # try:
        #     with open(file_path, 'rb') as src_file:
        #         with open(destination_path, 'wb') as dest_file:
        #             shutil.copyfileobj(src_file, dest_file)  # Copy the content from source to destination
        #     print(f"File saved successfully at {destination_path}")
        #     change_page = app(root)
        #     change_page.page2()
        # except Exception as e:
        #     print(f"Error: {e}")
        
            
        
    # except Exception as e:
    #     print(e)
    # if file_path:
    #     # Process the selected file (you can replace this with your own logic)
    #     print("file exists")