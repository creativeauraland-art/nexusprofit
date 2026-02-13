import os
import requests
import json
import time
import random

# VERSION 5.0-GHOST: Radical Safety & Stealth Integration
print("[DIAG] core/pinterest.py loaded: VERSION 5.0-GHOST")

class PinterestAI:
    """
    PinterestAI: Handles direct API-based pinning with Radical Safety (GHOST).
    Uses Pinterest API V5 with Anti-Ban metadata variation.
    """
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_API_KEY")
        self.api_base = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.board_id = None
        self.backoff_active = False

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
                if response.status_code == 401:
                    print(f"[PinterestAI] Board Discovery Failed: 401 Unauthorized. PLEASE REFRESH YOUR PINTEREST_API_KEY.")
                else:
                    print(f"[PinterestAI] Board Discovery Failed: {response.status_code}")
        except Exception as e:
            print(f"[PinterestAI] Board Discovery Error: {e}")
        return None

    def post_pin(self, title, description, link, image_url):
        """Posts a Pin directly via the Pinterest API V5 with safety jitter."""
        if self.backoff_active:
            print("[PinterestAI] GHOST Safety: Backoff active. Skipping post.")
            return False

        if not self.access_token:
            print("[PinterestAI] Error: PINTEREST_API_KEY not found.")
            return False

        board_id = self._get_active_board()
        if not board_id:
            return False

        # Metadata Variation (GHOST Entropy)
        variations = [
            f"REVEALED: {description}",
            f"{description} (Exclusive 2025 Review)",
            f"Why everyone is talking about {title}... {description}",
            f"The truth about {title}: {description[:100]}..."
        ]
        stealth_description = random.choice(variations)[:500]

        print(f"[PinterestAI] Posting Stealth Pin: {title[:30]}...")
        
        payload = {
            "title": title[:100],
            "description": stealth_description,
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
                print(f"[PinterestAI] SUCCESS: Ghost Pin Created (ID: {pin_id})")
                return True
            elif response.status_code == 429:
                print("[PinterestAI] WARNING: Rate limit (429) hit! Activating GHOST Backoff.")
                self.backoff_active = True
                return False
            else:
                print(f"[PinterestAI] FAIL: Status {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[PinterestAI] API Error: {e}")
            return False

if __name__ == "__main__":
    # Test Discovery
    p = PinterestAI()
    p._get_active_board()
