import time
import random
import os
from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI

def main():
    print("--- NexusProfit RSS Engine Started ---")
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    
    # Base URL for assets on GitHub Pages
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    
    # 1. Scout Trends
    trends = scout.find_trends()
    rss_items = []
    
    for trend in trends:
        # 2. Find High-Ticket Products
        products = scout.find_high_ticket_products(trend)
        
        for product in products:
            # 3. Generate Visual Assets
            title = f"Secret to {trend}: {product['name']}"
            desc = f"Get this {product['name']} and start earning {product['commission']}$ commissions! #affiliate #money"
            safe_trend = trend.replace(" ", "_").lower()
            timestamp = int(time.time())
            filename = f"assets/{safe_trend}_{timestamp}.png"
            
            persona.generate_pin_image(title, desc, filename)
            
            # 4. Prepare RSS Item
            rss_items.append({
                "title": title,
                "link": f"{GH_PAGES_BASE}/bridge/index.html",
                "description": desc,
                "image_url": f"{GH_PAGES_BASE}/{filename}"
            })
            
            print(f"Prepared RSS entry for: {title}")
            
    # 5. Generate/Update RSS Feed
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("--- RSS Feed Updated Successfully ---")

if __name__ == "__main__":
    main()
