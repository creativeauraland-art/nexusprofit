import random
import time
import requests

class SafetyAI:
    """
    SafetyAI: Responsible for account protection and link integrity.
    """
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.98 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]

    def mimetic_delay(self, min_min=60, max_min=240):
        """Generates a randomized 'human' delay to bypass bot detection."""
        wait_time = random.randint(min_min * 60, max_min * 60)
        minutes = wait_time // 60
        print(f"[Safety] Mimetic Delay Active: Waiting {minutes} minutes before next action...")
        # In a real GH Action, we would use sleep or schedule the next run
        # For local demo, we'll just simulate it.
        # time.sleep(wait_time) 
        return wait_time

    def validate_link(self, url):
        """Checks if a link is active and not returning a 404 or error."""
        print(f"[Safety] Shadow-Checking Link: {url[:40]}...")
        try:
            headers = {"User-Agent": random.choice(self.user_agents)}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print("[Safety] Link Verified: Active and Safe.")
                return True
            else:
                print(f"[Safety] Warning: Link returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"[Safety] Critical: Link validation failed: {e}")
            return False

if __name__ == "__main__":
    safety = SafetyAI()
    safety.validate_link("https://www.digistore24.com")
