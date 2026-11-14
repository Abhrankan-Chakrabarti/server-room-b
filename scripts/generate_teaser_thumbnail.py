"""
Server Room B - High-Converting 9:16 Teaser Thumbnail Generator
Creates a vertical (720x1280) promotional cover for the 15-second Sunday hype teaser.
Optimized for YouTube Shorts, Instagram Reels, and Facebook Stories/Posts.
Creator: Abhrankan Chakrabarti / Channel: Abhrankan Creates
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

def generate():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    out_dir = os.path.join(repo_dir, "episodes")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Base Keyframe Selection: Scene 14 (emergency strobe shadows, peak tension)
    base_path = os.path.join(kf_dir, "scene_14.jpg")
    if not os.path.exists(base_path):
        base_path = os.path.join(kf_dir, "scene_11.jpg")
    
    img = Image.open(base_path).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    
    # Cinematic contrast & grading
    img = ImageEnhance.Contrast(img).enhance(1.30)
    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Brightness(img).enhance(1.02)

    # 2. Add subtle scanline texture for hard sci-fi feel
    scanlines = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(scanlines)
    for y in range(0, 1280, 4):
        s_draw.line([(0, y), (720, y)], fill=(0, 0, 0, 22), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), scanlines).convert("RGB")

    # 3. Vignette overlays (top and bottom gradients for maximum legibility)
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Top dark gradient (y: 0 -> 280)
    for y in range(280):
        alpha = int(230 * (1 - y / 280))
        draw.rectangle([(0, y), (720, y + 1)], fill=(2, 6, 23, alpha))
        
    # Bottom dark gradient (y: 860 -> 1280)
    for y in range(860, 1280):
        alpha = int(250 * ((y - 860) / 420))
        draw.rectangle([(0, y), (720, y + 1)], fill=(2, 6, 23, alpha))

    # Font loading with fallbacks
    def get_font(name, size):
        for candidate in [name, "arialbd.ttf", "segoeuib.ttf", "consola.ttf"]:
            try:
                return ImageFont.truetype(candidate, size)
            except:
                pass
        return ImageFont.load_default()

    font_badge = get_font("arialbd.ttf", 34)
    font_hook = get_font("arialbd.ttf", 36)
    font_subhook = get_font("arialbd.ttf", 26)
    font_title = get_font("arialbd.ttf", 46)
    font_subtitle = get_font("arialbd.ttf", 28)
    font_credit = get_font("arialbd.ttf", 22)

    # 4. Top Urgency / Hype Badge: "⚡ DROPPING THIS SUNDAY"
    badge_w, badge_h = 560, 72
    bx1 = (720 - badge_w) // 2
    by1 = 70
    
    # Outer glow
    draw.rounded_rectangle([(bx1 - 3, by1 - 3), (bx1 + badge_w + 3, by1 + badge_h + 3)], radius=12, fill=(16, 185, 129, 60))
    # Badge body: High-voltage emerald green with dark backdrop
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=10, fill=(5, 150, 105, 240), outline=(110, 231, 183), width=3)
    draw.text((720 // 2, by1 + badge_h // 2), "⚡ DROPPING THIS SUNDAY", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # 5. Curiosity Hook Box (Center-Bottom, y: 840 -> 930)
    hook_box_w = 640
    hook_box_h = 80
    hx1 = (720 - hook_box_w) // 2
    hy1 = 840
    
    draw.rounded_rectangle([(hx1, hy1), (hx1 + hook_box_w, hy1 + hook_box_h)], radius=8, fill=(15, 23, 42, 225), outline=(56, 189, 248), width=2)
    draw.text((720 // 2, hy1 + 25), "THE SYSTEM IS COMPILING YOU.", fill=(255, 255, 255), font=font_subhook, anchor="mm")
    draw.text((720 // 2, hy1 + 56), "15-SECOND SNEAK PEEK", fill=(56, 189, 248), font=font_credit, anchor="mm")

    # 6. Title Block (y: 970 -> 1220)
    # Series Title with glowing drop shadow
    title_text = "SERVER ROOM B"
    title_y = 1010
    for offset in [(-2, -2), (2, 2), (-2, 2), (2, -2), (0, 3)]:
        draw.text((360 + offset[0], title_y + offset[1]), title_text, fill=(14, 165, 233, 160), font=font_title, anchor="mm")
    draw.text((360, title_y), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    # Subtitle: Original Sci-Fi Thriller
    draw.text((360, 1075), "ORIGINAL SCI-FI THRILLER", fill=(234, 179, 8), font=font_subtitle, anchor="mm")
    
    # Creator & Channel Branding
    draw.text((360, 1140), "Abhrankan Creates", fill=(192, 132, 252), font=font_subhook, anchor="mm")
    draw.text((360, 1185), "Story & Direction by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    # 7. High-Tech Tech Corner Brackets / Frame
    frame_margin = 16
    draw.rectangle([(frame_margin, frame_margin), (720 - frame_margin, 1280 - frame_margin)], outline=(16, 185, 129, 140), width=2)
    # Inner corner accent tabs
    corner_len = 28
    for (cx, cy) in [(frame_margin, frame_margin), (720 - frame_margin, frame_margin),
                     (frame_margin, 1280 - frame_margin), (720 - frame_margin, 1280 - frame_margin)]:
        draw.rectangle([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=(56, 189, 248, 240))

    # Save deliverable
    out_path = os.path.join(out_dir, "thumbnail_teaser.jpg")
    img.save(out_path, format="JPEG", quality=95, optimize=True)
    print(f"Teaser thumbnail successfully created: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    generate()
