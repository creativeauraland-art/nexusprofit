import random

class LinkAI:
    """
    LinkAI: Responsible for selecting high-converting products and building affiliate links.
    """
    def __init__(self, user_id):
        self.user_id = user_id
        # High-Ticket Digistore24 Product IDs (Focus on $100+ Commissions)
        self.products = [
            {"id": "421676", "name": "Tube Mastery & Automation (2025)", "niche": "AI Automation", "commission": "$250"},
            {"id": "346981", "name": "AI Content Machine & Viral Masterclass", "niche": "Content Creation", "commission": "$120"},
            {"id": "542452", "name": "Project Serenity (Wealth & Tech)", "niche": "Crypto Tech", "commission": "$175"},
            {"id": "222222", "name": "Biohacking Secrets (Premium)", "niche": "Biohacking", "commission": "$105"},
            {"id": "333333", "name": "Solar Energy Empire Mastery", "niche": "Green Tech", "commission": "$350"}
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
