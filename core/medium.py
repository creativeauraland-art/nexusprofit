import os
import requests

# VERSION 6.0-OMNI: Medium.com Authority Ranking
print("[DIAG] core/medium.py loaded: VERSION 6.0-OMNI")

class MediumAI:
    """
    MediumAI: Automatically cross-posts sales-hardened reviews to Medium 
    to dominate Google Search rankings.
    """
    def __init__(self):
        self.access_token = os.getenv("MEDIUM_ACCESS_TOKEN")
        self.api_base = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.user_id = None

    def _get_user_id(self):
        """Fetches the Medium User ID associated with the token."""
        if self.user_id:
            return self.user_id
            
        try:
            response = requests.get(f"{self.api_base}/me", headers=self.headers)
            if response.status_code == 200:
                self.user_id = response.json().get("data", {}).get("id")
                return self.user_id
            else:
                print(f"[MediumAI] Failed to get Me: {response.status_code}")
        except Exception as e:
            print(f"[MediumAI] API Error: {e}")
        return None

    def post_article(self, title, content_markdown, canonical_url, tags=None):
        """Publishes a review article to Medium."""
        if not self.access_token:
            print("[MediumAI] Error: MEDIUM_ACCESS_TOKEN not found.")
            return False

        user_id = self._get_user_id()
        if not user_id:
            return False

        print(f"[MediumAI] Cross-Posting to Medium: {title[:30]}...")
        
        # Prepare tags
        if not tags:
            tags = ["Affiliate Marketing", "Passive Income", "AI Tools"]

        payload = {
            "title": title,
            "contentFormat": "markdown",
            "content": f"# {title}\n\n*Originally published at {canonical_url}*\n\n{content_markdown}",
            "canonicalUrl": canonical_url,
            "tags": tags[:5],
            "publishStatus": "public" 
        }

        try:
            response = requests.post(
                f"{self.api_base}/users/{user_id}/posts", 
                headers=self.headers, 
                json=payload
            )
            if response.status_code == 201:
                post_url = response.json().get("data", {}).get("url")
                print(f"[MediumAI] SUCCESS: Article Live on Medium! URL: {post_url}")
                return True
            else:
                print(f"[MediumAI] FAIL: Status {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[MediumAI] Request Error: {e}")
            return False

if __name__ == "__main__":
    # Test block
    m = MediumAI()
    print("MediumAI Initialized.")
