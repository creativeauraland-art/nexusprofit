import os
import requests

# VERSION 6.1-OMNI: Medium.com Import Assistant (API Bypass)
print("[DIAG] core/medium.py loaded: VERSION 6.1-OMNI")

class MediumAI:
    """
    MediumAI: Since the API is closed, this generates 'One-Click Import' 
    links to ensure our high-authority distribution remains active.
    """
    def __init__(self):
        # API is dead for new users, shifting to assistant mode
        self.import_base = "https://medium.com/p/import"

    def generate_import_link(self, title, canonical_url):
        """
        Generates a direct link to Medium's import tool for the generated review.
        """
        import_url = f"{self.import_base}?url={canonical_url}"
        
        print("\n" + "🏮"*20)
        print("🚀 MEDIUM AUTHORITY ACTION REQUIRED 🚀")
        print(f"To rank '{title}' on Google's First Page:")
        print(f"1. Click here: {import_url}")
        print("2. Medium will auto-fetch your review.")
        print("3. Click 'Publish' to go live.")
        print("🏮"*20 + "\n")
        
        return import_url

    def post_article(self, title, content_markdown, canonical_url, tags=None):
        """Assistant version: Logs the import link for the user."""
        return self.generate_import_link(title, canonical_url)

if __name__ == "__main__":
    # Test block
    m = MediumAI()
    print("MediumAI Initialized.")
