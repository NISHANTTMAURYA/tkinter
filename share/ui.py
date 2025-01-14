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
import shutil

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
            
            # Don't clean temp directory here anymore
            
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
        files = filedialog.askopenfilenames(title="Select files to share", filetypes=[("All files", "*.*")])
        if not files:  # If user cancels selection
            return
            
        print(f"\nDebug: Selected files:")
        for file in files:
            print(f"- {file}")
        
        try:
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(script_dir, 'http_server.py')
            url_file = os.path.join(script_dir, 'share_url.txt')
            temp_dir = os.path.join(script_dir, 'temp_serve')
            
            print(f"\nDebug: Absolute paths:")
            print(f"Script dir: {os.path.abspath(script_dir)}")
            print(f"Server path: {os.path.abspath(server_path)}")
            print(f"Temp dir: {os.path.abspath(temp_dir)}")
            
            # Clear any existing URL file
            if os.path.exists(url_file):
                os.remove(url_file)
            
            # Clean and recreate temp directory
            if os.path.exists(temp_dir):
                print(f"Debug: Removing existing temp directory")
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            print(f"Debug: Created fresh temp directory at {os.path.abspath(temp_dir)}")
            
            # Copy all selected files to temp directory
            print("\nDebug: Copying files to temp directory:")
            for file_path in files:
                dest_path = os.path.join(temp_dir, os.path.basename(file_path))
                print(f"Copying {file_path} -> {dest_path}")
                shutil.copy2(file_path, dest_path)
                # Verify file was copied
                if os.path.exists(dest_path):
                    print(f"Successfully copied: {os.path.basename(dest_path)} ({os.path.getsize(dest_path)} bytes)")
                else:
                    print(f"Warning: Failed to copy {os.path.basename(file_path)}")
            
            # Verify files in temp directory
            print("\nDebug: Files in temp directory before server start:")
            temp_files = os.listdir(temp_dir)
            for file in temp_files:
                file_path = os.path.join(temp_dir, file)
                print(f"- {file} ({os.path.getsize(file_path)} bytes)")
            
            if not temp_files:
                raise Exception("No files were copied to temp directory")
            
            # Create new app instance with clean state
            change_page = app(root)
            change_page.url_file = url_file
            # Important: Change - we're serving from temp_dir but telling server it's a folder
            change_page.server_process = subprocess.Popen(['python3', server_path, temp_dir, 'folder', url_file])
            
            # Wait briefly to ensure server starts
            time.sleep(1)
            
            # Verify temp directory still exists and has files
            print("\nDebug: Verifying temp directory after server start:")
            if os.path.exists(temp_dir):
                files_after = os.listdir(temp_dir)
                print(f"Temp directory exists at {os.path.abspath(temp_dir)}")
                print(f"Files in temp_serve: {files_after}")
                for file in files_after:
                    file_path = os.path.join(temp_dir, file)
                    print(f"- {file} ({os.path.getsize(file_path)} bytes)")
            else:
                print(f"Warning: Temp directory no longer exists at {os.path.abspath(temp_dir)}!")
            
            change_page.page2()
            
        except Exception as e:
            print(f"Error starting server: {e}")
            print(f"Stack trace: {traceback.format_exc()}")
        
    except Exception as e:
        print(f"Error in import_file: {e}")
        print(f"Stack trace: {traceback.format_exc()}")





