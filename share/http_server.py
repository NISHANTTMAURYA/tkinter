import http.server
import socketserver
import os
import sys
import shutil
from pyngrok import ngrok
import signal
import json

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

def start_server(path, type_of_share, url_file):
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    if not path:
        print("No path selected!")
        sys.exit(1)
    
    # Create a temporary directory for serving files
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_serve')
    os.makedirs(temp_dir, exist_ok=True)
    
    if type_of_share == 'file':
        # If it's a file, copy it to the temp directory
        file_name = os.path.basename(path)
        dest_path = os.path.join(temp_dir, file_name)
        shutil.copy2(path, dest_path)
        os.chdir(temp_dir)
        print(f"Serving file: {file_name}")
    else:
        # If it's a folder, serve it directly
        os.chdir(path)
        print(f"Serving directory: {path}")
    
    handler_object = MyHttpRequestHandler
    
    # Start ngrok before starting the server
    public_url = start_ngrok(PORT)
    if not public_url:
        print("Failed to start ngrok tunnel")
        sys.exit(1)
    
    # Write the URL to the specified file
    with open(url_file, 'w') as f:
        f.write(public_url)

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
            # Clean up temp directory if we were serving a file
            if type_of_share == 'file' and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            # Kill the ngrok tunnel
            ngrok.kill()
            print("Ngrok tunnel closed.")
            print("Server closed.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        start_server(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python http_server.py <path> <type> <url_file>")
        print("type can be 'file' or 'folder'")
        sys.exit(1)