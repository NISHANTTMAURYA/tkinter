import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import time

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
            url_file = os.path.join(script_dir, 'share_url.txt')  # Define url file path
            
            # Pass the file_path and type as command line arguments
            change_page = app(root)
            change_page.url_file = url_file  # Store url file path in app instance
            change_page.server_process = subprocess.Popen(['python3', server_path, file_path, 'folder', url_file])
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
            url_file = os.path.join(script_dir, 'share_url.txt')  # Define url file path
            
            # Pass the file_path and type as command line arguments
            change_page = app(root)
            change_page.url_file = url_file  # Store url file path in app instance
            change_page.server_process = subprocess.Popen(['python3', server_path, file_path, 'file', url_file])
            change_page.page2()
            
        except Exception as e:
            print(f"Error starting server: {e}")
        
    except Exception as e:
        print(f"Error in import_file: {e}")





class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x900")
        self.server_process = None
        self.qr_label = None
        self.url_file = None  # Add this to store the url file path
        self.page1()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        if os.path.exists('share_url.txt'):
            os.remove('share_url.txt')
        self.master.destroy()
    
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
        self.frame2.pack(expand=True, fill='both')
        
        # Add a title
        title_label = tk.Label(self.frame2, text="Share Link", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Wait briefly for the URL file to be created
        attempts = 0
        while attempts < 10 and not os.path.exists(self.url_file):  # Use the stored url_file path
            time.sleep(0.5)
            attempts += 1
        
        try:
            # Read the URL from the file using the correct path
            with open(self.url_file, 'r') as f:
                url = f.read().strip()
            
            # Display URL
            url_label = tk.Label(self.frame2, text=f"Share URL:", font=('Arial', 12))
            url_label.pack(pady=5)
            
            url_text = tk.Label(self.frame2, text=url, font=('Arial', 10), wraplength=400)
            url_text.pack(pady=5)
            
            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Resize QR code to fit window better
            qr_image = qr_image.resize((300, 300))
            
            # Convert to PhotoImage
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Display QR Code with a label
            qr_title = tk.Label(self.frame2, text="Scan QR Code:", font=('Arial', 12))
            qr_title.pack(pady=5)
            
            self.qr_label = tk.Label(self.frame2, image=qr_photo)
            self.qr_label.image = qr_photo  # Keep a reference!
            self.qr_label.pack(pady=10)
            
        except Exception as e:
            error_label = tk.Label(self.frame2, text=f"Error generating QR code: {e}")
            error_label.pack(pady=10)
        
        # Back button
        self.login_btn = tk.Button(self.frame2, text="Back", command=self.page1,
                                 font=('Arial', 12))
        self.login_btn.pack(pady=20)


app(root)

root.mainloop()

