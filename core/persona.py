import google.generativeai as genai
import os
import requests
import json
import random
import textwrap
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

print("[DIAG] core/persona.py loaded: VERSION 2.3-PROD")

class PersonaAI:
    """
    PersonaAI: Designer-grade engine for high-conversion, elite visuals.
    """
    def __init__(self, brand_name="NexusProfit"):
        self.brand_name = brand_name
        self.palettes = {
            "POETCORE": {"bg": (40, 30, 20), "accent": (180, 160, 140), "text": (255, 255, 255)},
            "VAMP_ROMANTIC": {"bg": (20, 0, 0), "accent": (128, 0, 32), "text": (240, 240, 240)},
            "CHERRY_CODED": {"bg": (255, 0, 0), "accent": (255, 255, 255), "text": (255, 255, 255)},
            "EXPEDITION": {"bg": (100, 90, 70), "accent": (210, 180, 140), "text": (255, 255, 255)},
            "FUNHAUS": {"bg": (255, 255, 255), "accent": (255, 0, 0), "text": (0, 0, 255)}
        }
        # Default palette
        self.default_palette = {"bg": (15, 23, 42), "accent": (56, 189, 248), "glow": (56, 189, 248)}
        
        # Viral Font Support
        self.font_bold = "ariblk.ttf" # Arial Black
        self.font_impact = "impact.ttf" # Impact
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        else:
            self.model = None

    def get_font(self, font_name, size):
        """Safely loads a system font or falls back to default."""
        try:
            return ImageFont.truetype(font_name, size)
        except:
            return ImageFont.load_default()

    def draw_text_professional(self, draw, text, pos, font_name, max_size, max_width, color=(255,255,255), align="center", shadow=True):
        """Standardized professional text drawing with dynamic scaling and high legibility."""
        current_size = max_size
        font = self.get_font(font_name, current_size)
        
        # 1. Dynamic Scaling
        while current_size > 15:
            lines = textwrap.wrap(text, width=int(max_width / (current_size * 0.5)))
            # Check if total height fits (rough estimate)
            total_h = len(lines) * (current_size * 1.2)
            # Check if any line overflows max_width
            max_line_w = 0
            for line in lines:
                l, t, r, b = draw.textbbox((0,0), line, font=font)
                max_line_w = max(max_line_w, r - l)
            
            if max_line_w <= max_width:
                break
            current_size -= 4
            font = self.get_font(font_name, current_size)
        
        # 2. Draw Text with Shadow for Maximum Legibility
        x, y = pos
        lines = textwrap.wrap(text, width=int(max_width / (current_size * 0.5)))
        line_h = current_size * 1.2
        
        for i, line in enumerate(lines):
            line_y = y + (i * line_h)
            if shadow:
                # Draw subtle drop shadow
                draw.text((x+3, line_y+3), line, fill=(0,0,0,180), anchor="mm" if align=="center" else "lm", font=font)
                draw.text((x-1, line_y-1), line, fill=(0,0,0,100), anchor="mm" if align=="center" else "lm", font=font)
            
            draw.text((x, line_y), line, fill=color, anchor="mm" if align=="center" else "lm", font=font)
        
        return y + (len(lines) * line_h)

    def generate_visual_prompt(self, niche, product_name, aesthetic=None, creative_style=None):
        """Generates a hyper-realistic, photography-grade visual prompt with creative styling."""
        camera_specs = "Shot on Sony A7R IV, 35mm f/1.4 lens, 8k resolution, documentary photography style."
        lighting_specs = "Cinematic rim lighting, volumetric fog, soft natural shadows, golden hour glow."
        
        if creative_style == "surreal":
            base_prompt = (
                f"A surreal digital art masterpiece. "
                f"Subject: {product_name} visualized through magical realism. "
                f"Ethereal glows, floating elements, dream-like atmosphere, high-end creative concept."
            )
        else:
            base_prompt = (
                f"{camera_specs} {lighting_specs} "
                f"Subject: A high-end professional visualization of {product_name}. "
                f"Extremely detailed textures, professional color grading, ultra-realistic."
            )
        
        if aesthetic == "POETCORE":
            base_prompt += " Aesthetic: Dark academia, antique books, vintage fountain pen, coffee stains, moody intellectual vibes."
        elif aesthetic == "VAMP_ROMANTIC":
            base_prompt += " Aesthetic: Gothic elegance, dark velvety roses, silver candlesticks, dramatic shadows, mysterious allure."
        elif aesthetic == "CHERRY_CODED":
            base_prompt += " Aesthetic: High-gloss y2k fashion, polished red surfaces, cherry motifs, vibrant pop art studio lighting."
        elif aesthetic == "EXPEDITION":
            base_prompt += " Aesthetic: Rugged safari, leather explorer gear, worn maps, brass compass, warm sunlight through canvas."
        
        if self.model:
            try:
                res = self.model.generate_content(f"Refine this into a hyper-realistic, award-winning Pinterest visual prompt (NO FACES, NO TEXT): {base_prompt}")
                return res.text.strip()
            except:
                return base_prompt
        return base_prompt

    def apply_editorial_filters(self, img):
        """Applies artistic film grain, bloom, and color grading."""
        print(f"[PersonaAI] Applying Editorial Filters...")
        # 1. Subtle Film Grain
        grain = Image.effect_noise(img.size, 15).convert('RGBA')
        img = Image.blend(img, grain, 0.05)
        
        # 2. Cinematic Color Grading (Warm/Cool split)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.05)
        
        # 3. Soft Bloom (Blur overlay)
        bloom = img.filter(ImageFilter.GaussianBlur(radius=8))
        img = Image.blend(img, bloom, 0.15)
        return img

    def blend_double_exposure(self, base, overlay):
        """Artistically blends two images using a luminance-based double exposure style."""
        print(f"[PersonaAI] Creating Double Exposure Mashup...")
        base = base.convert('L').convert('RGBA') # Convert base to moody monochrome
        overlay = overlay.convert('RGBA')
        
        # Create a luma mask from the overlay
        mask = overlay.convert('L').point(lambda x: x if x > 50 else 0)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Composite
        result = Image.composite(overlay, base, mask)
        return result

    def conceptualize_design(self, title, description, niche):
        """Calls Gemini to act as a Senior Art Director & SEO Specialist to create a Pin Design Brief."""
        print(f"[PersonaAI] Senior Art Director conceptualizing design for: {title[:30]}...")
        
        prompt = (
            "Act as a World-Class Pinterest Art Director. Your goal is to design a pin that triggers curiosity and clicks.\n"
            f"Topic: {title}\n"
            f"Context: {description}\n"
            f"Niche: {niche}\n\n"
            "Generate a Design Brief in JSON format. Rules:\n"
            "1. 'audience': Who specifically will click this (be niche).\n"
            "2. 'tone': fun, elegant, bold, minimal, or professional.\n"
            "3. 'headline': A short, punchy, high-contrast headline (max 7-8 words).\n"
            "4. 'graphic_style': modern, minimal, bright, or soft.\n"
            "5. 'image_specs': A descriptive prompt for a high-end visual. Focus on metaphors. "
            "Example: Instead of 'Brain', say 'Ethereal glowing neural network in a cosmic space, 3D render, vibrant gold and deep blue'. "
            "DO NOT include any text in the image specs. Use specific lighting (e.g., 'Volumetric lighting', 'Cyberpunk neon').\n"
            "6. 'palette': 3 Hex codes that pop (Must be vibrant, e.g., #FFD700, #FFFFFF, #00BFFF).\n"
            "7. 'fonts': Font type (e.g., 'Modern Heavy Serif').\n"
            "8. 'seo_description': 300-500 char keyword-rich story for Pinterest SEO.\n"
            "9. 'hashtags': 5 relevant high-volume hashtags.\n"
            "10. 'alt_text': Clear accessibility text.\n\n"
            "Return ONLY raw JSON."
        )
        
        if self.model:
            try:
                res = self.model.generate_content(prompt)
                # Clean JSON string
                json_str = res.text.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0].strip()
                elif "```" in json_str:
                    json_str = json_str.split("```")[1].strip()
                return json.loads(json_str)
            except Exception as e:
                print(f"  ⚠️ Design conceptualization failed: {e}. Falling back to default brief.")

        # Default fallback brief if AI fails
        return {
            "audience": "Enthusiasts",
            "tone": "Professional",
            "headline": title.upper(),
            "graphic_style": "minimal",
            "image_specs": f"High-end photography of {niche} concept, cinematic lighting, 8k resolution.",
            "palette": ["#0F172A", "#FFFFFF", "#38BDF8"],
            "fonts": "Bold Sans-Serif",
            "seo_description": f"Check out this epic guide to {title}. Perfect for beginners and pros alike!",
            "hashtags": ["#Tutorial", "#Success", "#Pinterest"],
            "alt_text": f"A professional visualization of {niche}"
        }

    def generate_studio_pin(self, title, description, output_path, niche):
        """The Masterpiece: Renders a Pin following an AI Art Director's Design Brief."""
        brief = self.conceptualize_design(title, description, niche)
        print(f"[PersonaAI] Art Director suggests '{brief['tone']}' tone with '{brief['graphic_style']}' style.")
        
        # 1. Fetch & Resize the Guided Visual
        visual_prompt = brief['image_specs']
        img = self.fetch_ai_image(visual_prompt, size=(1000, 1500)).convert('RGBA')
        img = img.resize((1000, 1500), Image.Resampling.LANCZOS)
        w, h = img.size
        
        # 2. Extract Art Specs
        palette = brief['palette']
        bg_col = palette[0] if len(palette) > 0 else "#0F172A"
        txt_col = palette[1] if len(palette) > 1 else "#FFFFFF"
        acc_col = palette[2] if len(palette) > 2 else "#38BDF8"
        
        # Helper: Hex to RGB
        def hex_to_rgb(h_str):
            try:
                h_str = h_str.lstrip('#')
                return tuple(int(h_str[i:i+2], 16) for i in (0, 2, 4))
            except:
                return (15, 23, 42)
        
        bg_rgb = hex_to_rgb(bg_col)
        txt_rgb = hex_to_rgb(txt_col)
        acc_rgb = hex_to_rgb(acc_col)

        # 3. Artistic Overlay (Ensuring Background remains visible)
        draw = ImageDraw.Draw(img)
        if brief['tone'].lower() == "minimal":
            # Very subtle gradient at the bottom only
            vignette = Image.new('RGBA', (w, h), (0,0,0,0))
            v_draw = ImageDraw.Draw(vignette)
            for i in range(h//2, h):
                alpha = int(0 + (140 * ((i - h//2) / (h//2))))
                v_draw.line([(0, i), (w, i)], fill=bg_rgb + (alpha,))
            img = Image.alpha_composite(img, vignette)
        else:
            # Modern Float Glass (Smaller, more transparent)
            glass_h = 500
            glass_y = h - glass_h - 150
            glass_x = 80
            glass_w = w - 160
            
            # Subtle blur of background
            glass_block = img.crop((glass_x, glass_y, glass_x + glass_w, glass_y + glass_h))
            glass_block = glass_block.filter(ImageFilter.GaussianBlur(radius=50))
            img.paste(glass_block, (glass_x, glass_y))
            
            # semi-transparent tint
            overlay = Image.new('RGBA', (glass_w, glass_h), bg_rgb + (120,))
            img.paste(overlay, (glass_x, glass_y), overlay)
            # Stylish border
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle([glass_x, glass_y, glass_x + glass_w, glass_y + glass_h], radius=40, outline=txt_rgb + (150,), width=4)

        # 4. High-Contrast Typography
        draw = ImageDraw.Draw(img)
        headline = brief.get('headline', title).upper()
        
        if brief['tone'].lower() == "minimal":
            y = h - 400
            next_y = self.draw_text_professional(draw, headline, (w//2, y), self.font_bold, 80, w - 120, color=txt_rgb)
            self.draw_text_professional(draw, description.upper(), (w//2, next_y + 40), self.font_bold, 32, w - 180, color=acc_rgb)
        else:
            y = h - 600
            next_y = self.draw_text_professional(draw, headline, (w//2, y), self.font_bold, 90, w - 200, color=txt_rgb)
            self.draw_text_professional(draw, description.upper(), (w//2, next_y + 50), self.font_bold, 40, w - 220, color=acc_rgb)

        # 5. Fine Editorial Filters
        img = self.apply_editorial_filters(img)
        
        # 6. Export Asset + SEO Sidecar
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.convert('RGB').save(output_path, quality=95)
        
        seo_path = output_path.replace(".png", "_seo.txt")
        with open(seo_path, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {headline}\n")
            f.write(f"DESCRIPTION: {brief['seo_description']}\n")
            f.write(f"HASHTAGS: {' '.join(brief['hashtags'])}\n")
            f.write(f"ALT TEXT: {brief['alt_text']}\n")
            f.write(f"AUDIENCE: {brief['audience']}\n")
            f.write(f"TONE: {brief['tone']}\n")
            
        print(f"  ✅ Studio-Grade Pin & SEO Sidecar saved: {output_path}")
        return output_path

    def fetch_ai_image(self, prompt, size=(1000, 1500), retries=2):
        """Fetches the highest quality backdrop with retries."""
        import time, random
        entropy = f" [REF_{random.randint(10000, 99999)}]"
        print(f"[PersonaAI] Crafting Masterpiece Backdrop...")
        encoded = requests.utils.quote(prompt + entropy)
        base_url = f"https://image.pollinations.ai/prompt/{encoded}?width={size[0]}&height={size[1]}&nologo=true"
        models = ["turbo", "standard", "flux"]
        
        for attempt in range(retries):
            model = models[attempt % len(models)]
            seed = random.randint(1, 999999)
            # Add parameters to bypass caches and try different pools
            final_url = f"{base_url}&model={model}&seed={seed}&enhance=true"
            print(f"  [AI-FETCH] Attempt {attempt+1} (Model: {model}): {final_url[:80]}...")
            
            try:
                res = requests.get(final_url, timeout=35)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content)).convert('RGB')
                    w_a, h_a = img.size
                    
                    # Extensive 49-point grid sampling for ANY sign of the beige banner
                    beige_hits = 0
                    test_xs = [w_a//x for x in range(2, 11)]
                    test_ys = [h_a//y for y in range(2, 11)]
                    
                    for x in test_xs:
                        for y in test_ys:
                            p = img.getpixel((x, y))
                            # The rate limit banner background is (244, 230, 204)
                            # We detect anything in that light-warm-yellow range
                            if p[0] > 230 and p[1] > 210 and p[2] < 220 and p[0] > p[2] + 10:
                                beige_hits += 1
                                
                    if beige_hits > 2: # Very sensitive: even 3-4 pixels of that beige is a fail
                        print(f"  ⚠️ Confirmed 'Rate Limit' screen detected ({beige_hits} beige hits). Retrying...")
                        continue
                        
                    if img.size[0] > 100:
                        print(f"  ✅ AI Background Successfully Fetched with {model}")
                        return img
                else:
                    print(f"  ⚠️ Pollinations Error {res.status_code}")
                time.sleep(1)
            except Exception as e:
                print(f"  ⚠️ Fetch Exception: {e}")
                time.sleep(1)

        print("  ⚠️ AI Throttled. Fetching High-End Professional Stock Imagery...")
        try:
            # Fallback to high-quality random stock photo based on size
            res = requests.get(f"https://picsum.photos/1000/1500?random={random.randint(1,100)}", timeout=15)
            if res.status_code == 200:
                print("  ✅ Stock Imagery Successfully Fetched (Picsum)")
                return Image.open(BytesIO(res.content))
        except:
            pass

        print("  ⚠️ All Fetch Options Failed. Generating High-End Abstract Masterpiece...")
        canvas = Image.new('RGB', size, (15, 23, 42))
        draw = ImageDraw.Draw(canvas)
        for i in range(size[1]):
            r = int(15 + (40 * (i/size[1])))
            g = int(23 + (60 * (i/size[1])))
            b = int(42 + (80 * (i/size[1])))
            draw.line([(0, i), (size[0], i)], fill=(r, g, b))
        return canvas

    def fetch_external_image(self, url, size=(1000, 1500)):
        """Downloads an image from a URL and prepares it for Pin use."""
        print(f"[PersonaAI] Fetching External Asset: {url}...")
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                img = Image.open(BytesIO(res.content)).convert('RGBA')
                # Resize and center crop to fit the vertical Pin aspect ratio
                w, h = img.size
                target_w, target_h = size
                
                # Calculate scaling to cover the target size
                scale = max(target_w / w, target_h / h)
                new_w, new_h = int(w * scale), int(h * scale)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Center crop
                left = (new_w - target_w) // 2
                top = (new_h - target_h) // 2
                img = img.crop((left, top, left + target_w, top + target_h))
                return img
        except Exception as e:
            print(f"[PersonaAI] Failed to fetch external image: {e}")
        
        return None

    def generate_viral_hook(self, product_name, niche, trend_context=None):
        """Generates a force-stop hook using psychological triggers and trend alignment."""
        if not self.model:
            return f"The {niche} Secret: {product_name}"
        
        context = f" in context of {trend_context}" if trend_context else ""
        prompt = (
            f"Write a 1-sentence viral Pinterest hook for {product_name}{context}. "
            f"Focus on lifestyle transformation and curiosity gaps. NO tech jargon. "
            f"Use phrases like 'How I saved...', 'The secret to...', 'Stop doing...' "
            f"Max 8 words."
        )
        try:
            res = self.model.generate_content(prompt)
            return res.text.strip().replace('"', '')
        except:
            return f"The Hidden {niche} Strategy Revealed"

    def generate_pin_image(self, title, description, output_path, niche="Technology", style="designer", base_image_url=None, aesthetic=None):
        """Unified entry point for multiple high-end visuals."""
        if style == "trend_aligned":
            return self.generate_trend_aligned_pin(title, description, output_path, niche, aesthetic)
        elif style == "viral_mashup":
            return self.generate_viral_mashup_pin(title, description, output_path, niche, base_image_url)
        elif style == "studio":
            return self.generate_studio_pin(title, description, output_path, niche)
        elif style == "visionary":
            return self.generate_visionary_pin(title, description, output_path, niche)
        elif style == "neon_whisper":
            return self.generate_neon_whisper_pin(title, description, output_path, niche)
        elif style == "aspiration":
            dream_subject = random.choice(["luxury sports car", "private villa", "luxury yacht", "tropical beach office"])
            return self.generate_aspiration_pin(title, description, output_path, niche, dream_subject)
        elif style == "money_maker":
            amount = random.choice(["700", "1,200", "2,500", "3,800"])
            platform = random.choice(["ChatGPT", "Canva", "Amazon", "Pinterest"])
            return self.generate_money_pin(amount, platform, niche, output_path, base_image_url)

        # 1. Elite Designer Style (Original Glassmorphism)
        print(f"[PersonaAI] Rendering Elite Designer Style: {title[:20]}...")
        palette = self.palettes.get(aesthetic if aesthetic else niche, self.default_palette)
        
        if base_image_url:
            img = self.fetch_external_image(base_image_url)
            if not img:
                img = self.fetch_ai_image(self.generate_visual_prompt(niche, title, aesthetic)).convert('RGBA')
        else:
            bg_prompt = self.generate_visual_prompt(niche, title, aesthetic)
            img = self.fetch_ai_image(bg_prompt).convert('RGBA')
        w, h = img.size
        
        # Overlay and Depth
        vignette = Image.new('RGBA', (w, h), (0,0,0,0))
        v_draw = ImageDraw.Draw(vignette)
        for i in range(h):
            alpha = int(120 + (80 * (i/h)))
            v_draw.line([(0, i), (w, i)], fill=(15, 23, 42, alpha))
        img = Image.alpha_composite(img, vignette)

        draw = ImageDraw.Draw(img)
        margin = 60
        card_w, card_h = w - (margin * 2), 700
        card_x, card_y = margin, (h // 2) - (card_h // 2)
        
        # Professional Glass Block
        glass_crop = img.crop((card_x, card_y, card_x + card_w, card_y + card_h))
        glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=40))
        img.paste(glass_crop, (card_x, card_y))
        
        overlay = Image.new('RGBA', (card_w, card_h), (255, 255, 255, 25))
        img.paste(overlay, (card_x, card_y), overlay)
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=50, outline=(255, 255, 255, 120), width=4)
        
        # Dynamic Typography with zero collision
        current_y = card_y + 120
        next_y = self.draw_text_professional(draw, title.upper(), (w//2, current_y), self.font_bold, 75, card_w - 60)
        
        current_y = next_y + 40
        next_y = self.draw_text_professional(draw, description.upper(), (w//2, current_y), self.font_bold, 35, card_w - 100, color=palette["accent"])

        # Call to Action Button
        btn_w, btn_h = 480, 100
        btn_x, btn_y = (w // 2) - (btn_w // 2), card_y + card_h - 150
        draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], radius=35, fill=palette["accent"])
        self.draw_text_professional(draw, "GET INSTANT ACCESS ➔", (w//2, btn_y + 50), self.font_bold, 32, btn_w - 40, color=(15, 23, 42), shadow=False)

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

    def generate_viral_lifestyle_pin(self, title, description, output_path, niche="Technology", base_image_url=None):
        """Renders luxury viral asset: Professional Layout, Split Image."""
        print(f"[PersonaAI] Rendering Professional Lifestyle Asset...")
        w, h = 1000, 1500
        canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        
        # 1. Fetch High-Res Images
        if base_image_url:
            top_img = self.fetch_external_image(base_image_url, size=(1000, 650))
            bottom_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "lifestyle office luxury"), size=(1000, 650)).convert('RGBA')
            if not top_img:
                top_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "modern architecture luxury"), size=(1000, 650)).convert('RGBA')
        else:
            top_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "high-end workspace"), size=(1000, 650)).convert('RGBA')
            bottom_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "luxury life freedom"), size=(1000, 650)).convert('RGBA')
            
        canvas.paste(top_img, (0, 0))
        canvas.paste(bottom_img, (0, 850))
        
        # 2. Text Area (White with subtle gradient)
        draw = ImageDraw.Draw(canvas)
        text_y_start = 650
        text_h = 200
        # Apply glass effect to the text area
        glass_crop = canvas.crop((0, text_y_start, w, text_y_start + text_h))
        glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=20))
        canvas.paste(glass_crop, (0, text_y_start))
        overlay = Image.new('RGBA', (w, text_h), (255, 255, 255, 50)) # Semi-transparent white overlay
        canvas.paste(overlay, (0, text_y_start), overlay)

        # 3. Precision Typography
        mid_y = text_y_start + (text_h // 2) - 30
        next_y = self.draw_text_professional(draw, title.upper(), (w//2, mid_y), self.font_bold, 85, w - 80, color=(15, 23, 42), shadow=False)
        self.draw_text_professional(draw, description.upper(), (w//2, next_y + 10), self.font_bold, 45, w - 100, color=(147, 51, 234), shadow=False)

        # 4. Professional Branding
        self.draw_text_professional(draw, f"WWW.{self.brand_name.upper()}.COM", (w//2, h - 60), self.font_bold, 28, w - 100, color=(255, 255, 255))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_money_pin(self, amount, platform, niche, output_path, base_image_url=None):
        """Renders Professional Money-Maker: Impactful Typography & Illustration."""
        print(f"[PersonaAI] Rendering High-Impact Money-Maker...")
        w, h = 1000, 1500
        canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        # 1. Background Content
        if base_image_url:
            illu_img = self.fetch_external_image(base_image_url, size=(1000, 500))
            if not illu_img:
                illu_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "wealth growth illustration"), size=(1000, 500)).convert('RGBA')
        else:
            illu_img = self.fetch_ai_image(self.generate_visual_prompt(niche, "person celebrating financial freedom luxury"), size=(1000, 500)).convert('RGBA')
        canvas.paste(illu_img, (0, 1000))

        # 2. Precision Layout
        y = 120
        y = self.draw_text_professional(draw, "HOW I MAKE", (w//2, y), self.font_bold, 110, w - 100, color=(15, 23, 42))
        
        y += 40
        y = self.draw_text_professional(draw, f"${amount}", (w//2, y), self.font_impact, 360, w - 60, color=(34, 197, 94))
        
        y += 20
        y = self.draw_text_professional(draw, "EVERY SINGLE DAY USING", (w//2, y), self.font_bold, 60, w - 100, color=(15, 23, 42))
        
        y += 40
        y = self.draw_text_professional(draw, platform.upper(), (w//2, y), self.font_impact, 160, w - 80, color=(34, 197, 94))
        
        y += 20
        self.draw_text_professional(draw, "WITH ZERO EXPERIENCE", (w//2, y), self.font_bold, 60, w - 100, color=(15, 23, 42))

        # 3. Branding
        self.draw_text_professional(draw, f"WWW.{self.brand_name.upper()}.COM", (w//2, h - 40), self.font_bold, 28, w - 100, color=(0,0,0,180))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_trend_aligned_pin(self, title, description, output_path, niche, aesthetic):
        """Renders Professional Trend-Aligned Visual: Photography + Sleek Layout."""
        print(f"[PersonaAI] Rendering Pro Trend Visual: {aesthetic}...")
        palette = self.palettes.get(aesthetic, self.default_palette)
        bg_prompt = self.generate_visual_prompt(niche, title, aesthetic)
        img = self.fetch_ai_image(bg_prompt).convert('RGBA')
        w, h = img.size
        
        # 1. Overlay Gradient for Depth
        vignette = Image.new('RGBA', (w, h), (0,0,0,0))
        v_draw = ImageDraw.Draw(vignette)
        for i in range(h):
            alpha = int(20 + (180 * (i/h)))
            v_draw.line([(0, i), (w, i)], fill=(palette["bg"] + (alpha,)))
        img = Image.alpha_composite(img, vignette)

        draw = ImageDraw.Draw(img)
        
        # 2. Dynamic Typography in Safe Zone
        box_h = 450
        current_y = h - box_h + 80
        next_y = self.draw_text_professional(draw, title.upper(), (w//2, current_y), self.font_bold, 80, w - 100)
        
        current_y = next_y + 30
        self.draw_text_professional(draw, description.upper(), (w//2, current_y), self.font_bold, 40, w - 120, color=palette["accent"])
        
        img.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_aspiration_pin(self, title, description, output_path, niche="Technology", dream_subject="luxury sports car"):
        """Renders the 'Aspiration' Pin: Dream outcome at top, working reality at bottom, NO white space."""
        print(f"[PersonaAI] Rendering Aspiration Visual: {dream_subject}...")
        w, h = 1000, 1500
        canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        
        # 1. Fetch High-Res Images
        d_prompt = self.generate_visual_prompt(niche, f"A hyper-realistic {dream_subject} at sunset, luxury cinematic, ultra-detailed.")
        top_img = self.fetch_ai_image(d_prompt, size=(1000, 1100)).convert('RGBA')
        
        r_prompt = self.generate_visual_prompt(niche, "A hardworking person tired at a messy office desk, dim cinematic lighting, professional photography.")
        bottom_img = self.fetch_ai_image(r_prompt, size=(1000, 600)).convert('RGBA')
        
        # 2. Full-Bleed Layout (No white space)
        canvas.paste(top_img, (0, 0))
        # Overlay reality at the bottom with a bit of overlap for a blend feel
        canvas.paste(bottom_img, (0, 900))
        
        draw = ImageDraw.Draw(canvas)
        # 3. Grounded Text Box (Glass Block at the very bottom)
        text_bg_h = 450
        text_bg_y = h - text_bg_h
        
        glass_crop = canvas.crop((0, text_bg_y, w, h))
        glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=30))
        canvas.paste(glass_crop, (0, text_bg_y))
        
        # Semi-transparent dark overlay for high-contrast legibility
        overlay = Image.new('RGBA', (w, text_bg_h), (15, 23, 42, 190))
        canvas.paste(overlay, (0, text_bg_y), overlay)
        
        # 4. Precision Typography (Centered in the glass block)
        current_y = text_bg_y + 100
        next_y = self.draw_text_professional(draw, title.upper(), (w//2, current_y), self.font_bold, 75, w - 80)
        
        current_y = next_y + 40
        self.draw_text_professional(draw, description.upper(), (w//2, current_y), self.font_bold, 35, w - 120, color=(56, 189, 248))
        
        img_final = canvas.convert('RGB')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img_final.save(output_path, quality=95)
        return output_path

    def generate_visionary_pin(self, title, description, output_path, niche="Technology"):
        """Renders the 'Visionary' style: Double Exposure surrealism."""
        print(f"[PersonaAI] Rendering Visionary Surrealism...")
        w, h = 1000, 1500
        
        # 1. Fetch Surreal Elements
        dream_prompt = self.generate_visual_prompt(niche, "A glowing ethereal luxury vision of the future", creative_style="surreal")
        dream_img = self.fetch_ai_image(dream_prompt).convert('RGBA')
        
        reality_prompt = self.generate_visual_prompt(niche, "Cinematic silhouette of a person thinking deeply at night")
        reality_img = self.fetch_ai_image(reality_prompt).convert('RGBA')
        
        # 2. Mashup via Double Exposure
        mashup = self.blend_double_exposure(reality_img, dream_img)
        mashup = self.apply_editorial_filters(mashup)
        
        draw = ImageDraw.Draw(mashup)
        # 3. Artistic Typography (Minimalist & Floating)
        y = h - 600
        y = self.draw_text_professional(draw, title.upper(), (w//2, y), self.font_bold, 80, w - 100, color=(255, 255, 255))
        self.draw_text_professional(draw, description.upper(), (w//2, y + 120), self.font_bold, 35, w - 150, color=(56, 189, 248, 200))
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        mashup.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_neon_whisper_pin(self, title, description, output_path, niche="Technology"):
        """Renders the 'Neon Whisper' style: Mirror/Glass narrative storytelling."""
        print(f"[PersonaAI] Rendering Neon Whisper Narrative...")
        w, h = 1000, 1500
        
        # 1. Fetch Moody Base
        prompt = self.generate_visual_prompt(niche, "Cinematic moody office at night, rain on window, neon city lights reflection", creative_style="surreal")
        img = self.fetch_ai_image(prompt).convert('RGBA')
        img = self.apply_editorial_filters(img)
        
        draw = ImageDraw.Draw(img)
        # 2. Text as 'Reflection' in the mid-section
        y = 500
        text_color = (0, 255, 255, 180) # Neon Cyan
        
        # Draw text with glow
        font = self.get_font(self.font_bold, 90)
        wrapped = textwrap.wrap(title.upper(), width=12)
        for line in wrapped:
            # Glow effect
            for offset in range(5, 0, -1):
                draw.text((w//2, y), line, fill=(0, 255, 255, 30), anchor="mm", font=font, stroke_width=offset)
            draw.text((w//2, y), line, fill=(255, 255, 255, 230), anchor="mm", font=font)
            y += 110
            
        self.draw_text_professional(draw, description.upper(), (w//2, h - 300), self.font_bold, 40, w - 100, color=(255, 255, 255, 150))
        
        img.convert('RGB').save(output_path, quality=95)
        return output_path

    def generate_viral_mashup_pin(self, title, description, output_path, niche, base_image_url=None):
        """The 'Spiderman' Method: Mash pop-culture with product (Modern Style)."""
        print(f"[PersonaAI] Rendering Professional Viral Mashup...")
        trends = ["Spiderman aesthetic", "Cyberpunk workspace", "Vintage Ghibli scenery", "80s Retrowave luxury"]
        trend = random.choice(trends)
        
        prompt = self.generate_visual_prompt(niche, f"Pop culture {trend} style integration")
        img = self.fetch_ai_image(prompt).convert('RGBA')
        w, h = img.size
        draw = ImageDraw.Draw(img)
        
        # 1. Huge Impact Title in Safe Center
        self.draw_text_professional(draw, title.upper(), (w//2, h//2 - 100), self.font_impact, 130, w - 60, color=(255, 255, 0))
        
        # 2. Mashup Label
        self.draw_text_professional(draw, f"PROMPT: {trend.upper()}", (w//2, h - 100), self.font_bold, 30, w - 100, color=(255,255,255,180))
        
        img.convert('RGB').save(output_path, quality=95)
        return output_path

if __name__ == "__main__":
    persona = PersonaAI()
    persona.generate_pin_image("How I Fixed My Gut", "Aesthetic Checklist", "assets/trend_test.png", style="trend_aligned", aesthetic="POETCORE")
