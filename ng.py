from pyngrok import ngrok

def start_ngrok(port):
    """
    Starts an Ngrok tunnel for the specified port and returns the public HTTPS URL.
    """
    # Open an Ngrok tunnel on the specified port
    https_url = ngrok.connect(port, "http").public_url
    print(f"Ngrok Tunnel URL: {https_url}")
    print("Visit the Ngrok dashboard at http://127.0.0.1:4040 to inspect requests.")
    return https_url

if __name__ == "__main__":
    # Replace this with the port your local server is running on
    LOCAL_PORT = 8000

    # Start Ngrok and expose the local server
    try:
        print("Starting Ngrok...")
        public_url = start_ngrok(LOCAL_PORT)
        print(f"Your local server is now accessible at: {public_url}")
        print("Press Ctrl+C to stop the tunnel.")
        
        # Keep the tunnel open
        input("Press Enter to terminate the tunnel...")
    except KeyboardInterrupt:
        print("\nNgrok tunnel stopped.")
    finally:
        ngrok.kill()
