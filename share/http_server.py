import http.server
import socketserver
import os
import sys
import shutil

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def start_server(path, type_of_share):
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
    
    with socketserver.TCPServer(("", PORT), handler_object) as httpd:
        print(f"Serving at port {PORT}")
        print("Server is running. Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Server stopped.")
            httpd.server_close()
            # Clean up temp directory if we were serving a file
            if type_of_share == 'file' and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            print("Server closed.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        start_server(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python http_server.py <path> <type>")
        print("type can be 'file' or 'folder'")
        sys.exit(1)