class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x600")  # Smaller, mre compact window
        self.master.configure(bg='#2C2C2C')  # Dark background
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

        # Main frame with padding and dark cream background
        self.frame1 = tk.Frame(self.master, bg='#2A2829')  # Darker background
        self.frame1.pack(expand=True, fill='both', padx=20, pady=20)

        # Title with enhanced styling
        title = tk.Label(
            self.frame1, 
            text='Share Files Securely',
            font=('Helvetica', 24, 'bold'),
            fg='#E8D5C4',  # Cream colored text
            bg='#2A2829',
            pady=30
        )
        title.pack()

        # Container for buttons
        button_frame = tk.Frame(self.frame1, bg='#2A2829')
        button_frame.pack(expand=True)

        # Enhanced button styling
        button_style = {
            'font': ('Helvetica', 14),
            'width': 18,
            'height': 2,
            'bd': 0,
            'relief': 'flat',
            'cursor': 'hand2',
            'borderwidth': 0,
            'fg': 'black',          # Force black text
            'activeforeground': 'black'  # Keep black even when clicked
        }

        button1 = tk.Button(
            button_frame,
            text="Share a File",
            command=import_file,
            bg='#3E6D9C',
            **button_style
        )
        button1.pack(pady=15)

        button2 = tk.Button(
            button_frame,
            text="Share a Folder",
            command=import_folder,
            bg='#3E6D9C',
            **button_style
        )
        button2.pack(pady=15)

        # Modified hover effects (only changes background)
        def on_enter(e):
            e.widget['background'] = '#2B4865'

        def on_leave(e):
            e.widget['background'] = '#3E6D9C'

        # Add rounded corners and hover effects
        for button in (button1, button2):
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            # Round corners using canvas
            button.configure(highlightthickness=0)
            radius = 15  # Adjust for more/less curve
            button.configure(relief='flat', borderwidth=0)

    def page2(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.frame2 = tk.Frame(self.master, bg='#2A2829')
        self.frame2.pack(expand=True, fill='both', padx=20, pady=20)

        # Update title styling
        title_label = tk.Label(
            self.frame2,
            text="File Sharing Active",
            font=('Helvetica', 24, 'bold'),
            fg='#E8D5C4',
            bg='#2A2829',
            pady=20
        )
        title_label.pack()

        try:
            # Read URL with timeout
            url = None
            start_time = time.time()
            while time.time() - start_time < 10:
                if os.path.exists(self.url_file):
                    with open(self.url_file, 'r') as f:
                        url = f.read().strip()
                    if url:
                        break
                time.sleep(0.5)

            if not url:
                raise Exception("Could not get sharing URL")

            # Create a frame to hold URL and copy button horizontally
            url_frame = tk.Frame(self.frame2, bg='#2C2C2C')
            url_frame.pack(pady=(0, 20))

            url_text = tk.Label(
                url_frame,  # Changed parent to url_frame
                text=url,
                font=('Helvetica', 10),
                fg='#B0B0B0',
                bg='#2C2C2C',
                wraplength=300  # Slightly reduced to make space for button
            )
            url_text.pack(side='left', padx=(0, 10))

            def copy_url():
                self.master.clipboard_clear()
                self.master.clipboard_append(url)
                copy_btn.config(text="Copied!")
                # Reset button text after 2 seconds
                self.master.after(2000, lambda: copy_btn.config(text="Copy"))

            copy_btn = tk.Button(
                url_frame,
                text="Copy",
                command=copy_url,
                font=('Helvetica', 10),
                bg='#3E6D9C',
                fg='black',
                activeforeground='black',
                padx=10,
                relief='flat',
                cursor='hand2'
            )
            copy_btn.pack(side='left')

            # QR Code section
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="white", back_color="#2C2C2C")
            qr_image = qr_image.resize((250, 250))
            qr_photo = ImageTk.PhotoImage(qr_image)

            qr_title = tk.Label(
                self.frame2,
                text="Scan QR Code:",
                font=('Helvetica', 12, 'bold'),
                fg='#E0E0E0',
                bg='#2C2C2C'
            )
            qr_title.pack(pady=(0, 10))

            self.qr_label = tk.Label(self.frame2, image=qr_photo, bg='#2C2C2C')
            self.qr_label.image = qr_photo
            self.qr_label.pack(pady=10)

            # Share Another File button with improved styling
            def share_another():
                if self.server_process:
                    self.server_process.terminate()
                    self.server_process = None
                cleanup_ports_background()
                self.page1()

            share_btn = tk.Button(
                self.frame2,
                text="Share Another File",
                command=share_another,
                font=('Helvetica', 14, 'bold'),
                bg='#3E6D9C',
                fg='black',             # Force black text
                activeforeground='black',  # Keep black even when clicked
                padx=30,
                pady=12,
                relief='flat',
                cursor='hand2'
            )
            share_btn.pack(pady=30)

            # Modified hover effects (only changes background)
            def on_enter(e):
                e.widget['background'] = '#2B4865'

            def on_leave(e):
                e.widget['background'] = '#3E6D9C'

            share_btn.bind("<Enter>", on_enter)
            share_btn.bind("<Leave>", on_leave)

            # Update retry button if present
            if 'retry_btn' in locals():
                retry_btn.configure(
                    bg='#3E6D9C',
                    fg='black',
                    activeforeground='black',
                    font=('Helvetica', 12, 'bold')
                )

        except Exception as e:
            error_label = tk.Label(
                self.frame2,
                text=f"Error: {e}",
                font=('Helvetica', 12),
                fg='#FF6B6B',
                bg='#2C2C2C'
            )
            error_label.pack(pady=10)

            retry_btn = tk.Button(
                self.frame2,
                text="Try Again",
                command=self.page1,
                font=('Helvetica', 12),
                bg='#3D5A80',
                fg='white',
                padx=20,
                pady=10,
                relief='flat',
                cursor='hand2'
            )
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

