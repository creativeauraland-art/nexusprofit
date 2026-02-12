import os
import time
from main import main

if __name__ == "__main__":
    print("--- [DIAGNOSTICS] Starting End-to-End System Audit ---")
    
    # 1. Verification of IDs
    USER_ID = "creative_aura"
    print(f"[*] Verifying Affiliate ID: {USER_ID}")
    
    # 2. ROI & Surface Area Audit
    NICHES = [
        "AI Automation", "Content Creation", "Crypto Tech", "Biohacking", "Green Tech",
        "Minimalist Living", "Mindfulness", "Self-Care Rituals", "Credit Repair", "Passive Income",
        "Side Hustles", "Digital Nomad Life", "Aura Beauty", "Poetcore Lifestyle", "Survival DIY",
        "Home Lab Gaming", "No-Code SaaS", "Marketing Psychology", "Luxury Manifestation", "Holistic Wellness"
    ]
    print(f"[*] Surface Area: {len(NICHES)} niches active.")
    # To run only 1 iteration, we'll manually call the core part of main
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
    from main import update_storefront

    print("[*] Running Core System Engine (1 Iteration)...")
    try:
        scout = ScoutAI()
        persona = PersonaAI()
        rss_ai = RSSAI()
        motion = MotionAI()
        link_ai = LinkAI(USER_ID)
        vocal = VocalAI()
        safety = SafetyAI()
        pseo = PSEOAI()
        asset_gen = AssetAI()
        gumroad = GumroadAI("uEGG-B5gUwPJO-5EGMShiOk16q5hbBZL6FBFV5PTS8s")

        niche = "AI Automation"
        product = link_ai.get_next_product()
        print(f"[*] Testing Product: {product['name']} (Link: {product['link']})")
        
        if safety.validate_link(product['link']):
             print("[OK] Link Validation Passed.")
        else:
             print("[!] Link Validation issues detected, but proceeding for tech check.")

        # Test PSEO (Authority Scaling Check)
        page = pseo.generate_review_page(product)
        if os.path.exists(page):
            with open(page, "r", encoding="utf-8") as f:
                html = f.read()
                word_count = len(html.split())
                print(f"[OK] PSEO Page Generated: {page}")
                print(f"[ROI] Page length: {word_count} words (Target: >500 for Authority)")
                if "ai-authority-section" in html:
                    print("[OK] AI Authority Section detected (High Conversion Active).")
                else:
                    print("[!] Warning: Authority Page using fallback template.")
        
        # Test Storefront
        update_storefront([product])
        print("[OK] Storefront Updated.")

    except Exception as e:
        print(f"[!] System Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- [DIAGNOSTICS] Audit Complete ---")
