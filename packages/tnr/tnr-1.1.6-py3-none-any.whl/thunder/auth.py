import click
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
from thunder import api
from thunder import auth_helper

CLIENT_ID = "YOUR_FIREBASE_CLIENT_ID"
REDIRECT_URI = "http://localhost:5000"
OAUTH_URL = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=token&scope=email profile"

# Global variable to store the token
auth_token = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_token
        path = self.path
        if path.startswith("/?"):
            query = path.split("?")[1]
            params = dict(qc.split("=") for qc in query.split("&"))
            if "access_token" in params:
                auth_token = params["access_token"]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authentication successful. You can close this window.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authentication failed.")

def run_server():
    server = HTTPServer(('localhost', 5000), OAuthHandler)
    server.serve_forever()

def login() -> tuple:
    threading.Thread(target=run_server, daemon=True).start()
    webbrowser.open(OAUTH_URL)
    click.echo("Opening browser for authentication...")

    global auth_token
    while auth_token is None:
        pass

    # Save the token for future use
    auth_helper.save_tokens(auth_token, auth_token, "")  # Assuming refresh token is same for simplicity

    click.echo("Logged in successfully.")
    return auth_token, auth_token, ""

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
