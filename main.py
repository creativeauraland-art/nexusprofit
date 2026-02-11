import time
import random
import os
from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI
from core.motion import MotionAI

def main():
    print("--- NexusProfit Multi-Platform Engine Started ---")
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    motion = MotionAI()
    
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
            
            # Static Pin
            img_path = f"assets/{safe_trend}_{timestamp}.png"
            persona.generate_pin_image(title, desc, img_path)
            
            # Motion Reel (Instagram/YouTube)
            video_path = f"assets/reels/{safe_trend}_{timestamp}.mp4"
            motion.generate_reel(img_path, title, output_path=video_path)
            
            # 4. Prepare RSS Item (Pinterest)
            rss_items.append({
                "title": title,
                "link": f"{GH_PAGES_BASE}/index.html",
                "description": desc,
                "image_url": f"{GH_PAGES_BASE}/{img_path}"
            })
            
            print(f"Engine Cycle Complete: {title}")
            
    # 5. Generate/Update RSS Feed
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("--- Engine Cycle Finished Successfully ---")

if __name__ == "__main__":
    main()
