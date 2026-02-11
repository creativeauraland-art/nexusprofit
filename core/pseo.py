import os

class PSEOAI:
    """
    PSEOAI: Generates programmatic SEO pages for every product to capture Google Search traffic.
    """
    def __init__(self, output_dir="reviews"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_review_page(self, product):
        """Creates a standalone HTML review page for a product."""
        safe_filename = product['name'].replace(" ", "-").lower().replace("(", "").replace(")", "")
        file_path = f"{self.output_dir}/{safe_filename}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['name']} Review 2025: Is it worth it?</title>
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; line-height: 1.6; padding: 40px; }}
        .container {{ max-width: 800px; margin: auto; background: rgba(30, 41, 59, 0.7); padding: 30px; border-radius: 15px; border: 1px solid #38bdf8; }}
        h1 {{ color: #38bdf8; }}
        .btn {{ display: inline-block; background: #38bdf8; color: #0f172a; padding: 15px 30px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Detailed Review: {product['name']}</h1>
        <p>Looking for a high-performance solution in <strong>{product['niche']}</strong>? We've analyzed {product['name']} to see if it lives up to the hype.</p>
        
        <h2>Why we recommend it:</h2>
        <ul>
            <li>Proven ROI in the {product['niche']} sector.</li>
            <li>Instant access to premium resources.</li>
            <li>Top-tier support and community.</li>
        </ul>

        <p>Don't miss out on this high-value opportunity.</p>
        <a href="{product['link']}" class="btn" target="_blank">Access {product['name']} Now</a>
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
