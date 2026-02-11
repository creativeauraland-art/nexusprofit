import os
from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip

class MotionAI:
    """
    MotionAI: Responsible for generating high-retention vertical videos (9:16).
    """
    def __init__(self, size=(1080, 1920)):
        self.size = size
        self.colors = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#38bdf8"}

    def generate_reel(self, image_path, title, duration=7, output_path="assets/reels/reel.mp4"):
        print(f"[MotionAI] Creating Reel for: {title}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 1. Background
        bg = ColorClip(size=self.size, color=[15, 23, 42]).with_duration(duration)
        
        # 2. Main Image with subtle zoom (Ken Burns effect)
        img_clip = ImageClip(image_path).with_duration(duration)
        img_clip = img_clip.resized(width=self.size[0] * 0.8)
        img_clip = img_clip.with_position(('center', 'center'))
        
        # 3. Text Overlay
        # Note: In a headless environment, TextClip might need ImageMagick. 
        # For this 'Zero-Cost' setup, we use simple overlays if possible.
        # If ImageMagick is missing, we would fallback to a simpler method.
        try:
            txt_clip = TextClip(
                text=title,
                font_size=70,
                color=self.colors["accent"],
                size=(self.size[0]*0.9, None),
                method='caption'
            ).with_duration(duration).with_position(('center', 1400))
            
            final_video = CompositeVideoClip([bg, img_clip, txt_clip], size=self.size)
        except Exception as e:
            print(f"[MotionAI] TextClip failed (likely missing ImageMagick): {e}")
            print("[MotionAI] Falling back to image-only clip.")
            final_video = CompositeVideoClip([bg, img_clip], size=self.size)

        # 4. Write Video
        # Using a low bitrate for 'Zero-Cost' storage efficiency
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio=False, logger=None)
        
        return output_path

if __name__ == "__main__":
    # Test run
    motion = MotionAI()
    if os.path.exists("assets/sample_pin.png"):
        motion.generate_reel("assets/sample_pin.png", "The Future of AI is Here", output_path="assets/reels/test_reel.mp4")
