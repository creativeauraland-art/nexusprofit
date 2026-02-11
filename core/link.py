import random

class LinkAI:
    """
    LinkAI: Responsible for selecting high-converting products and building affiliate links.
    """
    def __init__(self, user_id):
        self.user_id = user_id
        # High-converting Digistore24 Product IDs (AI/Tech Niche)
        # 542452: Ultimate AI Ads (Example ID)
        # 421676: Tube Mastery (High Ticket)
        # 346981: AI Profit Masterclass
        self.products = [
            {"id": "542452", "name": "Ultimate AI Video Course", "niche": "AI Tools", "commission": "$47"},
            {"id": "421676", "name": "Tube Mastery & Automation", "niche": "Technology", "commission": "$250"},
            {"id": "346981", "name": "AI Content Machine", "niche": "AI Tools", "commission": "$39"},
            {"id": "500000", "name": "Deep Fake Marketing Pro", "niche": "Technology", "commission": "$88"}
        ]

    def get_next_product(self):
        """Pick a high-performing product and build the custom link."""
        product = random.choice(self.products)
        # Digistore24 Link Format: https://www.digistore24.com/redir/PRODUCT_ID/AFFILIATE_ID/
        product["link"] = f"https://www.digistore24.com/redir/{product['id']}/{self.user_id}/"
        return product

if __name__ == "__main__":
    link_ai = LinkAI("creative_aura")
    print(f"Generated Link: {link_ai.get_next_product()}")
