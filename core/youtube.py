import os
import requests
import json
import random

# VERSION 6.0-OMNI: YouTube Shorts Automated Uploader
print("[DIAG] core/youtube.py loaded: VERSION 6.0-OMNI")

class YouTubeAI:
    """
    YouTubeAI: Handles automated Shorts uploading via Data API v3.
    Uses OAuth2 Refresh Tokens for persistent cloud automation.
    """
    def __init__(self):
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        self.access_token = None

    def _refresh_access_token(self):
        """Refreshes the OAuth2 access token using the refresh token."""
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            print("[YouTubeAI] Missing OAuth2 credentials.")
            return False

        url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                return True
            else:
                print(f"[YouTubeAI] Token Refresh Failed: {response.text}")
        except Exception as e:
            print(f"[YouTubeAI] Refresh Error: {e}")
        return False

    def upload_short(self, video_path, title, description, tags=None):
        """
        Uploads an MP4 video as a YouTube Short.
        Note: YouTube automatically identifies videos < 60s as Shorts.
        """
        if not self._refresh_access_token():
            return False

        print(f"[YouTubeAI] Uploading Short: {title[:30]}...")

        # 1. Initialize Upload (Metadata)
        url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(os.path.getsize(video_path)),
            "X-Upload-Content-Type": "video/mp4"
        }
        
        metadata = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags or ["shorts", "passiveincome", "aitools"],
                "categoryId": "22" # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        try:
            # Step 1: Get Upload URL
            res = requests.post(url, headers=headers, json=metadata)
            if res.status_code != 200:
                print(f"[YouTubeAI] Metadata rejected: {res.text}")
                return False
            
            upload_url = res.headers.get("Location")
            
            # Step 2: Upload Binary
            with open(video_path, "rb") as f:
                upload_res = requests.put(upload_url, data=f)
                
            if upload_res.status_code in [200, 201]:
                video_id = upload_res.json().get("id")
                print(f"[YouTubeAI] SUCCESS: Short Published! ID: {video_id}")
                return True
            else:
                print(f"[YouTubeAI] Upload failed: {upload_res.text}")
                return False
                
        except Exception as e:
            print(f"[YouTubeAI] Request Error: {e}")
            return False

if __name__ == "__main__":
    y = YouTubeAI()
    print("YouTubeAI Initialized.")
