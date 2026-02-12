import random
import requests
import re
from bs4 import BeautifulSoup

class LinkAI:
    """
    LinkAI: Responsible for selecting high-converting products and building affiliate links.
    """
    def __init__(self, user_id):
        self.user_id = user_id
        # Curated Elite List
        self.products = [
            {"id": "530050", "name": "ProDentim", "niche": "Health", "commission": "$120", "trend_tags": ["gut health"]},
            {"id": "520025", "name": "The Genius Wave", "niche": "Personal Development", "commission": "$50", "trend_tags": ["mindfulness"]},
            {"id": "510010", "name": "His Secret Obsession", "niche": "Dating", "commission": "$55", "trend_tags": ["aura beauty"]},
            {"id": "490088", "name": "No Grid Survival", "niche": "Survival", "commission": "$40", "trend_tags": ["DIY home"]},
            {"id": "421676", "name": "Tube Mastery", "niche": "Business", "commission": "$250", "trend_tags": ["side hustle"]}
        ]

    def automate_marketplace(self, niche="Business"):
        """Scrapes trending products."""
        print(f"[LinkAI] Discovering Products for {niche}...")
        url = f"https://www.digistore24.com/en/marketplace?search_category={niche}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                # Basic scraping logic using BeautifulSoup
                soup = BeautifulSoup(res.text, 'html.parser')
                # (Scraping logic shortened for stability)
                ids = re.findall(r'data-product-id="(\d+)"', res.text)
                if ids:
                    return {"id": ids[0], "name": f"Discovered {niche} Product", "niche": niche, "link": f"https://www.digistore24.com/redir/{ids[0]}/creative_aura/"}
        except:
            pass
        return self.get_next_product()

    def get_next_product(self):
        product = random.choice(self.products)
        product["link"] = f"https://www.digistore24.com/redir/{product['id']}/creative_aura/"
        return product
