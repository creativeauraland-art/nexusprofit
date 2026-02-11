import google.generativeai as genai
import os
import requests
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

class PersonaAI:
    """
    PersonaAI: Designer-grade engine for high-conversion, elite visuals.
    """
    def __init__(self, brand_name="NexusProfit"):
        self.brand_name = brand_name
        self.palettes = {
            "AI Automation": {"bg": (15, 23, 42), "accent": (56, 189, 248), "glow": (0, 255, 255)},
            "Content Creation": {"bg": (30, 10, 50), "accent": (255, 100, 255), "glow": (255, 0, 255)},
            "Crypto Tech": {"bg": (10, 30, 20), "accent": (50, 255, 150), "glow": (0, 255, 100)},
            "Biohacking": {"bg": (40, 20, 10), "accent": (255, 150, 50), "glow": (255, 100, 0)},
            "Green Tech": {"bg": (10, 40, 20), "accent": (150, 255, 100), "glow": (0, 255, 50)}
        }
        # Default palette
        self.default_palette = {"bg": (15, 23, 42), "accent": (56, 189, 248), "glow": (56, 189, 248)}
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_visual_prompt(self, niche, product_name):
        """Generates a hyper-realistic, content-focused masterpiece prompt."""
        prompt = (
            f"A high-end professional photography shot of {niche} in action. "
            f"Subject: {product_name} concept visualized with realistic lighting, "
            f"depth of field, macro details, 8k resolution, cinematic atmosphere. "
            f"No text, no faces, extremely high quality commercial grade."
        )
        if self.model:
            try:
                res = self.model.generate_content(f"Convert this into a hyper-detailed content-based prompt for a mastery brand: {prompt}")
                return res.text.strip()
            except:
                return prompt
        return prompt

    def fetch_ai_image(self, prompt, size=(1000, 1500)):
        """Fetches the highest quality backdrop from a free AI provider."""
        print(f"[PersonaAI] Crafting Masterpiece Backdrop...")
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={size[0]}&height={size[1]}&nologo=true&seed={random.randint(1,9999)}"
        try:
            res = requests.get(url, timeout=20)
            if res.status_code == 200:
                return Image.open(BytesIO(res.content))
        except:
            return Image.new('RGB', size, (15, 23, 42))
        return Image.new('RGB', size, (15, 23, 42))

    def generate_viral_hook(self, product_name, niche):
        """Generates a force-stop hook using psychological triggers."""
        if not self.model:
            return f"The {niche} Secret: {product_name}"
        prompt = f"Write a psychological 1-sentence viral hook for {product_name} in {niche}. Use 'curiosity gap'. Max 10 words."
        try:
            res = self.model.generate_content(prompt)
            return res.text.strip().replace('"', '')
        except:
            return f"The Hidden {niche} Strategy Revealed"

    def generate_pin_image(self, title, description, output_path, niche="Technology"):
        """Renders an ULTIMATE, technical luxury visual with pinpoint designer accuracy."""
        print(f"[PersonaAI] Crafting Premium Visual: {title[:20]}...")
        palette = self.palettes.get(niche, self.default_palette)
        
        # 1. Base Masterpiece
        bg_prompt = self.generate_visual_prompt(niche, title)
        img = self.fetch_ai_image(bg_prompt).convert('RGBA')
        w, h = img.size
        
        # 2. Deep Gradient Layer
        # Creates a vignette and bottom-up shadow for text pop
        vignette = Image.new('RGBA', (w, h), (0,0,0,0))
        v_draw = ImageDraw.Draw(vignette)
        for i in range(h):
            alpha = int(100 + (100 * (i/h))) # Denser at bottom
            v_draw.line([(0, i), (w, i)], fill=(15, 23, 42, alpha))
        img = Image.alpha_composite(img, vignette)

        # 3. Technical UI Decorations (The "Elite" touch)
        ui_draw = ImageDraw.Draw(img)
        # Corner brackets
        b_len = 50
        b_thick = 4
        # Top Left
        ui_draw.line([(50, 50), (50+b_len, 50)], fill=palette["accent"], width=b_thick)
        ui_draw.line([(50, 50), (50, 50+b_len)], fill=palette["accent"], width=b_thick)
        # Bottom Right
        ui_draw.line([(w-50, h-50), (w-50-b_len, h-50)], fill=palette["accent"], width=b_thick)
        ui_draw.line([(w-50, h-50), (w-50, h-50-b_len)], fill=palette["accent"], width=b_thick)

        # 4. Designer Glass Block (Center)
        draw = ImageDraw.Draw(img)
        margin = 70
        card_w = w - (margin * 2)
        card_h = 680
        card_x = margin
        card_y = (h // 2) - (card_h // 2) - 30
        
        # Layered Glass Glow
        for offset in range(10, 0, -2):
            draw.rounded_rectangle([card_x-offset, card_y-offset, card_x+card_w+offset, card_y+card_h+offset], 
                                    radius=45, outline=palette["accent"] + (30//offset,), width=2)
                                    
        # Blurred Glass Effect
        glass_crop = img.crop((card_x, card_y, card_x + card_w, card_y + card_h))
        glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=35))
        img.paste(glass_crop, (card_x, card_y))
        
        # Inner Glass Depth
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], 
                                radius=40, outline=(255, 255, 255, 90), width=3)
        
        # 5. Elite content Layer
        wrapped_title = textwrap.fill(title.upper(), width=16)
        
        # Title with 3D Pop (Offset Shadow)
        title_x, title_y = w//2, card_y + 180
        # Deep Shadow
        draw.multiline_text((title_x+6, title_y+6), wrapped_title, 
                            fill=(0, 0, 0, 180), anchor="mm", align="center", 
                            font_size=68, spacing=15)
        # Main Title (Bright White)
        draw.multiline_text((title_x, title_y), wrapped_title, 
                            fill=(255, 255, 255), anchor="mm", align="center", 
                            font_size=68, spacing=15)
        
        # Designer Subtitle (High Spacing)
        draw.text((w//2, card_y + 380), f"● {description.upper()} ●", 
                  fill=palette["accent"], anchor="mm", font_size=32)

        # 6. High-Conversion Tactical Button
        btn_w, btn_h = 520, 110
        btn_x = (w // 2) - (btn_w // 2)
        btn_y = card_y + 490
        # Button Glow & Shadow
        draw.rounded_rectangle([btn_x+2, btn_y+2, btn_x+btn_w+10, btn_y+btn_h+10], radius=35, fill=(0,0,0,120))
        # Button Gradient Base
        draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], radius=35, fill=palette["accent"])
        # Professional Button Border
        draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], radius=35, outline=(255,255,255,150), width=3)
        # Button Text (Black for High Contrast)
        draw.text((w//2, btn_y + 55), "SECURE SYSTEM ACCESS ➔", fill=(15, 23, 42), anchor="mm", font_size=34)

        # 7. Footnote
        draw.text((w//2, h-80), f"OFFICIAL {self.brand_name.upper()} CHANNEL", 
                  fill=(255, 255, 255, 100), anchor="mm", font_size=24)

        # Final Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.convert('RGB').save(output_path, quality=95, subsampling=0)
        return output_path

if __name__ == "__main__":
    persona = PersonaAI()
    persona.generate_pin_image("The Silicon Valley Money Secret Revealed", "100% Automated System 2025", "assets/designer_test.png", niche="AI Automation")
