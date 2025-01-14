import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import time
import subprocess
import os
import threading

from tkinter.filedialog import SaveFileDialog,askdirectory
def cleanup_ports_background():
    def cleanup():
        print("Starting background port cleanup...")
        try:
            # Kill any existing ngrok processes
            print("Checking for ngrok processes...")
            try:
                subprocess.run(['pkill', 'ngrok'], stderr=subprocess.DEVNULL)
                print("Killed ngrok processes")
            except Exception as e:
                print(f"Note: No ngrok processes found ({e})")
            
            # Kill any process on port 8000
            print("Checking for processes on port 8000...")
            try:
                cmd = "lsof -ti :8000"
                pid = subprocess.check_output(cmd, shell=True).decode().strip()
                if pid:
                    print(f"Found process {pid} on port 8000, killing it...")
                    subprocess.run(['kill', '-9', pid], stderr=subprocess.DEVNULL)
                    print(f"Killed process {pid}")
                else:
                    print("No process found on port 8000")
            except subprocess.CalledProcessError:
                print("No process found on port 8000")
            except Exception as e:
                print(f"Error checking port 8000: {e}")

            # Wait a moment to ensure ports are cleared
            time.sleep(1)
            print("Port cleanup completed")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")

    # Run cleanup in background thread
    thread = threading.Thread(target=cleanup)
    thread.daemon = True
    thread.start()
    # Wait a moment for cleanup to complete
    time.sleep(2)

# Run cleanup when app starts
print("Initializing application...")
cleanup_ports_background()

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
            url_file = os.path.join(script_dir, 'share_url.txt')
            
            # Clear any existing URL file
            if os.path.exists(url_file):
                os.remove(url_file)
            
            # Create new app instance with clean state
            change_page = app(root)
            change_page.url_file = url_file
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
            url_file = os.path.join(script_dir, 'share_url.txt')
            
            # Clear any existing URL file
            if os.path.exists(url_file):
                os.remove(url_file)
            
            # Create new app instance with clean state
            change_page = app(root)
            change_page.url_file = url_file
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
        self.url_file = None
        self.page1()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        try:
            # Stop server process if running
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait()
            
            # Clean up URL file if it exists
            if self.url_file and os.path.exists(self.url_file):
                os.remove(self.url_file)
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Always destroy the window
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
        max_attempts = 20  # Increased wait time
        while attempts < max_attempts and not os.path.exists(self.url_file):
            time.sleep(0.5)
            attempts += 1
            
        if not os.path.exists(self.url_file):
            error_label = tk.Label(self.frame2, text="Error: Could not get sharing URL", font=('Arial', 12))
            error_label.pack(pady=10)
            return
            
        try:
            # Read the URL from the file
            with open(self.url_file, 'r') as f:
                url = f.read().strip()
            
            if not url:  # Check if URL is empty
                raise Exception("No URL found")
                
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

