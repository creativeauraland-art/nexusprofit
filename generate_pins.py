from core.link import LinkAI
from core.persona import PersonaAI
from core.scout import ScoutAI
import random
import os

def generate_product_pins():
    """
    Orchestrator to generate Pinterest Pins for all Digistore24 products.
    """
    print("🚀 Starting Batch Pinterest Pin Generation...")
    
    # Initialize Core Engines
    link_ai = LinkAI(user_id="creative_aura")
    persona = PersonaAI(brand_name="NexusProfit")
    scout = ScoutAI()
    
    products = link_ai.products
    output_dir = "assets/pins"
    os.makedirs(output_dir, exist_ok=True)
    
    for product in products:
        print(f"\n📦 Processing: {product['name']}")
        
        # 1. Select Best Aesthetic using ScoutAI
        aesthetic = scout.get_best_aesthetic_for_product(product)
        print(f"  🔍 ScoutAI Recommendation: {aesthetic}")
        
        # 2. Generate Pins for Studio-Grade Excellence
        styles = ["studio", "trend_aligned"]
        
        for style in styles:
            pin_filename = f"{product['id']}_{style}.png"
            output_path = os.path.join(output_dir, pin_filename)
            
            # Use real product image if available
            image_url = product.get("image_url")
            
            # Generate Hook with Trend Context
            hook = persona.generate_viral_hook(product['name'], product['niche'], trend_context=aesthetic)
            sub_text = product.get("conversion_hook", f"Verified in {product['niche']}")
            
            print(f"  🎨 Rendering Style: {style}...")
            try:
                persona.generate_pin_image(
                    title=hook,
                    description=sub_text,
                    output_path=output_path,
                    niche=product['niche'],
                    style=style,
                    base_image_url=image_url,
                    aesthetic=aesthetic
                )
                print(f"  ✅ Saved: {output_path}")
            except Exception as e:
                print(f"  ❌ Failed to generate {style} for {product['name']}: {e}")

    print("\n🏁 Pin Generation Complete. Check assets/pins/ directory.")

if __name__ == "__main__":
    generate_product_pins()
