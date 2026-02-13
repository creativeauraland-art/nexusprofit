import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser

# NexusProfit: YouTube OAuth2 Token Generator
# Run this locally once to get your REFRESH_TOKEN

CLIENT_ID = input("Enter your YOUTUBE_CLIENT_ID: ").strip()
CLIENT_SECRET = input("Enter your YOUTUBE_CLIENT_SECRET: ").strip()

REDIRECT_URI = "http://localhost:8080"
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = "https://www.googleapis.com/auth/youtube.upload"

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"[DEBUG] Received request: {self.path}")
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Success!</h1><p>You can close this window and check your terminal.</p>")
            
            print("[DEBUG] Exchanging code for tokens...")
            # Exchange code for tokens
            payload = {
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            res = requests.post(TOKEN_URL, data=payload)
            tokens = res.json()
            
            if 'error' in tokens:
                print(f"❌ Error from Google: {tokens.get('error_description', tokens['error'])}")
                os._exit(1)

            refresh_token = tokens.get('refresh_token')
            
            print("\n" + "="*50)
            if refresh_token:
                print("💎 YOUR REFRESH TOKEN IS BELOW 💎")
                print("="*50)
                print(refresh_token)
                print("="*50)
                print("Copy this carefully into your GitHub Secrets as YOUTUBE_REFRESH_TOKEN")
            else:
                print("⚠️ WARNING: No Refresh Token received.")
                print("This usually happens if you already authorized the app once.")
                print("Try going to Google Security settings and Revoke access to 'NexusProfit' first.")
                print("OR just copy the full response for debugging:")
                print(json.dumps(tokens, indent=2))
            print("="*50)
            
            os._exit(0)
        else:
            print("[DEBUG] No 'code' found in request.")
            self.send_response(400)
            self.end_headers()

def run_server():
    server = HTTPServer(('localhost', 8080), OAuthHandler)
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPES,
        'access_type': 'offline',
        'prompt': 'consent'
    }
    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    
    print(f"\n🚀 Opening browser for authorization...")
    print(f"If it doesn't open automatically, go here:\n{url}\n")
    webbrowser.open(url)
    server.handle_request()

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: You must provide a Client ID and Secret.")
    else:
        run_server()
