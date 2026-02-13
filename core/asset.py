from google import genai
import os

# VERSION 2.8-PROD: Fully hardened and standard
print("[DIAG] core/asset.py loaded: VERSION 2.8-PROD")

class AssetAI:
    """
    AssetAI: Automatically generates digital products (Guides, Cheat Sheets) for 100% profit.
    """
    def __init__(self):
        # Configure New Gemini SDK
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            self.model_id = "gemini-1.5-flash"
        else:
            self.client = None

    def generate_cheat_sheet(self, niche, product_name):
        """Generates a high-value text-based cheat sheet/guide using the new SDK."""
        print(f"[AssetAI] Designing Digital Product for {niche}...")
        
        if not self.client:
            return f"The Starter Guide to {niche}"
            
        prompt = (
            f"Write a 300-word 'Secret Cheat Sheet' for {niche}. "
            f"Focus on the topic of {product_name}. "
            f"Make it sound extremely valuable and professional. "
            f"Use bullet points and a punchy 'Executive Summary' style. "
            f"Include a 'Pro Tip' section at the end."
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            content = response.text
            
            # Save as a local text asset that can be 'delivered' via a bridge
            os.makedirs("assets/products", exist_ok=True)
            filename = f"assets/products/{niche.lower().replace(' ', '_')}_guide.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- NEXUSPROFIT EXCLUSIVE: {niche.upper()} GUIDE ---\n\n")
                f.write(content)
            
            return filename
        except Exception as e:
            print(f"[AssetAI] Generation failed: {e}")
            return None

if __name__ == "__main__":
    asset_ai = AssetAI()
    asset_ai.generate_cheat_sheet("AI Automation", "Productivity Hacks")
