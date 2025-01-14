import http.server
import socketserver
import os
import sys
import shutil
from pyngrok import ngrok
import signal
import json
import time
import subprocess

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def start_ngrok(port):
    try:
        # Open an Ngrok tunnel on the specified port
        https_url = ngrok.connect(port, "http").public_url
        print(f"\nNgrok Tunnel URL: {https_url}")
        print("Visit the Ngrok dashboard at http://127.0.0.1:4040 to inspect requests.")
        return https_url
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None

def signal_handler(signum, frame):
    print("\nReceived signal to terminate...")
    cleanup_and_exit()

def cleanup_and_exit():
    print("Cleaning up...")
    # Kill the ngrok tunnel
    ngrok.kill()
    print("Ngrok tunnel closed.")
    
    # Clean up temp directory if it exists
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_serve')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print("Temporary directory cleaned.")
    
    sys.exit(0)

def check_and_kill_port(port):
    print(f"Checking if port {port} is in use...")
    try:
        # Try to kill any process using the port
        cmd = f"lsof -ti :{port}"
        pid = subprocess.check_output(cmd, shell=True).decode().strip()
        if pid:
            print(f"Found process {pid} using port {port}, killing it...")
            subprocess.run(['kill', '-9', pid], stderr=subprocess.DEVNULL)
            time.sleep(1)  # Wait for the port to be released
            print(f"Killed process on port {port}")
            return True
    except subprocess.CalledProcessError:
        print(f"No process found using port {port}")
    except Exception as e:
        print(f"Error checking port {port}: {e}")
    return False

def start_server(path, type_of_share, url_file):
    print("\nStarting server setup...")
    
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    if not path:
        print("No path selected!")
        sys.exit(1)
    
    # Check and kill any process using our port
    check_and_kill_port(PORT)
    
    # Kill any existing ngrok processes
    print("Killing any existing ngrok processes...")
    ngrok.kill()
    time.sleep(1)  # Wait for ngrok to fully close
    
    # Create a temporary directory for serving files
    print("Setting up temporary directory...")
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_serve')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    if type_of_share == 'file':
        print(f"Preparing to serve file: {path}")
        file_name = os.path.basename(path)
        dest_path = os.path.join(temp_dir, file_name)
        shutil.copy2(path, dest_path)
        os.chdir(temp_dir)
        print(f"Serving file: {file_name}")
    else:
        print(f"Preparing to serve directory: {path}")
        os.chdir(path)
        print(f"Serving directory: {path}")
    
    handler_object = MyHttpRequestHandler
    
    # Start ngrok before starting the server
    print("Starting ngrok tunnel...")
    public_url = start_ngrok(PORT)
    if not public_url:
        print("Failed to start ngrok tunnel")
        sys.exit(1)
    
    # Write the URL to the specified file
    print(f"Writing URL to file: {url_file}")
    with open(url_file, 'w') as f:
        f.write(public_url)

    print("Starting HTTP server...")
    try:
        socketserver.TCPServer.allow_reuse_address = True  # Allow port reuse
        with socketserver.TCPServer(("", PORT), handler_object) as httpd:
            print(f"\nLocal server running at: http://localhost:{PORT}")
            print(f"Public URL: {public_url}")
            print("\nPress Ctrl+C to stop the server.")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                print("\nServer stopped.")
                httpd.server_close()
                cleanup_and_exit()
    except Exception as e:
        print(f"Error starting server: {e}")
        cleanup_and_exit()

if __name__ == "__main__":
    if len(sys.argv) > 3:
        start_server(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python http_server.py <path> <type> <url_file>")
        print("type can be 'file' or 'folder'")
        sys.exit(1)