import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import time
import subprocess
import os
import threading
import importlib.util
import traceback
import ngrok

from tkinter.filedialog import SaveFileDialog,askdirectory
def cleanup_ports_background():
    def cleanup():
        print("Starting background port cleanup...")
        try:
            # First kill any existing ngrok processes
            print("Checking for ngrok processes...")
            try:
                # More thorough ngrok cleanup
                ngrok.kill()  # Kill through pyngrok
                time.sleep(0.5)  # Brief wait
                
                # Additional ngrok process cleanup
                subprocess.run(['pkill', 'ngrok'], stderr=subprocess.DEVNULL)
                print("Killed ngrok processes")
            except Exception as e:
                print(f"Note: Ngrok cleanup: {e}")
            
            # Then kill any process on port 8000
            print("Checking for processes on port 8000...")
            try:
                cmd = "lsof -ti :8000"
                pid = subprocess.check_output(cmd, shell=True).decode().strip()
                if pid:
                    print(f"Found process {pid} on port 8000, killing it...")
                    subprocess.run(['kill', '-9', pid], stderr=subprocess.DEVNULL)
                    print(f"Killed process {pid}")
            except subprocess.CalledProcessError:
                print("No process found on port 8000")
            except Exception as e:
                print(f"Error checking port 8000: {e}")

            # Wait for ports to be fully released
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error during cleanup: {e}")

    # Run cleanup in background thread
    thread = threading.Thread(target=cleanup)
    thread.daemon = True
    thread.start()

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
            if self.server_process:
                # Kill the server process
                self.server_process.terminate()
                self.server_process.wait(timeout=1)
            
            # Clean up URL file
            if self.url_file and os.path.exists(self.url_file):
                os.remove(self.url_file)
                
            # Ensure ngrok is killed
            ngrok.kill()
            
            # Run final cleanup in background
            cleanup_ports_background()
                
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
        title_label = tk.Label(self.frame2, text="File Sharing Active", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        try:
            # Read the URL from the file with timeout
            url = None
            start_time = time.time()
            while time.time() - start_time < 10:  # 10 second timeout
                if os.path.exists(self.url_file):
                    with open(self.url_file, 'r') as f:
                        url = f.read().strip()
                    if url:
                        break
                time.sleep(0.5)
            
            if not url:
                raise Exception("Could not get sharing URL")
                
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
            qr_image = qr_image.resize((300, 300))
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Display QR Code
            qr_title = tk.Label(self.frame2, text="Scan QR Code:", font=('Arial', 12))
            qr_title.pack(pady=5)
            
            self.qr_label = tk.Label(self.frame2, image=qr_photo)
            self.qr_label.image = qr_photo
            self.qr_label.pack(pady=10)
            
            # Share Another File button
            def share_another():
                if self.server_process:
                    self.server_process.terminate()
                    self.server_process = None
                cleanup_ports_background()
                self.page1()
            
            share_btn = tk.Button(self.frame2, text="Share Another File", 
                                command=share_another,
                                font=('Arial', 12),
                                bg='#4CAF50',
                                fg='white',
                                padx=20,
                                pady=10)
            share_btn.pack(pady=20)
            
        except Exception as e:
            error_label = tk.Label(self.frame2, text=f"Error: {e}")
            error_label.pack(pady=10)
            # Add retry button
            retry_btn = tk.Button(self.frame2, text="Try Again", 
                                command=self.page1,
                                font=('Arial', 12))
            retry_btn.pack(pady=10)

    def update_shared_content(self, path, is_file=False):
        print(f"\nAttempting to update shared content:")
        print(f"Path: {path}")
        print(f"Is file: {is_file}")
        
        if self.server_process and self.server_process.poll() is None:
            print("Server is running")
            try:
                # Update the server's directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                server_path = os.path.join(script_dir, 'http_server.py')
                print(f"Server path: {server_path}")
                
                # Use same URL file
                if not hasattr(self, 'url_file'):
                    self.url_file = os.path.join(script_dir, 'share_url.txt')
                print(f"URL file: {self.url_file}")
                
                # Update the server's directory
                print("Loading server module...")
                spec = importlib.util.spec_from_file_location("http_server", server_path)
                server_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(server_module)
                
                print("Calling update_directory...")
                if server_module.MyHttpRequestHandler.update_directory(path, is_file):
                    print("Update successful, refreshing page...")
                    # Refresh the page to show current content
                    self.page2()
                else:
                    print("Update failed")
                    tk.messagebox.showerror("Error", "Failed to update shared content")
            except Exception as e:
                print(f"Error during update: {e}")
                print(f"Exception type: {type(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                tk.messagebox.showerror("Error", f"Error updating shared content: {e}")
        else:
            print("Server not running")
            tk.messagebox.showerror("Error", "Server not running")

app(root)

root.mainloop()

