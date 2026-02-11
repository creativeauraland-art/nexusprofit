from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI
from core.motion import MotionAI
from core.link import LinkAI
from core.vocal import VocalAI
import time
import os

def update_storefront(products):
    """Injects new products into index.html for a dynamic storefront."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        product_html = ""
        for p in products:
            product_html += f"""
            <div class="card">
                <span style="color: #38bdf8; font-size: 0.8rem; font-weight: bold;">[EXCLUSIVE DEAL]</span>
                <h2>{p['name']}</h2>
                <p>High-Value Solution in {p['niche']}. Secure your spot today.</p>
                <a href="{p['link']}" class="btn" target="_blank">Access Now</a>
            </div>
            """
        
        start_tag = "<!-- DYNAMIC_PRODUCTS_START -->"
        end_tag = "<!-- DYNAMIC_PRODUCTS_END -->"
        
        if start_tag in content and end_tag in content:
            head = content.split(start_tag)[0]
            tail = content.split(end_tag)[1]
            new_content = f"{head}{start_tag}{product_html}{end_tag}{tail}"
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("[Engine] Storefront updated with new products.")
    except Exception as e:
        print(f"[Engine] Storefront update failed: {e}")

def main():
    USER_ID = "creative_aura"
    print(f"--- NexusProfit | $1,000/Day Mode | USER: {USER_ID} ---")
    
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    motion = MotionAI()
    link_ai = LinkAI(USER_ID)
    vocal = VocalAI()
    
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    
    # List of High-Value Niches to Orbit
    NICHES = ["AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech"]
    
    products_to_list = []
    rss_items = []
    
    for niche in NICHES:
        print(f"\n--- Orbiting Niche: {niche} ---")
        
        # 1. Select High-Ticket Product
        # We find a product matching the niche or pick a random high-ticket one
        product = link_ai.get_next_product()
        
        # 2. Brillian Hook Generation (Smart Work)
        hook = persona.generate_viral_hook(product['name'], niche)
        print(f"[SmartAI] Hook Generated: {hook}")
        
        # 3. Assets Generation
        timestamp = int(time.time())
        safe_name = product['name'].replace(" ", "_").lower()[:10]
        
        # Static Image
        img_path = f"assets/{safe_name}_{timestamp}.png"
        persona.generate_pin_image(hook, f"Earn {product['commission']} with {product['name']}", img_path)
        
        # Voiceover
        audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
        vocal.generate_voiceover(hook, audio_path)
        
        # Hyper-Reel (Reel + Voice)
        video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
        motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
        
        # 4. Sync
        products_to_list.append(product)
        rss_items.append({
            "title": hook,
            "link": f"{GH_PAGES_BASE}/index.html",
            "description": f"Check out {product['name']} - {hook}",
            "image_url": f"{GH_PAGES_BASE}/{img_path}"
        })
        
        # Randomized delay (Zero-Ban safety)
        time.sleep(random.randint(2, 5))

    # 5. Global Deployment
    update_storefront(products_to_list)
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("\n--- Hyper-Growth Cycle Finished: All Platforms Live ---")

if __name__ == "__main__":
    main()
