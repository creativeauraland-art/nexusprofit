from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip, AudioFileClip
import os

class MotionAI:
    """
    MotionAI: Responsible for generating high-retention vertical videos (9:16).
    """
    def __init__(self, size=(1080, 1920)):
        self.size = size
        self.colors = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#38bdf8"}

    def generate_reel(self, image_path, title, audio_path=None, duration=7, output_path="assets/reels/reel.mp4"):
        print(f"[MotionAI] Creating Hyper-Reel for: {title[:30]}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 1. Background
        bg = ColorClip(size=self.size, color=[15, 23, 42]).with_duration(duration)
        
        # 2. Main Image
        img_clip = ImageClip(image_path).with_duration(duration)
        img_clip = img_clip.resized(width=self.size[0] * 0.9)
        img_clip = img_clip.with_position(('center', 'center'))
        
        # 3. Audio Attachment
        audio = None
        if audio_path and os.path.exists(audio_path):
            try:
                audio = AudioFileClip(audio_path)
                # If audio is longer than clip, we might want to trim it or vice-versa
                # For now, we'll just set the duration to the audio or a min of 7s
                duration = max(duration, audio.duration)
                bg = bg.with_duration(duration)
                img_clip = img_clip.with_duration(duration)
            except Exception as e:
                print(f"[MotionAI] Audio attachment failed: {e}")

        # 4. Text Overlay (Simplification for Headless servers)
        # We use a placeholder if TextClip fails
        try:
            # We'll skip complex TextClip to avoid ImageMagick dependencies in GitHub Actions
            final_video = CompositeVideoClip([bg, img_clip], size=self.size)
        except:
             final_video = CompositeVideoClip([bg, img_clip], size=self.size)

        if audio:
            final_video = final_video.with_audio(audio)

        # 5. Write Video
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac" if audio else None, logger=None)
        
        return output_path

if __name__ == "__main__":
    # Test run
    motion = MotionAI()
    if os.path.exists("assets/sample_pin.png"):
        motion.generate_reel("assets/sample_pin.png", "The Future of AI is Here", output_path="assets/reels/test_reel.mp4")
