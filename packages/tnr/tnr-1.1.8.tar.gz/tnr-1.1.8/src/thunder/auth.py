import click
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import os
from thunder import api
from thunder import auth_helper

CLIENT_ID = "thunder-426102"
REDIRECT_URI = "https://console.thundercompute.com/login-success"
OAUTH_URL = "https://console.thundercompute.com/login-cli"

# Global variable to store the token
auth_token = None
refresh_token = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        global auth_token, refresh_token
        if self.path == "/tokens":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data)
            auth_token = params.get("token")
            refresh_token = params.get("refreshToken")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "tokens received"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Override to suppress logging
        return

def run_server():
    server = HTTPServer(('localhost', 5324), OAuthHandler)
    server.serve_forever()

def is_running_in_docker():
    """Check if the script is running inside a Docker container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return any('docker' in line for line in ifh)
    except Exception:
        return False

def open_browser(url):
    if "WSL_DISTRO_NAME" in os.environ:
        # Running in WSL
        os.system(f"powershell.exe /c start {url}")
    elif is_running_in_docker():
        # Running inside a Docker container
        click.echo(f"Please open the following URL in your browser: {url}")
    else:
        # Not running in WSL or Docker
        webbrowser.open(url)

def login() -> tuple:
    threading.Thread(target=run_server, daemon=True).start()
    open_browser(OAUTH_URL)
    click.echo("Opening browser for authentication...")

    global auth_token, refresh_token
    while auth_token is None:
        pass

    # Save the tokens for future use
    auth_helper.save_tokens(auth_token, refresh_token, "")
    
    click.echo("Logged in successfully.")
    return auth_token, refresh_token, ""

def logout():
    auth_helper.delete_data()
    click.echo("Logged out successfully.")

def handle_token_refresh(refresh_token: str) -> tuple:
    new_id_token, new_refresh_token, uid = api.refresh_id_token(refresh_token)
    if new_id_token and new_refresh_token:
        auth_helper.save_tokens(new_id_token, new_refresh_token, uid)
        return new_id_token, new_refresh_token, uid
    return None, None, None

def load_tokens() -> tuple:
    credentials_file_path = auth_helper.get_credentials_file_path()
    try:
        with open(credentials_file_path, "r", encoding="utf-8") as file:
            encrypted_id_token = file.readline().strip()
            encrypted_refresh_token = file.readline().strip()
            uid = file.readline().strip()
            if encrypted_id_token and encrypted_refresh_token:
                return (
                    auth_helper.decrypt_data(encrypted_id_token),
                    auth_helper.decrypt_data(encrypted_refresh_token),
                    uid,
                )
            else:
                return None, None, None
    except FileNotFoundError:
        return None, None, None
