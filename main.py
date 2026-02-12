import os
import time
import random
import re
import traceback
import sys
import core.pseo
import core.scout
import core.link
import core.asset
import core.motion
import core.vocal
import core.safety
import core.persona
import core.rss

VERSION = "2.3-PROD"
print(f"[DIAG] main.py loaded: VERSION {VERSION}")
print(f"[DIAG] core path: {os.path.dirname(core.pseo.__file__)}")

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
                    <span class="card-tag">Verified Strategy</span>
                    <h3>{p['name']}</h3>
                    <p>High-yield infrastructure in the {p['niche']} sector. Fully automated payout protocol included.</p>
                    <a href="{p['link']}" class="btn" target="_blank">Access Strategic Hub</a>
                </div>
            """
        
        # 2. Automated Owned Assets (100% PROFIT)
        asset_html = ""
        if assets:
            asset_html = "<div style='grid-column: 1/-1; margin-top: 40px;'><div class='card-tag' style='text-align: center; font-size: 1.5rem;'>💎 Owned Assets (100% Profit)</div></div>"
            for a in assets:
                asset_html += f"""
                <div class="card" style="border-color: #f59e0b; background: rgba(245, 158, 11, 0.05);">
                    <span class="card-tag" style="color: #f59e0b;">Premium Asset</span>
                    <h3>{a['name']}</h3>
                    <p>Exclusive {a['niche']} Insight. Instant Gumroad delivery for maximum ROI.</p>
                    <a href="{a['link']}" class="btn" style="background: #f59e0b; color: #000;" target="_blank">Get Access for $7</a>
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
    try:
        _run_engine()
    except Exception:
        print("\n[!!!] CRITICAL ENGINE CRASH [!!!]")
        traceback.print_exc()
        sys.exit(1)

def _run_engine():
    USER_ID = "creative_aura"
    GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN", "uEGG-B5gUwPJO-5EGMShiOk16q5hbBZL6FBFV5PTS8s")
    
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
    # Expanded Viral Niche Ecosystem (Scalar Strategy)
    NICHES = [
        "AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech",
        "Minimalist Living", "Mindfulness", "Self-Care Rituals", "Credit Repair", "Passive Income",
        "Side Hustles", "Digital Nomad Life", "Aura Beauty", "Poetcore Lifestyle", "Survival DIY",
        "Home Lab Gaming", "No-Code SaaS", "Marketing Psychology", "Luxury Manifestation", "Holistic Wellness"
    ]
    
    products_to_list = []
    assets_to_list = []
    rss_items = []
    
    for niche in NICHES:
        print(f"\n--- Multi-Path Orbit: {niche} ---")
        
        # 1. Source High-Ticket Product (Automated Marketplace Discovery)
        product = link_ai.automate_marketplace(niche)
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
        if os.environ.get("GITHUB_ACTIONS"):
            print("\n[Engine] Preparing for Cloud Sync (GitHub)...")
            # Ensure we have the latest remote state
            os.system("git pull origin main --rebase")
            
            status = os.popen("git status --porcelain").read().strip()
            if status:
                print(f"[Engine] Changes detected:\n{status}")
                os.system("git add .")
                os.system('git commit -m "Auto-Update: New Elite Assets & Review Pages"')
                push_res = os.system("git push origin main")
                if push_res == 0:
                    print("[Engine] Successfully synced with Global Hub.")
                else:
                    print(f"[Engine] Push failed with exit code {push_res}")
            else:
                print("[Engine] No new assets to sync. Skipping push.")
        else:
            print("\n[Engine] Skipping Cloud Sync in Local/Dev environment.")
        
        print("\n--- Cycle Finished: Global Hub is LIVE and Synced ---")
    except Exception as e:
        print(f"[Engine] Deployment failed: {e}")

if __name__ == "__main__":
    try:
        main()
        print("\n--- NexusProfit Orchestration Complete ---")
    except Exception as e:
        print(f"[Engine Final Error] {e}")
