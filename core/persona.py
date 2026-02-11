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
        
        # Viral Font Support
        self.font_bold = "ariblk.ttf" # Arial Black
        self.font_impact = "impact.ttf" # Impact
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def get_font(self, font_name, size):
        """Safely loads a system font or falls back to default."""
        try:
            return ImageFont.truetype(font_name, size)
        except:
            return ImageFont.load_default(size)

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

    def fetch_ai_image(self, prompt, size=(1000, 1500), retries=2):
        """Fetches the highest quality backdrop with retries."""
        import time
        print(f"[PersonaAI] Crafting Masterpiece Backdrop...")
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={size[0]}&height={size[1]}&nologo=true&seed={random.randint(1,99999)}"
        
        for attempt in range(retries):
            try:
                res = requests.get(url, timeout=25)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content))
                    if img.size[0] > 100: # Verify it's not a tiny error image
                        return img
                time.sleep(2)
            except:
                time.sleep(2)

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

    def generate_pin_image(self, title, description, output_path, niche="Technology", style="designer"):
        """Unified entry point for multiple high-end visuals."""
        if style == "viral_lifestyle":
            return self.generate_viral_lifestyle_pin(title, description, output_path, niche)
        elif style == "money_maker":
            amount = random.choice(["700", "1,200", "2,500", "3,800"])
            platform = random.choice(["ChatGPT", "Canva", "Amazon", "Pinterest"])
            return self.generate_money_pin(amount, platform, niche, output_path)

        # 1. Elite Designer Style (Original Glassmorphism)
        print(f"[PersonaAI] Rendering Elite Designer Style: {title[:20]}...")
        palette = self.palettes.get(niche, self.default_palette)
        bg_prompt = self.generate_visual_prompt(niche, title)
        img = self.fetch_ai_image(bg_prompt).convert('RGBA')
        w, h = img.size
        
        # Overlay and Depth
        vignette = Image.new('RGBA', (w, h), (0,0,0,0))
        v_draw = ImageDraw.Draw(vignette)
        for i in range(h):
            alpha = int(100 + (100 * (i/h)))
            v_draw.line([(0, i), (w, i)], fill=(15, 23, 42, alpha))
        img = Image.alpha_composite(img, vignette)

        draw = ImageDraw.Draw(img)
        margin = 70
        card_w, card_h = w - (margin * 2), 680
        card_x, card_y = margin, (h // 2) - (card_h // 2) - 30
        
        glass_crop = img.crop((card_x, card_y, card_x + card_w, card_y + card_h))
        glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=35))
        img.paste(glass_crop, (card_x, card_y))
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=40, outline=(255, 255, 255, 90), width=3)
        
        title_font = self.get_font(self.font_bold, 68)
        wrapped_title = textwrap.fill(title.upper(), width=16)
        draw.multiline_text((w//2, card_y + 180), wrapped_title, fill=(255,255,255), anchor="mm", align="center", font=title_font, spacing=15)
        
        sub_font = self.get_font(self.font_bold, 32)
        draw.text((w//2, card_y + 380), description.upper(), fill=palette["accent"], anchor="mm", font=sub_font)

        btn_w, btn_h = 520, 110
        btn_x, btn_y = (w // 2) - (btn_w // 2), card_y + 490
        draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], radius=35, fill=palette["accent"])
        btn_font = self.get_font(self.font_bold, 34)
        draw.text((w//2, btn_y + 55), "SECURE ACCESS ➔", fill=(15, 23, 42), anchor="mm", font=btn_font)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_viral_lifestyle_pin(self, title, description, output_path, niche="Technology"):
        """Split-screen lifestyle style."""
        print(f"[PersonaAI] Rendering Lifestyle Split...")
        bg1 = self.fetch_ai_image(self.generate_lifestyle_prompt(niche, "modern tech scene"), size=(1000, 650))
        bg2 = self.fetch_ai_image(self.generate_lifestyle_prompt(niche, "happy person at desk"), size=(1000, 650))
        
        canvas = Image.new('RGB', (1000, 1500), (255,255,255))
        canvas.paste(bg1, (0, 0))
        canvas.paste(bg2, (0, 850))
        
        draw = ImageDraw.Draw(canvas)
        title_font = self.get_font(self.font_bold, 85)
        lines = textwrap.wrap(title.upper(), width=15)
        curr_y = 650
        for line in lines:
            draw.text((500, curr_y), line, fill=(0,0,0), anchor="mm", font=title_font)
            curr_y += 100
            
        sub_font = self.get_font(self.font_bold, 45)
        draw.text((500, 800), description.upper(), fill=(147, 51, 234), anchor="mm", font=sub_font)
        
        canvas.save(output_path, quality=95)
        return output_path

    def generate_money_pin(self, amount, platform, niche, output_path):
        """High-impact money maker style."""
        print(f"[PersonaAI] Rendering Money-Maker...")
        canvas = Image.new('RGB', (1000, 1500), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        f1 = self.get_font(self.font_bold, 110)
        f2 = self.get_font(self.font_impact, 380)
        f3 = self.get_font(self.font_bold, 65)
        f4 = self.get_font(self.font_impact, 160)
        
        draw.text((500, 150), "HOW I MAKE", fill=(0,0,0), anchor="mm", font=f1)
        draw.text((500, 420), f"${amount}", fill=(34,197,94), anchor="mm", font=f2, stroke_width=12, stroke_fill=(0,0,0))
        draw.text((500, 660), "Every single day using", fill=(0,0,0), anchor="mm", font=f3)
        draw.text((500, 840), platform.upper(), fill=(34,197,94), anchor="mm", font=f4, stroke_width=8, stroke_fill=(0,0,0))
        draw.text((500, 1000), "with NO experience", fill=(0,0,0), anchor="mm", font=f3)
        
        bg = self.fetch_ai_image(self.generate_lifestyle_prompt(niche, "person on laptop flat illustration"), size=(1000, 450))
        canvas.paste(bg, (0, 1050))
        canvas.save(output_path, quality=95)
        return output_path

    def generate_lifestyle_prompt(self, niche, detail):
        """Generates a prompt for realistic lifestyle/earning imagery."""
        prompt = (
            f"A high-quality photo related to {niche}. "
            f"Subject: {detail}, professional, cinematic, high-end."
        )
        if self.model:
            try:
                res = self.model.generate_content(f"Convert into a photography prompt: {prompt}")
                return res.text.strip()
            except:
                return prompt
        return prompt

    def generate_viral_lifestyle_pin(self, title, description, output_path, niche="Technology"):
        """Renders the EXACT style of the user's reference: Top Image, Middle Text, Bottom Image."""
        print(f"[PersonaAI] Rendering Viral Lifestyle Asset: {title[:20]}...")
        
        # 1. Fetch 2 Different Images
        img1_prompt = self.generate_lifestyle_prompt(niche, "person at desk")
        img2_prompt = self.generate_lifestyle_prompt(niche, "AI robot or futuristic tech")
        
        top_img = self.fetch_ai_image(img1_prompt, size=(1000, 600)).convert('RGBA')
        bottom_img = self.fetch_ai_image(img2_prompt, size=(1000, 600)).convert('RGBA')
        
        # 2. Base Canvas (White Background)
        w, h = 1000, 1500
        canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        
        # 3. Paste Images
        canvas.paste(top_img, (0, 0))
        canvas.paste(bottom_img, (0, h - 600))
        
        # 4. Middle Text Block
        draw = ImageDraw.Draw(canvas)
        text_bg_y = 600
        text_bg_h = 300
        # draw.rectangle([0, text_bg_y, w, text_bg_y + text_bg_h], fill=(255, 255, 255))
        
        # 5. Bold Typography (The "MarketingArtfully" Style)
        # Title (Top part of middle)
        title_lines = textwrap.wrap(title.upper(), width=15)
        current_y = text_bg_y + 40
        for line in title_lines:
            draw.text((w//2, current_y), line, fill=(15, 23, 42), anchor="mm", font_size=85) # Bold Black
            current_y += 100
            
        # Description (Bottom part of middle)
        draw.text((w//2, current_y + 20), description.upper(), fill=(147, 51, 234), anchor="mm", font_size=55) # Purple Accent
        
        # 6. Branding Footer (Over bottom image)
        draw.text((w//2, h - 50), f"WWW.{self.brand_name.upper()}.COM", fill=(255, 255, 255), anchor="mm", font_size=25)

        # Final Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_money_pin(self, amount, platform, niche, output_path):
        """Renders the EXACT 'How I Make $700' style Pin."""
        print(f"[PersonaAI] Rendering Money-Maker Visual...")
        
        w, h = 1000, 1500
        canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        # 1. Huge Bold Text at Top
        draw.text((w//2, 100), "HOW I MAKE", fill=(0, 0, 0), anchor="mm", font_size=120)
        # The Money Amount (Large Green)
        draw.text((w//2, 350), f"${amount}", fill=(34, 197, 94), anchor="mm", font_size=350, stroke_width=8, stroke_fill=(0, 0, 0))
        # Frequency
        draw.text((w//2, 580), "Every single day using", fill=(0, 0, 0), anchor="mm", font_size=70)
        # Platform (Highlighted)
        draw.text((w//2, 750), platform.upper(), fill=(34, 197, 94), anchor="mm", font_size=150, stroke_width=5, stroke_fill=(0, 0, 0))
        # Benefit
        draw.text((w//2, 920), "with NO experience", fill=(0, 0, 0), anchor="mm", font_size=70)
        
        # 2. Illustration at Bottom
        illu_prompt = self.generate_lifestyle_prompt(niche, "person lying on floor with laptop and dog, flat illustration style")
        illu_img = self.fetch_ai_image(illu_prompt, size=(1000, 500)).convert('RGBA')
        canvas.paste(illu_img, (0, 1000))
        
        # 3. Footer
        draw.text((w//2, h - 50), f"WWW.{self.brand_name.upper()}.COM", fill=(0, 0, 0), anchor="mm", font_size=30)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.convert('RGB').save(output_path, quality=95)
        return output_path

if __name__ == "__main__":
    persona = PersonaAI()
    persona.generate_pin_image("The AI Profiting Secret", "Automate in 24h", "assets/style_test_1.png", style="designer")
    persona.generate_pin_image("TURN AI INTO INCOME", "FIND YOUR NICHE", "assets/style_test_2.png", style="viral_lifestyle")
    persona.generate_pin_image("FREE MONEY HACK", "USING CHATGPT", "assets/style_test_3.png", style="money_maker")
