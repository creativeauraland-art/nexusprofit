from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI
from core.motion import MotionAI
from core.link import LinkAI
from core.vocal import VocalAI
from core.safety import SafetyAI
from core.pseo import PSEOAI
from core.asset import AssetAI
from core.mail import MailOrbit
import time
import os
import random

def update_storefront(products, assets=None):
    """Injects new products and OWNED ASSETS into index.html."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. High-Ticket Affiliate Products
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
        
        # 2. Owned Assets (Infinity Scaling)
        asset_html = ""
        if assets:
            asset_html = "<div style='grid-column: 1/-1; margin-top: 40px;'><h2>💎 Owned Assets (100% Profit)</h2></div>"
            for a in assets:
                asset_html += f"""
                <div class="card" style="border-color: #f59e0b;">
                    <span style="color: #f59e0b; font-size: 0.8rem; font-weight: bold;">[OWNED ASSET]</span>
                    <h2>{a['name']}</h2>
                    <p>Exclusive guide to {a['niche']}. Instant digital delivery.</p>
                    <a href="#" class="btn" style="background: #f59e0b;">Get Access for $7</a>
                </div>
                """

        start_tag = "<!-- DYNAMIC_PRODUCTS_START -->"
        end_tag = "<!-- DYNAMIC_PRODUCTS_END -->"
        
        if start_tag in content and end_tag in content:
            head = content.split(start_tag)[0]
            tail = content.split(end_tag)[1]
            new_content = f"{head}{start_tag}{product_html}{asset_html}{end_tag}{tail}"
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("[Engine] Storefront updated with products and owned assets.")
    except Exception as e:
        print(f"[Engine] Storefront update failed: {e}")

def main():
    USER_ID = "creative_aura"
    print(f"--- NexusProfit | INFINITY SCALING | USER: {USER_ID} ---")
    
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    motion = MotionAI()
    link_ai = LinkAI(USER_ID)
    vocal = VocalAI()
    safety = SafetyAI()
    pseo = PSEOAI()
    asset_gen = AssetAI()
    mail_orbit = MailOrbit()
    
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    NICHES = ["AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech"]
    
    products_to_list = []
    assets_to_list = []
    rss_items = []
    
    for niche in NICHES:
        print(f"\n--- Infinity Orbit: {niche} ---")
        
        # 1. Product & Asset Sourcing
        product = link_ai.get_next_product()
        
        # ZERO-RISK check
        if not safety.validate_link(product['link']):
            continue

        # 2. Asset Inversion (OWNERSHIP)
        # We generate a PDF guide for every 2nd niche to diversify
        if random.random() > 0.5:
            asset_path = asset_gen.generate_cheat_sheet(niche, product['name'])
            assets_to_list.append({"name": f"{niche} Master Guide", "niche": niche, "path": asset_path})

        # 3. Content Creation
        hook = persona.generate_viral_hook(product['name'], niche)
        timestamp = int(time.time())
        safe_name = product['name'].replace(" ", "_").lower()[:10]
        
        img_path = f"assets/{safe_name}_{timestamp}.png"
        persona.generate_pin_image(hook, f"The {niche} Blueprint", img_path)
        
        audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
        vocal.generate_voiceover(hook, audio_path)
        
        video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
        motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
        
        # 4. pSEO Page
        page_path = pseo.generate_review_page(product)

        # 5. Sync Data
        products_to_list.append(product)
        rss_items.append({
            "title": hook,
            "link": f"{GH_PAGES_BASE}/{page_path}",
            "description": f"Exclusive Insider Info: {niche}",
            "image_url": f"{GH_PAGES_BASE}/{img_path}"
        })
        
        safety.mimetic_delay(1, 2)

    # 6. Weekly Newsletter Compilation (Mail Orbit)
    newsletter_path = mail_orbit.generate_newsletter(products_to_list, int(time.time() / 604800))
    print(f"[MailOrbit] Newsletter Ready: {newsletter_path}")

    # 7. Deployment
    update_storefront(products_to_list, assets_to_list)
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("\n--- Infinity Cycle Finished: You are now a Product Owner ---")

if __name__ == "__main__":
    main()
