import random

class ScoutAI:
    """
    ScoutAI: The intelligence core that maps current Pinterest trends 
    to high-converting Digistore24 products.
    """
    def __init__(self):
        # Current Pinterest Viral Aesthetics (2025-2026 Predictions)
        self.trending_aesthetics = {
            "POETCORE": {
                "desc": "Moody, academic, vintage journaling, fountain pens, coffee stained paper",
                "vibe": "Intellectual & Nostalgic",
                "color_palette": [(40, 30, 20), (180, 160, 140)]
            },
            "VAMP_ROMANTIC": {
                "desc": "Gothic, dark roses, burgundy lace, moody lighting, candles",
                "vibe": "Emotional & Dark",
                "color_palette": [(20, 0, 0), (128, 0, 32)]
            },
            "CHERRY_CODED": {
                "desc": "High-gloss red, cherry motifs, y2k aesthetic, vibrant and juicy",
                "vibe": "Playful & Bold",
                "color_palette": [(255, 0, 0), (255, 255, 255)]
            },
            "EXPEDITION": {
                "desc": "Archaeology, safari, linen textures, maps, survival gear, earth tones",
                "vibe": "Adventurous & Practical",
                "color_palette": [(100, 90, 70), (210, 180, 140)]
            },
            "FUNHAUS": {
                "desc": "Circus maximalism, primary colors, bold patterns, playful home decor",
                "vibe": "Energetic & Eclectic",
                "color_palette": [(255, 0, 0), (255, 255, 0), (0, 0, 255)]
            }
        }

    def get_best_aesthetic_for_product(self, product):
        """
        Logic to align a product with a trending aesthetic based on tags.
        """
        tags = product.get("trend_tags", [])
        
        # Simple mapping logic
        if "gut health" in tags or "sustainable" in tags:
            return "CHERRY_CODED" if random.random() > 0.5 else "EXPEDITION"
        if "poetcore" in tags or "mindfulness" in tags:
            return "POETCORE"
        if "vamp romantic" in tags or "psychology" in tags:
            return "VAMP_ROMANTIC"
        if "digital nomad" in tags or "side hustle" in tags:
            return "FUNHAUS"
            
        return random.choice(list(self.trending_aesthetics.keys()))

    def generate_mashup_idea(self, trend="Spiderman"):
        """
        The 'Spiderman' Method: Mash a viral pop-culture icon with a product.
        """
        return f"How {trend} would solve this: "

if __name__ == "__main__":
    scout = ScoutAI()
    print(f"Recommended Aesthetic: {scout.get_best_aesthetic_for_product({'trend_tags': ['poetcore']})}")
