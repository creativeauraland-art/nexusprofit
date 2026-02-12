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

VERSION = "2.5-PROD"
print(f"[DIAG] main.py loaded: VERSION {VERSION}")
print(f"[DIAG] core path: {os.path.dirname(core.pseo.__file__)}")

def update_storefront(products):
    """Injects new products into index.html."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        product_html = ""
        for p in products:
            product_html += f"""
                <div class="card">
                    <span class="card-tag">Verified Strategy</span>
                    <h3>{p['name']}</h3>
                    <p>Commission: {p.get('commission', '$50+')}</p>
                    <a href="{p['link']}" class="btn" target="_blank">Activate Offer ➔</a>
                </div>
            """
        
        if "<!-- PRODUCT_GRID -->" in content:
            content = content.replace("<!-- PRODUCT_GRID -->", product_html)
            
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Engine] Storefront updated with {len(products)} products.")
    except Exception as e:
        print(f"[Engine] Storefront update failed: {e}")

def _run_engine():
    USER_ID = "creative_aura"
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    
    print(f"--- NexusProfit | PROD SCALE (v{VERSION}) | USER: {USER_ID} ---")
    
    scout = core.scout.ScoutAI()
    persona = core.persona.PersonaAI()
    link_ai = core.link.LinkAI(USER_ID)
    pseo = core.pseo.PSEOAI()
    asset_ai = core.asset.AssetAI()
    motion = core.motion.MotionAI()
    vocal = core.vocal.VocalAI()
    safety = core.safety.SafetyAI()
    rss_ai = core.rss.RSSAI()
    
    products_to_list = []
    rss_items = []
    
    niches = [
        "AI Automation", "Content Creation", "Crypto Tech", "Biohacking", 
        "Green Tech", "Minimalist Living", "Mindfulness", "Self-Care Rituals",
        "Credit Repair", "DIY Wealth", "Affiliate Marketing", "Side Hustle",
        "Digital Nomad", "E-commerce", "SaaS", "Coding Hacks",
        "Graphic Design", "Video Editing", "Social Media Mastery", "Public Speaking"
    ]
    
    for niche in niches:
        # --- NICHE ISOLATION (Graceful Failure) ---
        try:
            print(f"\n--- Multi-Path Orbit: {niche} ---")
            
            product = link_ai.automate_marketplace(niche)
            
            if not safety.validate_link(product['link']):
                print(f"[Engine] Skipping niche {niche} due to unsafe product link.")
                continue
                
            hook = f"The Hidden {niche} Strategy That Multiplies Your Growth"
            timestamp = int(time.time())
            safe_name = product['name'].replace(" ", "_").lower()[:10]
            
            img_path = f"assets/{safe_name}_{timestamp}.png"
            persona.generate_pin_image(hook, f"Verified in {niche}", img_path, niche=niche)
            
            audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
            vocal.generate_voiceover(hook, audio_path)
            
            video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
            motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
            
            page_path = pseo.generate_review_page(product)
            products_to_list.append(product)
            rss_items.append({
                "title": hook,
                "link": f"{GH_PAGES_BASE}/{page_path}",
                "description": f"Internal Review: {niche}",
                "image_url": f"{GH_PAGES_BASE}/{img_path}"
            })
            
            safety.mimetic_delay(1, 2)
        except Exception as niche_err:
            print(f"[Engine] Orbit failed for {niche}: {niche_err}. Safely proceeding to next orbit.")
            continue

    # 6. Deployment & Revenue Sync
    try:
        if products_to_list:
            update_storefront(products_to_list)
        if rss_items:
            rss_ai.generate_rss(rss_items, "rss.xml")
        
        if os.environ.get("GITHUB_ACTIONS"):
            print("\n[Engine] Preparing for Cloud Sync (GitHub)...")
            os.system("git pull origin main --rebase")
            
            status = os.popen("git status --porcelain").read().strip()
            if status:
                os.system("git add .")
                os.system('git commit -m "Auto-Update: Hardened Elite Assets & Review Pages"')
                os.system("git push origin main")
                print("[Engine] Successfully synced with Global Hub.")
            else:
                print("[Engine] No new assets to sync.")
    except Exception as e:
        print(f"[Engine] Deployment failed: {e}")

def main():
    try:
        _run_engine()
    except Exception:
        print("\n[!!!] CRITICAL ENGINE CRASH [!!!]")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
