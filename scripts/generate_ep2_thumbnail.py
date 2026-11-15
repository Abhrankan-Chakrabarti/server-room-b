"""
Server Room B - Episode 2: Force Quit Thumbnail Generator
Creates high-converting 9:16 vertical and 16:9 landscape covers for Episode 2.
Features PID 1 denial badge, 16.67ms frame-lock callout, and cyber thriller typography.
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
    # Base keyframe: scene_14 (emergency strobe shadows) or scene_11
    base_p = os.path.join(kf_dir, "scene_14.jpg")
    if not os.path.exists(base_p):
        base_p = os.path.join(kf_dir, "scene_07.jpg")

    img = Image.open(base_p).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Brightness(img).enhance(1.02)

    # Scanlines
    scanlines = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(scanlines)
    for y in range(0, 1280, 4):
        s_draw.line([(0, y), (720, y)], fill=(0, 0, 0, 24), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), scanlines).convert("RGB")

    draw = ImageDraw.Draw(img, "RGBA")

    # Top dark gradient (y: 0 -> 280)
    for y in range(280):
        alpha = int(235 * (1 - y / 280))
        draw.rectangle([(0, y), (720, y + 1)], fill=(15, 5, 5, alpha))

    # Bottom dark gradient (y: 840 -> 1280)
    for y in range(840, 1280):
        alpha = int(250 * ((y - 840) / 440))
        draw.rectangle([(0, y), (720, y + 1)], fill=(12, 3, 3, alpha))

    font_badge = get_font("arialbd.ttf", 30)
    font_subhook = get_font("arialbd.ttf", 26)
    font_code = get_font("consola.ttf", 24)
    font_title = get_font("arialbd.ttf", 46)
    font_subtitle = get_font("arialbd.ttf", 28)
    font_credit = get_font("arialbd.ttf", 22)

    # Top Urgent Warning Badge: Crimson Alert
    badge_w, badge_h = 580, 72
    bx1 = (720 - badge_w) // 2
    by1 = 70
    draw.rounded_rectangle([(bx1 - 3, by1 - 3), (bx1 + badge_w + 3, by1 + badge_h + 3)], radius=10, fill=(220, 38, 38, 70))
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=8, fill=(185, 28, 28, 245), outline=(254, 202, 202), width=3)
    draw.text((720 // 2, by1 + badge_h // 2), "KILL: (PID 1): NOT PERMITTED", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Center-Bottom Terminal Glitch Box (y: 830 -> 925)
    hook_w, hook_h = 650, 88
    hx1 = (720 - hook_w) // 2
    hy1 = 830
    draw.rounded_rectangle([(hx1, hy1), (hx1 + hook_w, hy1 + hook_h)], radius=8, fill=(15, 23, 42, 235), outline=(239, 68, 68), width=2)
    draw.text((720 // 2, hy1 + 26), "YOU CANNOT KILL THE PROCESS OF REALITY", fill=(255, 255, 255), font=font_subhook, anchor="mm")
    draw.text((720 // 2, hy1 + 58), "PHYSICS TIMESTEP REDUCED TO 16.67ms (60Hz)", fill=(252, 165, 165), font=font_code, anchor="mm")

    # Bottom Title Card (y: 960 -> 1220)
    title_text = "SERVER ROOM B"
    title_y = 1005
    for offset in [(-2, -2), (2, 2), (-2, 2), (2, -2), (0, 3)]:
        draw.text((360 + offset[0], title_y + offset[1]), title_text, fill=(239, 68, 68, 180), font=font_title, anchor="mm")
    draw.text((360, title_y), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    draw.text((360, 1070), "Chapter 2 • Force Quit", fill=(234, 179, 8), font=font_subtitle, anchor="mm")
    draw.text((360, 1135), "Abhrankan Creates", fill=(192, 132, 252), font=font_subhook, anchor="mm")
    draw.text((360, 1180), "Story & Direction by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    # Frame
    margin = 16
    draw.rectangle([(margin, margin), (720 - margin, 1280 - margin)], outline=(239, 68, 68, 140), width=2)
    for (cx, cy) in [(margin, margin), (720 - margin, margin), (margin, 1280 - margin), (720 - margin, 1280 - margin)]:
        draw.rectangle([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=(234, 179, 8, 255))

    out_p = os.path.join(out_dir, "thumbnail_episode_02.jpg")
    img.save(out_p, format="JPEG", quality=95, optimize=True)
    print("Created 9:16 Episode 2 thumbnail:", out_p, f"({os.path.getsize(out_p)} bytes)")
    return out_p

def create_landscape_16x9(repo_dir, kf_dir, out_dir):
    base_eye = os.path.join(kf_dir, "scene_07.jpg")
    base_strobe = os.path.join(kf_dir, "scene_14.jpg")

    im_left = Image.open(base_eye).convert("RGB").resize((680, 720), Image.Resampling.LANCZOS)
    im_right = Image.open(base_strobe).convert("RGB").resize((680, 720), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (1280, 720), (10, 5, 5))
    canvas.paste(im_left, (0, 0))

    right_rgba = im_right.convert("RGBA")
    alpha_mask = np.ones((720, 680), dtype=np.uint8) * 255
    for x in range(120):
        alpha_mask[:, x] = int(255 * (x / 120))
    right_rgba.putalpha(Image.fromarray(alpha_mask))
    canvas.paste(right_rgba, (600, 0), right_rgba)

    canvas = ImageEnhance.Contrast(canvas).enhance(1.30)
    canvas = ImageEnhance.Color(canvas).enhance(1.10)

    draw = ImageDraw.Draw(canvas, "RGBA")
    # Vignettes
    for x in range(160):
        alpha = int(190 * (1 - x / 160))
        draw.line([(x, 0), (x, 720)], fill=(8, 2, 2, alpha))
    for x in range(1120, 1280):
        alpha = int(190 * ((x - 1120) / 160))
        draw.line([(x, 0), (x, 720)], fill=(8, 2, 2, alpha))
    for y in range(160):
        alpha = int(210 * (1 - y / 160))
        draw.rectangle([(0, y), (1280, y + 1)], fill=(8, 2, 2, alpha))
    for y in range(490, 720):
        alpha = int(240 * ((y - 490) / 230))
        draw.rectangle([(0, y), (1280, y + 1)], fill=(8, 2, 2, alpha))

    font_badge = get_font("arialbd.ttf", 26)
    font_title = get_font("arialbd.ttf", 52)
    font_sub = get_font("arialbd.ttf", 28)
    font_credit = get_font("arialbd.ttf", 20)

    # Top Badge
    badge_w, badge_h = 560, 54
    bx = (1280 - badge_w) // 2
    by = 38
    draw.rounded_rectangle([(bx - 2, by - 2), (bx + badge_w + 2, by + badge_h + 2)], radius=8, fill=(220, 38, 38, 80))
    draw.rounded_rectangle([(bx, by), (bx + badge_w, by + badge_h)], radius=8, fill=(185, 28, 28, 240), outline=(254, 202, 202), width=2)
    draw.text((1280 // 2, by + badge_h // 2), "🔴 KILL (PID 1): OPERATION NOT PERMITTED", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Center-Bottom Title Block
    title_text = "SERVER ROOM B"
    title_y = 565
    for offset in [(-3, -3), (3, 3), (-3, 3), (3, -3), (0, 3)]:
        draw.text((640 + offset[0], title_y + offset[1]), title_text, fill=(239, 68, 68, 180), font=font_title, anchor="mm")
    draw.text((640, title_y), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    draw.text((640, 625), "Chapter 2: Force Quit • When Reality Denies Your Kill Command", fill=(234, 179, 8), font=font_sub, anchor="mm")
    draw.text((640, 672), "Abhrankan Creates • Written & Directed by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

    # Tech Border
    draw.rectangle([(12, 12), (1268, 708)], outline=(239, 68, 68, 130), width=2)
    for (cx, cy) in [(12, 12), (1268, 12), (12, 708), (1268, 708)]:
        draw.rectangle([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=(234, 179, 8, 255))

    out_p = os.path.join(out_dir, "thumbnail_episode_02_16x9.jpg")
    canvas.save(out_p, format="JPEG", quality=95, optimize=True)
    print("Created 16:9 Episode 2 thumbnail:", out_p, f"({os.path.getsize(out_p)} bytes)")
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
