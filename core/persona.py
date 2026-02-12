from google import genai
import os
import requests
import json
import random
import textwrap
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

# VERSION 2.8-PROD: Fully hardened and standard
print("[DIAG] core/persona.py loaded: VERSION 2.8-PROD")

class PersonaAI:
    """
    PersonaAI: Designer-grade engine for high-conversion, elite visuals using the new Gemini SDK.
    """
    def __init__(self):
        # Configure New Gemini SDK
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_id = "gemini-1.5-flash"
        else:
            self.client = None

    def _generate_ai_prompt(self, hook, style="designer"):
        """Generates a visual description using the new SDK."""
        if not self.client:
            return f"A high-end {style} visual representing {hook}"
            
        prompt = (
            f"Generate a detailed visual prompt for a Pinterest pin. "
            f"Hook: '{hook}'. Style: '{style}'. "
            f"Focus on lighting, textures, and elite aesthetic. No text in the image."
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except:
            return f"Elite {style} backdrop for {hook}"

    def generate_pin_image(self, title, subtitle, output_path, niche="Wealth", style="designer"):
        """Creates a studio-grade visual asset."""
        print(f"[PersonaAI] Rendering {style.title()} Visual: {title[:20]}...")
        
        # 1. Base Canvas (Dark Luxury)
        width, height = 1000, 1500
        canvas = Image.new('RGB', (width, height), (15, 23, 42))
        draw = ImageDraw.Draw(canvas)
        
        # 2. Abstract Backdrop (Simplified for stability)
        for i in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(50, 300)
            draw.ellipse([x-r, y-r, x+r, y+r], outline=(30, 41, 59), width=2)

        # 3. Text Overlay
        try:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
            draw.text((50, 400), textwrap.fill(title, width=15), font=font_main, fill=(56, 189, 248))
            draw.text((50, 1100), subtitle, font=font_sub, fill=(148, 163, 184))
        except:
            pass

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.save(output_path)
        return output_path

    def generate_content_hook(self, product_name, niche):
        """Generates a viral hook using the new Gemini SDK."""
        if not self.client:
            return f"The Hidden {niche} Strategy That Multiplies Your Growth"
            
        prompt = f"Write a 7-word viral hook for a product called '{product_name}' in the {niche} niche. Make it sound mysterious and elite."
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.replace('"', '').strip()
        except:
            return f"The Hidden {niche} Strategy That Multiplies Your Growth"
