"""
YouTube Channel Banner Generator for Abhrankan Creates
Produces a 2560x1440 banner with strict YouTube Mobile Safe Area (1546x423) alignment.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

def build_banner(backdrop_path, output_path):
    target_w, target_h = 2560, 1440
    
    if os.path.exists(backdrop_path):
        bg = Image.open(backdrop_path).convert("RGB")
        # Scale to fill 2560x1440
        scale = max(target_w / bg.width, target_h / bg.height)
        new_w, new_h = int(bg.width * scale), int(bg.height * scale)
        bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # Center crop
        x_off = (new_w - target_w) // 2
        y_off = (new_h - target_h) // 2
        banner = bg.crop((x_off, y_off, x_off + target_w, y_off + target_h))
    else:
        # Fallback dark cyber room gradient
        banner = Image.new("RGB", (target_w, target_h), (3, 7, 18))
        
    # Contrast and dark cinema mood
    banner = ImageEnhance.Contrast(banner).enhance(1.25)
    banner = ImageEnhance.Brightness(banner).enhance(0.95)
    
    draw = ImageDraw.Draw(banner, "RGBA")
    
    # Safe area coordinates:
    # Desktop / Mobile Safe Zone: Y from 508 to 931 (Height: 423)
    # Mobile Safe Zone X: from 507 to 2053 (Width: 1546)
    safe_y1, safe_y2 = 508, 931
    safe_x1, safe_x2 = 507, 2053
    cy = (safe_y1 + safe_y2) // 2 # 720
    cx = target_w // 2 # 1280
    
    # Vignette darkening outside safe zone so text pops on all screens
    for y in range(safe_y1):
        alpha = int(190 * (1 - y / safe_y1))
        draw.rectangle([(0, y), (target_w, y+1)], fill=(2, 6, 23, alpha))
    for y in range(safe_y2, target_h):
        alpha = int(220 * ((y - safe_y2) / (target_h - safe_y2)))
        draw.rectangle([(0, y), (target_w, y+1)], fill=(2, 6, 23, alpha))
        
    # Subtle central semi-transparent dark backing card inside safe zone
    card_w, card_h = 1380, 360
    c_x1 = cx - card_w // 2
    c_y1 = cy - card_h // 2
    c_x2 = cx + card_w // 2
    c_y2 = cy + card_h // 2
    
    draw.rectangle([(c_x1, c_y1), (c_x2, c_y2)], fill=(3, 7, 18, 205), outline=(56, 189, 248, 120), width=2)
    
    # Corner HUD tech accents on the backing card
    bracket_len = 24
    # Top-Left
    draw.line([(c_x1, c_y1), (c_x1 + bracket_len, c_y1)], fill=(56, 189, 248), width=3)
    draw.line([(c_x1, c_y1), (c_x1, c_y1 + bracket_len)], fill=(56, 189, 248), width=3)
    # Top-Right
    draw.line([(c_x2, c_y1), (c_x2 - bracket_len, c_y1)], fill=(56, 189, 248), width=3)
    draw.line([(c_x2, c_y1), (c_x2, c_y1 + bracket_len)], fill=(56, 189, 248), width=3)
    # Bottom-Left
    draw.line([(c_x1, c_y2), (c_x1 + bracket_len, c_y2)], fill=(56, 189, 248), width=3)
    draw.line([(c_x1, c_y2), (c_x1, c_y2 - bracket_len)], fill=(56, 189, 248), width=3)
    # Bottom-Right
    draw.line([(c_x2, c_y2), (c_x2 - bracket_len, c_y2)], fill=(56, 189, 248), width=3)
    draw.line([(c_x2, c_y2), (c_x2, c_y2 - bracket_len)], fill=(56, 189, 248), width=3)

    # Fonts
    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 78)
        font_tagline = ImageFont.truetype("arialbd.ttf", 30)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
        font_credit = ImageFont.truetype("arial.ttf", 24)
        font_mono = ImageFont.truetype("consola.ttf", 20)
    except:
        font_brand = font_tagline = font_badge = font_credit = font_mono = ImageFont.load_default()

    # 1. Top Category Badge
    badge_text = "ORIGINAL SCI-FI STORIES • CINEMATIC VISUALS • DIGITAL WORLDS"
    draw.text((cx, cy - 110), badge_text, fill=(56, 189, 248), font=font_badge, anchor="mm")
    
    # 2. Main Channel Title (Glowing Cyan & White)
    # Shadow for depth
    draw.text((cx + 3, cy - 35 + 3), "ABHRANKAN CREATES", fill=(0, 0, 0, 240), font=font_brand, anchor="mm")
    draw.text((cx, cy - 35), "ABHRANKAN CREATES", fill=(255, 255, 255), font=font_brand, anchor="mm")
    
    # Subtle horizontal neon separator line
    sep_w = 780
    draw.line([(cx - sep_w // 2, cy + 24), (cx + sep_w // 2, cy + 24)], fill=(56, 189, 248, 180), width=2)
    # Center diamond marker
    draw.polygon([(cx - 6, cy + 24), (cx, cy + 18), (cx + 6, cy + 24), (cx, cy + 30)], fill=(234, 179, 8))

    # 3. Tagline / Series Feature
    draw.text((cx, cy + 62), 'Creator of "SERVER ROOM B" • Where Code Meets Cinema', fill=(234, 179, 8), font=font_tagline, anchor="mm")

    # 4. Author / Creator Credit
    draw.text((cx, cy + 112), "Written & Produced by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    banner.save(output_path, quality=95)
    print(f"✓ YouTube Banner Generated: {output_path} ({os.path.getsize(output_path)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    b_in = os.path.join(repo, "episodes", "keyframes", "scene_01.jpg") # fallback or generated
    b_out = os.path.join(repo, "episodes", "youtube_channel_banner_2560x1440.jpg")
    build_banner(b_in, b_out)
