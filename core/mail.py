import os

class MailOrbit:
    """
    MailOrbit: Generates weekly newsletter content based on tracked trends and products.
    """
    def __init__(self, brand_name="NexusProfit"):
        self.brand_name = brand_name

    def generate_newsletter(self, products, week_number):
        """Compiles a weekly digest for the email list subscribers."""
        print(f"[MailOrbit] Compiling Weekly Digest (Week {week_number})...")
        
        newsletter_path = f"assets/newsletters/digest_week_{week_number}.html"
        os.makedirs("assets/newsletters", exist_ok=True)
        
        product_rows = ""
        for p in products:
            product_rows += f"""
            <div style="margin-bottom: 20px; border-bottom: 1px solid #38bdf8; padding-bottom: 10px;">
                <h3 style="color: #38bdf8;">{p['name']}</h3>
                <p>Trending in the {p['niche']} sector. Don't miss this high-value opportunity.</p>
                <a href="{p['link']}" style="background: #38bdf8; color: #0f172a; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Access Now</a>
            </div>
            """
            
        html = f"""
        <html>
        <body style="font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px;">
            <div style="max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px;">
                <h1 style="color: #38bdf8; border-bottom: 2px solid #38bdf8;">{self.brand_name} Weekly Digest</h1>
                <p>Welcome to this week's exclusive high-value opportunities. We've scouted the top trends so you don't have to.</p>
                
                {product_rows}
                
                <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 30px;">
                    This is an automated digest from NexusProfit. You received this because you joined our Zero-Risk Wealth Vault.
                </p>
            </div>
        </body>
        </html>
        """
        
        with open(newsletter_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        return newsletter_path

if __name__ == "__main__":
    mail = MailOrbit()
    mail.generate_newsletter([{"name": "AI Tool", "niche": "Tech", "link": "#"}], 1)
