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
import io
import zipfile

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def list_directory(self, path):
        try:
            # List files in directory
            files = os.listdir(path)
            files = [f for f in files if f != "index.html" and os.path.isfile(os.path.join(path, f))]
            files.sort()

            # Create HTML content with JavaScript for individual downloads
            html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Shared Files from directory {os.path.basename(os.getcwd())}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: #f5f5f5;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        color: #333;
                        margin-bottom: 20px;
                    }}
                    .file-list {{
                        list-style: none;
                        padding: 0;
                    }}
                    .file-item {{
                        display: flex;
                        align-items: center;
                        padding: 10px;
                        border-bottom: 1px solid #eee;
                    }}
                    .file-name {{
                        flex-grow: 1;
                        margin-right: 10px;
                    }}
                    .download-btn {{
                        background: #4CAF50;
                        color: white;
                        padding: 8px 15px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        text-decoration: none;
                    }}
                    .download-btn:hover {{
                        background: #45a049;
                    }}
                    .download-all {{
                        display: block;
                        width: 200px;
                        margin: 20px auto;
                        text-align: center;
                        background: #2196F3;
                    }}
                    .download-all:hover {{
                        background: #1976D2;
                    }}
                    .download-all-files {{
                        display: block;
                        width: 200px;
                        margin: 10px auto;
                        text-align: center;
                        background: #FF5722;
                    }}
                    .download-all-files:hover {{
                        background: #F4511E;
                    }}
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        .container {{
                            padding: 10px;
                        }}
                        .file-item {{
                            flex-direction: column;
                            align-items: flex-start;
                        }}
                        .download-btn {{
                            margin-top: 10px;
                        }}
                    }}
                </style>
                <script>
                    function downloadAllFiles() {{
                        const files = {str([f for f in files])};
                        let delay = 0;
                        files.forEach(file => {{
                            setTimeout(() => {{
                                const link = document.createElement('a');
                                link.href = file;
                                link.download = file;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                            }}, delay);
                            delay += 500; // 500ms delay between downloads
                        }});
                    }}
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>Shared Files from directory {os.path.basename(os.getcwd())}</h1>
                    <ul class="file-list">
            '''

            # Add files to HTML
            for file in files:
                html += f'''
                <li class="file-item">
                    <span class="file-name">{file}</span>
                    <a href="{file}" class="download-btn" download>Download</a>
                </li>
                '''

            # Add both download options if there are multiple files
            if len(files) > 1:
                html += f'''
                    </ul>
                    <a href="download-all" class="download-btn download-all">Download All as ZIP</a>
                    <a href="#" onclick="downloadAllFiles()" class="download-btn download-all-files">Download All Files</a>
                </div>
            </body>
            </html>
            '''
            else:
                html += '''
                    </ul>
                </div>
            </body>
            </html>
            '''

            # Send response
            encoded = html.encode('utf-8', 'replace')
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return None

        except Exception as e:
            print(f"Error in list_directory: {e}")
            return super().list_directory(path)

    def do_GET(self):
        if self.path == '/download-all':
            try:
                # Get the current directory name
                current_dir = os.path.basename(os.getcwd())
                zip_filename = f"{current_dir}.zip"
                
                # Create ZIP file in memory
                memory_file = io.BytesIO()
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    # Add all files in current directory to ZIP
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file != "index.html":  # Skip index.html
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, os.getcwd())
                                zf.write(file_path, arcname)

                # Get ZIP file content
                memory_file.seek(0)
                content = memory_file.getvalue()

                # Send ZIP file with directory name
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', f'attachment; filename="{zip_filename}"')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
                return

            except Exception as e:
                print(f"Error creating ZIP: {e}")
                self.send_error(500, "Internal server error")
                return

        return super().do_GET()

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