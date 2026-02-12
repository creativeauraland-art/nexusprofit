import os
import requests
import json
import time

# VERSION 4.0-INSTANT: Pinterest Direct API Integration
print("[DIAG] core/pinterest.py loaded: VERSION 4.0-INSTANT")

class PinterestAI:
    """
    PinterestAI: Handles direct API-based pinning to eliminate RSS delay.
    Uses Pinterest API V5.
    """
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_API_KEY")
        self.api_base = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.board_id = None

    def _get_active_board(self):
        """Discovers an active board ID if none is explicitly provided."""
        if self.board_id:
            return self.board_id
            
        print("[PinterestAI] Discovering active boards...")
        try:
            response = requests.get(f"{self.api_base}/boards", headers=self.headers)
            if response.status_code == 200:
                boards = response.json().get("items", [])
                if boards:
                    self.board_id = boards[0]['id']
                    print(f"[PinterestAI] Auto-Selected Board: {boards[0]['name']} ({self.board_id})")
                    return self.board_id
            else:
                print(f"[PinterestAI] Board Discovery Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[PinterestAI] Board Discovery Error: {e}")
        return None

    def post_pin(self, title, description, link, image_url):
        """Posts a Pin directly via the Pinterest API V5."""
        if not self.access_token:
            print("[PinterestAI] Error: PINTEREST_API_KEY not found in environment.")
            return False

        board_id = self._get_active_board()
        if not board_id:
            print("[PinterestAI] Error: No valid board ID found to pin to.")
            return False

        print(f"[PinterestAI] Posting Instant Pin: {title[:30]}...")
        
        payload = {
            "title": title[:100],
            "description": description[:500],
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            },
            "board_id": board_id
        }

        try:
            response = requests.post(f"{self.api_base}/pins", headers=self.headers, json=payload)
            if response.status_code == 201:
                pin_id = response.json().get("id")
                print(f"[PinterestAI] SUCCESS: Pin created instantly! ID: {pin_id}")
                return True
            else:
                print(f"[PinterestAI] FAIL: Status {response.status_code} - {response.text}")
                # Log if it's a rate limit issue
                if response.status_code == 429:
                    print("[PinterestAI] Rate limited. Cooling down...")
                return False
        except Exception as e:
            print(f"[PinterestAI] API Request Error: {e}")
            return False

if __name__ == "__main__":
    # Test Discovery
    p = PinterestAI()
    p._get_active_board()
