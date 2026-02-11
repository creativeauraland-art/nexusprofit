import google.generativeai as genai

class PersonaAI:
    """
    PersonaAI: Responsible for creating a consistent brand aesthetic and viral hooks.
    """
    def __init__(self, brand_name="NexusProfit"):
        self.brand_name = brand_name
        self.colors = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#38bdf8"}
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_viral_hook(self, product_name, niche):
        """Uses AI to generate a psychological 'Force-Stop' hook for the first 3s."""
        if not self.model:
            return f"Secret to {niche}: {product_name}"
            
        prompt = f"Write a psychological 1-sentence viral hook for {product_name} in the {niche} niche. Make it sound like a secret Silicon Valley hack or a massive money glitch. No hashtags, just the text."
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().replace('"', '')
        except:
            return f"They don't want you to know about {product_name}"

    def generate_pin_image(self, title, description, output_path):
        print(f"[PersonaAI] Rendering Visual: {title[:30]}...")
        # (Rest of the rendering logic remains the same)

if __name__ == "__main__":
    persona = PersonaAI()
    persona.generate_pin_image("The Future of AI", "Automate your life in 2025.", "assets/sample_pin.png")
