from core.persona import PersonaAI
import os

def test_visuals():
    print("🎨 Starting Visual Overhaul Verification...")
    persona = PersonaAI(brand_name="NexusProfit")
    
    # Test cases: Long titles (the collision risk)
    test_cases = [
        {
            "title": "THE GENIUS WAVE: HOW TO AWAKEN YOUR BRAIN PERFORMANCE IN 7 MINUTES",
            "desc": "PEAK MENTAL CLARITY",
            "style": "designer",
            "aesthetic": "POETCORE",
            "path": "assets/test_overhaul_1.png"
        },
        {
            "title": "PRODENTIM GUTS: THE CLINICALLY PROVEN TOOTHPASTE HACK YOU NEVER HEARD",
            "desc": "SMILE FROM THE INSIDE",
            "style": "viral_lifestyle",
            "aesthetic": "EXPEDITION",
            "path": "assets/test_overhaul_2.png"
        },
        {
            "title": "HOW I MAKE $3,800 EVERY SINGLE DAY USING PINTEREST AUTOMATION",
            "desc": "ZERO EXPERIENCE NEEDED",
            "style": "money_maker",
            "aesthetic": "CHERRY_CODED",
            "path": "assets/test_overhaul_3.png"
        },
        {
            "title": "STOP THE 9-5 GRIND: HOW I BUILT MY LUXURY LIFE FROM MY BEDROOM",
            "desc": "THE COMPLETE FREEDOM BLUEPRINT",
            "style": "aspiration",
            "aesthetic": "CHERRY_CODED",
            "path": "assets/test_overhaul_4.png"
        },
        {
            "title": "BEYOND THE DESK: THE MOMENT EVERYTHING CHANGED",
            "desc": "A SURREAL PROFIT BLUEPRINT",
            "style": "visionary",
            "aesthetic": "VAMP_ROMANTIC",
            "path": "assets/test_overhaul_5.png"
        },
        {
            "title": "MIDNIGHT MANIFESTO: THE SECRET TO PROFIT REFLECTIONS",
            "desc": "NEON GROWTH STRATEGY",
            "style": "neon_whisper",
            "aesthetic": "NONE",
            "path": "assets/test_overhaul_6.png"
        },
        {
            "title": "THE GENIUS WAVE: HOW TO AWAKEN YOUR BRAIN PERFORMANCE IN 7 MINUTES",
            "desc": "PEAK MENTAL CLARITY",
            "style": "studio",
            "aesthetic": "NONE",
            "path": "assets/test_studio_1.png"
        }
    ]
    
    for tc in test_cases:
        print(f"  📸 Generating: {tc['style']}...")
        persona.generate_pin_image(
            title=tc['title'],
            description=tc['desc'],
            output_path=tc['path'],
            niche="Health",
            style=tc['style'],
            aesthetic=tc['aesthetic']
        )
        print(f"  ✅ Saved: {tc['path']}")

if __name__ == "__main__":
    test_visuals()
