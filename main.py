import time
from core.scout import ScoutAI
from core.persona import PersonaAI
from core.rss import RSSAI
from core.motion import MotionAI
from core.link import LinkAI

def update_storefront(products):
    """Injects new products into index.html for a dynamic storefront."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    product_html = ""
    for p in products:
        product_html += f"""
        <div class="card">
            <span style="color: #38bdf8; font-size: 0.8rem; font-weight: bold;">[HOT DEAL]</span>
            <h2>{p['name']}</h2>
            <p>High-performance asset in {p['niche']}. Instant access available.</p>
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

def main():
    USER_ID = "creative_aura" # The Golden ID for payouts
    print(f"--- NexusProfit | USER: {USER_ID} | 100% Automated Mode ---")
    
    scout = ScoutAI()
    persona = PersonaAI()
    rss_ai = RSSAI()
    motion = MotionAI()
    link_ai = LinkAI(USER_ID)
    
    GH_PAGES_BASE = "https://creativeauraland-art.github.io/nexusprofit"
    
    # 1. Generate Automated Products & Links
    products_to_list = []
    rss_items = []
    
    # Run 3 cycles for variety
    for _ in range(3):
        product = link_ai.get_next_product()
        trend = product['niche']
        
        # 2. Generate Visuals
        title = f"Top {trend} Hack: {product['name']}"
        desc = f"Get {product['name']} and earn commissions up to {product['commission']}. #automation #passiveincome"
        safe_trend = trend.replace(" ", "_").lower()
        timestamp = int(time.time()) + _
        
        img_path = f"assets/{safe_trend}_{timestamp}.png"
        persona.generate_pin_image(title, desc, img_path)
        
        # 3. Prepare RSS and Storefront
        products_to_list.append(product)
        rss_items.append({
            "title": title,
            "link": f"{GH_PAGES_BASE}/index.html",
            "description": desc,
            "image_url": f"{GH_PAGES_BASE}/{img_path}"
        })
        print(f"Cycle Complete: {product['name']}")

    # 4. Finalize Updates
    update_storefront(products_to_list)
    rss_ai.generate_rss(rss_items, "rss.xml")
    print("--- Engine Shutdown: All Platforms Synced ---")

if __name__ == "__main__":
    main()
