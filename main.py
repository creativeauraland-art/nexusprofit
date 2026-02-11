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
from core.gumroad import GumroadAI
import time
import os
import random

def update_storefront(products, assets=None):
    """Injects new products and AUTOMATED GUMROAD ASSETS into index.html."""
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
        
        # 2. Automated Owned Assets (100% PROFIT)
        asset_html = ""
        if assets:
            asset_html = "<div style='grid-column: 1/-1; margin-top: 40px;'><h2>💎 Owned Assets (100% Profit)</h2></div>"
            for a in assets:
                asset_html += f"""
                <div class="card" style="border-color: #f59e0b;">
                    <span style="color: #f59e0b; font-size: 0.8rem; font-weight: bold;">[AUTOMATED ASSET]</span>
                    <h2>{a['name']}</h2>
                    <p>Exclusive {a['niche']} Insight. Instant Gumroad delivery.</p>
                    <a href="{a['link']}" class="btn" style="background: #f59e0b;" target="_blank">Get Access for $7</a>
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
            print("[Engine] Storefront updated with live Gumroad assets.")
    except Exception as e:
        print(f"[Engine] Storefront update failed: {e}")

def main():
    USER_ID = "creative_aura"
    GUMROAD_TOKEN = "uEGG-B5gUwPJO-5EGMShiOk16q5hbBZL6FBFV5PTS8s"
    
    print(f"--- NexusProfit | GUMROAD MASTERY | USER: {USER_ID} ---")
    
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
    gumroad = GumroadAI(GUMROAD_TOKEN)
    
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    NICHES = ["AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech"]
    
    products_to_list = []
    assets_to_list = []
    rss_items = []
    
    for niche in NICHES:
        print(f"\n--- Multi-Path Orbit: {niche} ---")
        
        # 1. Source High-Ticket Product
        product = link_ai.get_next_product()
        if not safety.validate_link(product['link']):
            continue

        # 2. Automated Asset Factory (Owner Mode)
        # Every run, create a niche specific guide and push to Gumroad
        asset_file = asset_gen.generate_cheat_sheet(niche, product['name'])
        if asset_file:
            gumroad_link = gumroad.create_and_upload_product(
                name=f"{niche} Profit Blueprint 2025",
                description=f"Automated high-value guide for mastering {niche}.",
                price_cents=700,
                file_path=asset_file
            )
            if gumroad_link:
                assets_to_list.append({"name": f"{niche} Elite Guide", "niche": niche, "link": gumroad_link})

        # 3. Viral Content Loop
        hook = persona.generate_viral_hook(product['name'], niche)
        timestamp = int(time.time())
        safe_name = product['name'].replace(" ", "_").lower()[:10]
        
        img_path = f"assets/{safe_name}_{timestamp}.png"
        style = random.choice(["designer", "viral_lifestyle", "money_maker"])
        persona.generate_pin_image(hook, f"Verified in {niche}", img_path, niche=niche, style=style)
        
        audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
        vocal.generate_voiceover(hook, audio_path)
        
        video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
        motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
        
        # 4. Global Hub Sync
        page_path = pseo.generate_review_page(product)
        products_to_list.append(product)
        rss_items.append({
            "title": hook,
            "link": f"{GH_PAGES_BASE}/{page_path}",
            "description": f"Internal Review: {niche}",
            "image_url": f"{GH_PAGES_BASE}/{img_path}"
        })
        
        safety.mimetic_delay(1, 2)

    # 5. Deployment & Revenue Sync
    try:
        update_storefront(products_to_list, assets_to_list)
        rss_ai.generate_rss(rss_items, "rss.xml")
        
        # 6. AUTOMATED LIVE PUSH (Fixes 404 Errors)
        print("\n[Engine] Syncing with Cloud (GitHub)...")
        os.system("git add .")
        os.system('git commit -m "Auto-Update: New Elite Assets & Review Pages"')
        os.system("git push origin main")
        
        print("\n--- Cycle Finished: Global Hub is LIVE and Synced ---")
    except Exception as e:
        print(f"[Engine] Deployment failed: {e}")

if __name__ == "__main__":
    while True:
        try:
            main()
            print("\n[Sleeping] Next cycle in 6 hours...")
            time.sleep(60 * 60 * 6) # 6 Hour Loop
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Engine Error] {e}")
            time.sleep(60)
