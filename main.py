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
import core.pinterest
import core.youtube
import core.medium
import core.gumroad

# VERSION 7.0-SALES: Omni-Presence + Tripwire Integration
VERSION = "7.0-SALES"
print(f"[DIAG] main.py loaded: VERSION {VERSION}")

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
    BATCH_LIMIT = random.randint(3, 5) # GHOST: Randomized batch cap
    
    print(f"--- NexusProfit | SALES DOMINATION (v{VERSION}) | USER: {USER_ID} ---")
    print(f"[GHOST] Security Protocol: Capping run to {BATCH_LIMIT} successful orbits.")
    
    # Initialize cores
    scout = core.scout.ScoutAI()
    persona = core.persona.PersonaAI()
    link_ai = core.link.LinkAI(USER_ID)
    pseo = core.pseo.PSEOAI()
    asset_ai = core.asset.AssetAI()
    motion = core.motion.MotionAI()
    vocal = core.vocal.VocalAI()
    safety = core.safety.SafetyAI()
    rss_ai = core.rss.RSSAI()
    pinterest = core.pinterest.PinterestAI()
    youtube = core.youtube.YouTubeAI()
    medium = core.medium.MediumAI()
    gumroad = core.gumroad.GumroadAI(os.getenv("GUMROAD_ACCESS_TOKEN"))
    
    products_to_list = []
    rss_items = []
    successful_orbits = 0
    
    # 🕵️ PLATFORM HEARTBEAT (Check for active channels)
    print("\n" + "📡"*20)
    platforms = {
        "Pinterest": "PINTEREST_API_KEY",
        "YouTube": "YOUTUBE_REFRESH_TOKEN",
        "Medium": "N/A (Import Assistant Active)",
        "Gumroad": "GUMROAD_ACCESS_TOKEN"
    }
    for p, env in platforms.items():
        status = "✅ ACTIVE" if (env == "N/A (Import Assistant Active)" or os.getenv(env)) else "❌ MISSING KEYS (Skipping)"
        print(f"[Heartbeat] {p:10} | {status}")
    print("📡"*20 + "\n")
    
    niches = [
        "AI Automation", "Content Creation", "Crypto Tech", "Biohacking", 
        "Green Tech", "Minimalist Living", "Mindfulness", "Self-Care Rituals",
        "Credit Repair", "DIY Wealth"
    ]
    random.shuffle(niches) # GHOST: Break deterministic patterns
    
    for niche in niches:
        if successful_orbits >= BATCH_LIMIT:
            print(f"[GHOST] Daily cap of {BATCH_LIMIT} reached. Shutting down stealthily.")
            break

        # --- GRACEFUL ORBIT ISOLATION ---
        try:
            print(f"\n--- Multi-Path Orbit: {niche} ---")
            
            product = link_ai.automate_marketplace(niche)
            if not product or not product.get('link'):
                continue
                
            if not safety.validate_link(product['link']):
                print(f"[Engine] Skipping niche {niche} due to unsafe product link.")
                continue
                
            hook = persona.generate_content_hook(product['name'], niche)
            timestamp = int(time.time())
            safe_name = "".join([c if c.isalnum() else "_" for c in product['name'].lower()])[:15]
            
            img_path = f"assets/{safe_name}_{timestamp}.png"
            persona.generate_pin_image(hook, f"Verified in {niche}", img_path, niche=niche)
            
            audio_path = f"assets/audio/{safe_name}_{timestamp}.mp3"
            vocal.generate_voiceover(hook, audio_path)
            
            video_path = f"assets/reels/{safe_name}_{timestamp}.mp4"
            motion.generate_reel(img_path, hook, audio_path=audio_path, output_path=video_path)
            
            # Review & Asset Generation
            page_path = pseo.generate_review_page(product)
            review_markdown = pseo.generate_review_page(product, format="markdown")
            cheat_sheet_path = asset_ai.generate_cheat_sheet(niche, product['name'])
            
            products_to_list.append(product)
            
            # Prepare data for Multi-Platform Blast
            review_url = f"{GH_PAGES_BASE}/{page_path}"
            image_url = f"{GH_PAGES_BASE}/{img_path}"
            
            rss_items.append({
                "title": hook,
                "link": review_url,
                "description": f"Internal Review: {niche}",
                "image_url": image_url
            })
            
            # 1. Pinterest Blast
            pin_success = pinterest.post_pin(
                title=hook,
                description=f"REVEALED: How {product['name']} is disruptive in {niche}.",
                link=review_url,
                image_url=image_url
            )
            
            # 2. YouTube Shorts Blast
            youtube.upload_short(
                video_path=video_path,
                title=f"{hook} #shorts #affiliate",
                description=f"Check out {product['name']}! Review here: {review_url}"
            )

            # 3. Medium Authority Blast
            medium.post_article(
                title=f"The Truth About {product['name']}: An Honest Review",
                content_markdown=review_markdown,
                canonical_url=review_url,
                tags=[niche, "Marketing", "Reviews", "Passive Income", "Success"]
            )
            
            # 4. Gumroad Tripwire Blast (Optional)
            if cheat_sheet_path and os.getenv("GUMROAD_ACCESS_TOKEN"):
                gumroad.create_and_upload_product(
                    name=f"The {niche} Master Guide",
                    description=f"Exclusive blueprint for dominating {niche} with {product['name']}.",
                    price_cents=900,
                    file_path=cheat_sheet_path
                )
            
            if pin_success:
                successful_orbits += 1
                # GHOST: High-Entropy Jitter (random 5-15 mins between successful pins)
                if successful_orbits < BATCH_LIMIT:
                    jitter = random.randint(300, 900) 
                    print(f"[GHOST] Mimetic Jitter: Waiting {jitter}s to mask footprint...")
                    time.sleep(jitter)
            
        except Exception as e:
            # Never crash entire system for one orbit failure
            print(f"[Engine Orbit Failed] {niche}: {e}. Safely proceeding...")
            continue

    # Deployment
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
                os.system(f'git commit -m "Auto-Update: Ghost Stealth Assets (v{VERSION})"')
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
