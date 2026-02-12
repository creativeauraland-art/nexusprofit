import os
import random
from google import genai

print("[DIAG] core/pseo.py loaded: VERSION 2.5-PROD")

class PSEOAI:
    """
    PSEOAI: Generates programmatic SEO pages for every product to capture Google Search traffic.
    """
    def __init__(self, output_dir="reviews"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Configure New Gemini SDK
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_id = "gemini-1.5-flash"
        else:
            self.client = None

    def _generate_ai_copy(self, product):
        """Generates high-conversion sales copy using the new Gemini SDK."""
        if not self.client:
            return None
            
        prompt = (
            f"Write a deep, authoritative product review for '{product['name']}' in the {product['niche']} niche. "
            "Format: Use AIDA model (Attention, Interest, Desire, Action). "
            "Tone: Expert, enthusiastic, yet critical and honest. "
            "Include: \n"
            "1. An 'Executive Summary' section.\n"
            "2. 'The Real Truth' section about its effectiveness.\n"
            "3. A 'Comparison Table' simulation (plain text summary).\n"
            "4. An 'FAQ' section with 3 common questions.\n"
            "Minimum 800 words. Output in HTML-compatible prose (use <p>, <h3>, <li> tags)."
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"[PSEOAI] AI Generation failed: {e}")
            return None

    def generate_review_page(self, product):
        """Creates a high-conversion sales/review page for a product."""
        safe_filename = product['name'].replace(" ", "-").lower().replace("(", "").replace(")", "")
        file_path = f"{self.output_dir}/{safe_filename}.html"
        
        # Sales Psychology Variables
        urgency_msg = random.choice([
            "Only 7 copies left at this introductory price!",
            "Offer expires in 14:52... (Closing Soon)",
            "Bonus guides included for the first 50 buyers only."
        ])
        
        # AI Authority Copy Generation
        ai_copy = self._generate_ai_copy(product)
        if not ai_copy:
            content_body = f"""
            <p style="font-size: 1.2rem;">If you are serious about <strong>{product['niche']}</strong>, you've likely seen the noise. Most tools promise the world but deliver nothing. We've put {product['name']} to the test.</p>
            <div class="testimonial">
                "I was skeptical at first, but after 7 days of using the {product['niche']} strategies inside {product['name']}, I've already seen a massive shift in my automation flow. This is the real deal."
            </div>
            <h2>Why This Is a Game-Changer:</h2>
            <ul class="benefit-list">
                <li><strong>Proven Revenue Model</strong>: Built specifically for the {product['niche']} elite.</li>
                <li><strong>Zero Fluff Implementation</strong>: Go from setup to live in under 48 hours.</li>
                <li><strong>High-Ticket Returns</strong>: Optimized for maximum conversion in the current 2025 market.</li>
                <li><strong>Step-by-Step Blueprint</strong>: No technical experience required.</li>
            </ul>
            """
        else:
            content_body = f"""<div class="ai-authority-section">{ai_copy}</div>"""

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REVEALED: {product['name']} - Is This Your ${random.randint(5,15)}k/mo Answer?</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --accent: #38bdf8; --bg: #0f172a; --card: #1e293b; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: #f8fafc; line-height: 1.6; margin: 0; padding: 20px; }}
        .header {{ text-align: center; padding: 60px 20px; border-bottom: 2px dashed rgba(255,255,255,0.1); }}
        .badge {{ background: var(--accent); color: var(--bg); padding: 5px 15px; border-radius: 20px; font-weight: 900; font-size: 0.8rem; text-transform: uppercase; }}
        h1 {{ font-size: 2.8rem; font-weight: 900; letter-spacing: -2px; margin-top: 15px; }}
        .container {{ max-width: 900px; margin: -40px auto 40px; background: var(--card); padding: 50px; border-radius: 24px; border: 1px solid rgba(56, 189, 248, 0.3); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}
        .highlight {{ color: var(--accent); }}
        .urgency-bar {{ background: #ef4444; color: white; padding: 12px; text-align: center; font-weight: bold; border-radius: 12px; margin-bottom: 30px; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} 100% {{ opacity: 1; }} }}
        .benefit-list {{ list-style: none; padding: 0; margin: 30px 0; }}
        .benefit-list li {{ padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: flex-start; }}
        .benefit-list li::before {{ content: "✅"; margin-right: 15px; }}
        .cta-box {{ text-align: center; background: rgba(56, 189, 248, 0.1); padding: 40px; border-radius: 20px; margin-top: 40px; }}
        .btn {{ display: inline-block; background: var(--accent); color: var(--bg); padding: 22px 45px; border-radius: 12px; text-decoration: none; font-size: 1.4rem; font-weight: 900; transition: transform 0.2s; box-shadow: 0 10px 15px -3px rgba(56,189,248,0.4); }}
        .btn:hover {{ transform: scale(1.05); }}
        .testimonial {{ font-style: italic; border-left: 4px solid var(--accent); padding-left: 20px; margin: 30px 0; color: #cbd5e1; }}
        .ai-authority-section h3 {{ color: var(--accent); margin-top: 30px; }}
        .ai-authority-section p {{ font-size: 1.1rem; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="header">
        <span class="badge">Verified Authority Review 2025</span>
        <h1>Is <span class="highlight">{product['name']}</span> The Missing Link In Your ${random.randint(3,7)},000/mo Plan?</h1>
    </div>

    <div class="container">
        <div class="urgency-bar">⚠️ {urgency_msg} ⚠️</div>
        
        {content_body}

        <div class="cta-box">
            <h3>Ready to skip the trial and error?</h3>
            <p>Don't let the 404s of life slow you down. Get the verified access now.</p>
            <a href="{product['link']}" class="btn" target="_blank">GET INSTANT ACCESS NOW ➔</a>
            <p style="font-size: 0.8rem; margin-top: 15px; opacity: 0.7;">Secure 256-bit encrypted checkout via Digistore24</p>
        </div>
    </div>
</body>
</html>
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return file_path

if __name__ == "__main__":
    pseo = PSEOAI()
    pseo.generate_review_page({"name": "Tube Mastery (2025)", "niche": "AI Automation", "link": "#"})
