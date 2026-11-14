"""
Server Room B - High-Converting 9:16 Video Thumbnail & Poster Generator
Generates high-contrast vertical covers with vignettes, hook badges, and typography.
Credit: Story by Abhrankan Chakrabarti
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def generate():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    out_dir = os.path.join(repo_dir, "episodes")

    try:
        font_hook = ImageFont.truetype("arialbd.ttf", 44)
        font_subhook = ImageFont.truetype("arialbd.ttf", 30)
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_credit = ImageFont.truetype("arialbd.ttf", 24)
    except:
        font_hook = font_subhook = font_title = font_credit = ImageFont.load_default()

    # --- 1. Thumbnail for Part 1: The Packet ---
    base_p1 = os.path.join(kf_dir, "scene_07.jpg")
    img1 = Image.open(base_p1).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    img1 = ImageEnhance.Contrast(img1).enhance(1.25)
    img1 = ImageEnhance.Brightness(img1).enhance(1.05)

    draw1 = ImageDraw.Draw(img1, "RGBA")
    for y in range(260):
        alpha = int(220 * (1 - y / 260))
        draw1.rectangle([(0, y), (720, y + 1)], fill=(0, 0, 0, alpha))
    for y in range(1000, 1280):
        alpha = int(240 * ((y - 1000) / 280))
        draw1.rectangle([(0, y), (720, y + 1)], fill=(0, 0, 0, alpha))

    # Top Hook Badge
    badge_w, badge_h = 440, 68
    bx1, by1 = (720 - badge_w) // 2, 80
    draw1.rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], fill=(220, 38, 38, 230), outline=(254, 202, 202), width=3)
    draw1.text((720 // 2, by1 + badge_h // 2), "SOURCE: 0.0.0.0", fill=(255, 255, 255), font=font_hook, anchor="mm")

    # Center-Bottom Curiosity Question
    draw1.rectangle([(40, 890), (680, 960)], fill=(0, 0, 0, 210), outline=(56, 189, 248), width=2)
    draw1.text((360, 925), "WHEN REALITY CRASHES", fill=(56, 189, 248), font=font_subhook, anchor="mm")

    # Title Card
    draw1.text((360, 1070), "SERVER ROOM B", fill=(255, 255, 255), font=font_hook, anchor="mm")
    draw1.text((360, 1125), "Episode 1 • The Packet", fill=(234, 179, 8), font=font_subhook, anchor="mm")
    draw1.text((360, 1180), "Story by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")
    draw1.rectangle([(12, 12), (708, 1268)], outline=(56, 189, 248, 160), width=3)

    p1_out = os.path.join(out_dir, "thumbnail_part1.jpg")
    img1.save(p1_out, quality=95)
    print("Saved:", p1_out)

    # --- 2. Thumbnail for Part 2: Reality Uninstall ---
    base_p2 = os.path.join(kf_dir, "scene_11.jpg")
    img2 = Image.open(base_p2).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    img2 = ImageEnhance.Contrast(img2).enhance(1.30)
    img2 = ImageEnhance.Brightness(img2).enhance(1.05)

    draw2 = ImageDraw.Draw(img2, "RGBA")
    for y in range(260):
        alpha = int(220 * (1 - y / 260))
        draw2.rectangle([(0, y), (720, y + 1)], fill=(0, 0, 0, alpha))
    for y in range(980, 1280):
        alpha = int(245 * ((y - 980) / 300))
        draw2.rectangle([(0, y), (720, y + 1)], fill=(0, 0, 0, alpha))

    # Top Warning Hook
    badge_w2, badge_h2 = 540, 68
    bx2, by2 = (720 - badge_w2) // 2, 80
    draw2.rectangle([(bx2, by2), (bx2 + badge_w2, by2 + badge_h2)], fill=(185, 28, 28, 235), outline=(254, 202, 202), width=3)
    draw2.text((720 // 2, by2 + badge_h2 // 2), "REALITY UNINSTALLING", fill=(255, 255, 255), font=font_hook, anchor="mm")

    # Middle Glitch Box
    draw2.rectangle([(40, 890), (680, 960)], fill=(0, 0, 0, 220), outline=(239, 68, 68), width=2)
    draw2.text((360, 925), "THIS IS NOT A BUG.", fill=(254, 202, 202), font=font_subhook, anchor="mm")

    # Bottom Title Card
    draw2.text((360, 1070), "SERVER ROOM B", fill=(255, 255, 255), font=font_hook, anchor="mm")
    draw2.text((360, 1125), "Part 2 • Reality Uninstall", fill=(234, 179, 8), font=font_subhook, anchor="mm")
    draw2.text((360, 1180), "Story by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")
    draw2.rectangle([(12, 12), (708, 1268)], outline=(239, 68, 68, 160), width=3)

    p2_out = os.path.join(out_dir, "thumbnail_part2.jpg")
    img2.save(p2_out, quality=95)
    print("Saved:", p2_out)

if __name__ == "__main__":
    generate()
