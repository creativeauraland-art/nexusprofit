from gtts import gTTS
import os

class VocalAI:
    """
    VocalAI: Responsible for generating automated voiceovers for high-engagement content.
    """
    def __init__(self, lang='en', tld='com'):
        self.lang = lang
        self.tld = tld # 'com' for US English, 'co.uk' for British etc.

    def generate_voiceover(self, text, output_path):
        print(f"[VocalAI] Generating Voiceover for: {text[:30]}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            tts = gTTS(text=text, lang=self.lang, tld=self.tld, slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"[VocalAI] Failed to generate voiceover: {e}")
            return None

if __name__ == "__main__":
    vocal = VocalAI()
    vocal.generate_voiceover("The AI tool Silicon Valley is keeping secret.", "assets/audio/test_hook.mp3")
