"""
Server Room B - Complete Director's Cut Thumbnail Generator
Creates prestige, high-converting thumbnails for the 2-Minute Full Film:
1. 9:16 Vertical Poster (720x1280) - For YouTube Shorts, Reels, TikTok & Mobile feeds
2. 16:9 Landscape Poster (1280x720) - For YouTube Main Video uploads, Facebook Video & Desktop
Creator: Abhrankan Chakrabarti / Channel: Abhrankan Creates
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

def get_font(name, size):
    for candidate in [name, "arialbd.ttf", "segoeuib.ttf", "consola.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except:
            pass
    return ImageFont.load_default()

def create_vertical_9x16(repo_dir, kf_dir, out_dir):
    # Base keyframe: scene_08.jpg (macro eye reflecting the glowing terminal code)
    base_p = os.path.join(kf_dir, "scene_08.jpg")
    if not os.path.exists(base_p):
        base_p = os.path.join(kf_dir, "scene_07.jpg")

    img = Image.open(base_p).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Brightness(img).enhance(1.04)
    img = ImageEnhance.Color(img).enhance(1.15)

    # Subtle scanlines for analog/cyber CRT texture
    scanlines = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(scanlines)
    for y in range(0, 1280, 4):
        s_draw.line([(0, y), (720, y)], fill=(0, 0, 0, 24), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), scanlines).convert("RGB")

    draw = ImageDraw.Draw(img, "RGBA")

    # Top dark gradient (y: 0 -> 280)
    for y in range(280):
        alpha = int(235 * (1 - y / 280))
        draw.rectangle([(0, y), (720, y + 1)], fill=(5, 5, 15, alpha))

    # Bottom dark gradient (y: 840 -> 1280)
    for y in range(840, 1280):
        alpha = int(250 * ((y - 840) / 440))
        draw.rectangle([(0, y), (720, y + 1)], fill=(3, 4, 12, alpha))

    font_badge = get_font("arialbd.ttf", 32)
    font_subhook = get_font("arialbd.ttf", 26)
    font_title = get_font("arialbd.ttf", 46)
    font_subtitle = get_font("arialbd.ttf", 28)
    font_credit = get_font("arialbd.ttf", 22)
    font_runtime = get_font("arialbd.ttf", 20)

    # Top Director's Cut Prestige Badge (Purple & Gold)
    badge_w, badge_h = 580, 72
    bx1 = (720 - badge_w) // 2
    by1 = 70
    draw.rounded_rectangle([(bx1 - 3, by1 - 3), (bx1 + badge_w + 3, by1 + badge_h + 3)], radius=12, fill=(139, 92, 246, 70))
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=10, fill=(88, 28, 135, 245), outline=(234, 179, 8), width=3)
    draw.text((720 // 2, by1 + badge_h // 2), "🎬 COMPLETE DIRECTOR'S CUT", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Center-Bottom Hook Callout (y: 835 -> 925)
    hook_w, hook_h = 650, 84
    hx1 = (720 - hook_w) // 2
    hy1 = 835
    draw.rounded_rectangle([(hx1, hy1), (hx1 + hook_w, hy1 + hook_h)], radius=8, fill=(15, 23, 42, 230), outline=(168, 85, 247), width=2)
    draw.text((720 // 2, hy1 + 26), "THE UNIVERSE IS BEING UNINSTALLED", fill=(255, 255, 255), font=font_subhook, anchor="mm")
    draw.text((720 // 2, hy1 + 58), "FULL 2-MINUTE CONTINUOUS FILM • ALL 16 SCENES", fill=(234, 179, 8), font=font_runtime, anchor="mm")

    # Bottom Title Card (y: 960 -> 1220)
    title_text = "SERVER ROOM B"
    title_y = 1005
    for offset in [(-2, -2), (2, 2), (-2, 2), (2, -2), (0, 3)]:
        draw.text((360 + offset[0], title_y + offset[1]), title_text, fill=(168, 85, 247, 180), font=font_title, anchor="mm")
    draw.text((360, title_y), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    draw.text((360, 1070), "Chapter 1 • Out of Memory", fill=(56, 189, 248), font=font_subtitle, anchor="mm")
    draw.text((360, 1135), "Abhrankan Creates", fill=(192, 132, 252), font=font_subhook, anchor="mm")
    draw.text((360, 1180), "Story & Direction by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    # High-Tech Cyber Border Frame
    margin = 16
    draw.rectangle([(margin, margin), (720 - margin, 1280 - margin)], outline=(168, 85, 247, 140), width=2)
    for (cx, cy) in [(margin, margin), (720 - margin, margin), (margin, 1280 - margin), (720 - margin, 1280 - margin)]:
        draw.rectangle([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=(234, 179, 8, 255))

    out_p = os.path.join(out_dir, "thumbnail_directors_cut.jpg")
    img.save(out_p, format="JPEG", quality=95, optimize=True)
    print("Created 9:16 Director's Cut thumbnail:", out_p, f"({os.path.getsize(out_p)} bytes)")
    return out_p

def create_landscape_16x9(repo_dir, kf_dir, out_dir):
    # 1280x720 Landscape for YouTube Standard Upload
    # Combine Scene 08 (macro eye) and Scene 14 (emergency strobe)
    base_eye = os.path.join(kf_dir, "scene_08.jpg")
    base_strobe = os.path.join(kf_dir, "scene_14.jpg")

    im_eye = Image.open(base_eye).convert("RGB")
    im_strobe = Image.open(base_strobe).convert("RGB")

    # Resize both to fill their half with some overlap for blending
    # Canvas is 1280x720
    im_eye_resized = im_eye.resize((680, 720), Image.Resampling.LANCZOS)
    im_strobe_resized = im_strobe.resize((680, 720), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (1280, 720), (5, 5, 15))
    canvas.paste(im_eye_resized, (0, 0))
    
    # Create soft alpha blended right half
    strobe_rgba = im_strobe_resized.convert("RGBA")
    # Linear alpha blend across the left 120 pixels of the strobe image
    alpha_mask = np.ones((720, 680), dtype=np.uint8) * 255
    for x in range(120):
        alpha_mask[:, x] = int(255 * (x / 120))
    strobe_rgba.putalpha(Image.fromarray(alpha_mask))

    canvas.paste(strobe_rgba, (600, 0), strobe_rgba)

    # Color grading
    canvas = ImageEnhance.Contrast(canvas).enhance(1.30)
    canvas = ImageEnhance.Color(canvas).enhance(1.15)
    canvas = ImageEnhance.Brightness(canvas).enhance(1.02)

    # Vignettes
    draw = ImageDraw.Draw(canvas, "RGBA")
    
    # Left & Right edge vignette
    for x in range(160):
        alpha = int(190 * (1 - x / 160))
        draw.line([(x, 0), (x, 720)], fill=(3, 4, 12, alpha))
    for x in range(1120, 1280):
        alpha = int(190 * ((x - 1120) / 160))
        draw.line([(x, 0), (x, 720)], fill=(3, 4, 12, alpha))
        
    # Top gradient (y: 0 -> 160)
    for y in range(160):
        alpha = int(210 * (1 - y / 160))
        draw.rectangle([(0, y), (1280, y + 1)], fill=(3, 4, 12, alpha))
        
    # Bottom gradient (y: 490 -> 720)
    for y in range(490, 720):
        alpha = int(240 * ((y - 490) / 230))
        draw.rectangle([(0, y), (1280, y + 1)], fill=(3, 4, 12, alpha))

    font_badge = get_font("arialbd.ttf", 26)
    font_title = get_font("arialbd.ttf", 52)
    font_sub = get_font("arialbd.ttf", 28)
    font_credit = get_font("arialbd.ttf", 20)

    # Top Prestige Badge
    badge_w, badge_h = 520, 54
    bx = (1280 - badge_w) // 2
    by = 38
    draw.rounded_rectangle([(bx - 2, by - 2), (bx + badge_w + 2, by + badge_h + 2)], radius=8, fill=(139, 92, 246, 80))
    draw.rounded_rectangle([(bx, by), (bx + badge_w, by + badge_h)], radius=8, fill=(88, 28, 135, 240), outline=(234, 179, 8), width=2)
    draw.text((1280 // 2, by + badge_h // 2), "🎬 COMPLETE DIRECTOR'S CUT (FULL FILM)", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Center-Bottom Title Block (y: 540 -> 690)
    title_text = "SERVER ROOM B"
    title_y = 565
    for offset in [(-3, -3), (3, 3), (-3, 3), (3, -3), (0, 3)]:
        draw.text((640 + offset[0], title_y + offset[1]), title_text, fill=(168, 85, 247, 180), font=font_title, anchor="mm")
    draw.text((640, title_y), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    draw.text((640, 625), "Chapter 1: Out of Memory • All 16 Scenes Continuous", fill=(234, 179, 8), font=font_sub, anchor="mm")
    draw.text((640, 672), "Abhrankan Creates • Written & Directed by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    # High-Tech Border
    draw.rectangle([(12, 12), (1268, 708)], outline=(168, 85, 247, 130), width=2)
    for (cx, cy) in [(12, 12), (1268, 12), (12, 708), (1268, 708)]:
        draw.rectangle([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=(234, 179, 8, 255))

    out_p = os.path.join(out_dir, "thumbnail_directors_cut_16x9.jpg")
    canvas.save(out_p, format="JPEG", quality=95, optimize=True)
    print("Created 16:9 Director's Cut thumbnail:", out_p, f"({os.path.getsize(out_p)} bytes)")
    return out_p

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    out_dir = os.path.join(repo_dir, "episodes")
    os.makedirs(out_dir, exist_ok=True)

    create_vertical_9x16(repo_dir, kf_dir, out_dir)
    create_landscape_16x9(repo_dir, kf_dir, out_dir)

if __name__ == "__main__":
    main()
