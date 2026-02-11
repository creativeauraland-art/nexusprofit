import os
from PIL import Image, ImageDraw, ImageFont

class PersonaAI:
    """
    PersonaAI: Responsible for creating a consistent brand aesthetic and visual assets.
    """
    def __init__(self, brand_name="NexusProfit"):
        self.brand_name = brand_name
        self.colors = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#38bdf8"}

    def generate_pin_image(self, title, description, output_path):
        print(f"[PersonaAI] Generating Pin for: {title}...")
        # Simple aesthetic image generation using Pillow
        img = Image.new('RGB', (1000, 1500), color=self.colors["bg"])
        draw = ImageDraw.Draw(img)
        
        # In a real scenario, we'd use nice fonts and layouts
        draw.text((50, 50), self.brand_name, fill=self.colors["accent"])
        draw.text((50, 200), title, fill=self.colors["text"])
        draw.text((50, 400), description, fill=self.colors["text"])
        
        img.save(output_path)
        return output_path

if __name__ == "__main__":
    persona = PersonaAI()
    persona.generate_pin_image("The Future of AI", "Automate your life in 2025.", "assets/sample_pin.png")
