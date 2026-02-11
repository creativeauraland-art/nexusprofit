from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI
from core.motion import MotionAI
from core.link import LinkAI
from core.vocal import VocalAI
from core.safety import SafetyAI
from core.pseo import PSEOAI
import time
import os
import random

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
    print(f"--- NexusProfit | ZERO-RISK MODE | USER: {USER_ID} ---")
    
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    motion = MotionAI()
    link_ai = LinkAI(USER_ID)
    vocal = VocalAI()
    safety = SafetyAI()
    pseo = PSEOAI()
    
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    NICHES = ["AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech"]
    
    products_to_list = []
    rss_items = []
    
    for niche in NICHES:
        print(f"\n--- Safely Orbiting Niche: {niche} ---")
        
        # 1. Select and Validate High-Ticket Product
        product = link_ai.get_next_product()
        
        # ZERO-RISK: Link Validation
        if not safety.validate_link(product['link']):
            print(f"[Safety] Skipping insecure link for {product['name']}")
            continue

        # 2. Viral Hook Generation
        hook = persona.generate_viral_hook(product['name'], niche)
        
        # 3. Assets Generation
        timestamp = int(time.time())
        safe_name = product['name'].replace(" ", "_").lower()[:10]
        
        # Visuals
        img_path = f"assets/{safe_name}_{timestamp}.png"
        persona.generate_pin_image(hook, f"Verified offer in {niche}", img_path)
        
        # Audio
        audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
        vocal.generate_voiceover(hook, audio_path)
        
        # Video
        video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
        motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
        
        # 4. pSEO: Generate Organic Review Page (Search Engine Shield)
        page_path = pseo.generate_review_page(product)
        print(f"[pSEO] Review Page Generated: {page_path}")

        # 5. Preparing for sync
        products_to_list.append(product)
        rss_items.append({
            "title": hook,
            "link": f"{GH_PAGES_BASE}/{page_path}", # Direct traffic to SEO page first
            "description": f"Internal Review: {product['name']}",
            "image_url": f"{GH_PAGES_BASE}/{img_path}"
        })
        
        # ZERO-BAN: Mimetic Jitter
        safety.mimetic_delay(1, 3) # Short delay for demo, use (60, 240) for real actions

    # 6. Global Deployment
    update_storefront(products_to_list)
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("\n--- Zero-Risk Cycle Finished: Safety Protocols Verified ---")

if __name__ == "__main__":
    main()
