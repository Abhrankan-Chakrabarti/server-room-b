"""
Server Room B - Episode 3: Link Stage Thumbnail & Keyframe Generator
Creates 9:16 vertical and 16:9 landscape covers, plus high-res keyframes for scenes 1-8.
Creator: Abhrankan Chakrabarti / Channel: Abhrankan Creates
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

def get_font(name, size):
    for candidate in [name, "arialbd.ttf", "segoeuib.ttf", "consola.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except:
            pass
    return ImageFont.load_default()

def draw_centered_text(draw, text, cx, cy, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)

def create_keyframes(repo_dir):
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    os.makedirs(kf_dir, exist_ok=True)
    w, h = 720, 1280

    # 1. Scene 17: Circular Buffer Corridor
    im1 = Image.new("RGB", (w, h), (8, 12, 22))
    d1 = ImageDraw.Draw(im1)
    for y in range(h):
        alpha = int(40 * (1 - abs(y - h // 2) / (h // 2)))
        d1.line([(0, y), (w, y)], fill=(12, 24, 40 + alpha))
    # Perspective corridor lines
    for x in range(0, w, 60):
        d1.line([(x, 0), (w // 2, h // 2)], fill=(20, 35, 60), width=2)
        d1.line([(x, h), (w // 2, h // 2)], fill=(20, 35, 60), width=2)
    # Sodium flicker lamp
    d1.ellipse([(w // 2 - 80, 240), (w // 2 + 80, 270)], fill=(234, 179, 8))
    # Low-poly texture artifact blocks
    for bx in range(120, 600, 70):
        for by in range(500, 800, 50):
            d1.rectangle([(bx, by), (bx + 60, by + 40)], outline=(56, 189, 248), width=1)
    im1.save(os.path.join(kf_dir, "scene_17.jpg"), quality=95)

    # 2. Scene 18: Retinal Burn-in 41% Eye Macro
    im2 = Image.new("RGB", (w, h), (3, 5, 10))
    d2 = ImageDraw.Draw(im2)
    cx, cy = w // 2, h // 2 - 40
    # Eye sclera & iris
    d2.ellipse([(cx - 260, cy - 140), (cx + 260, cy + 140)], fill=(15, 20, 30), outline=(56, 189, 248), width=2)
    d2.ellipse([(cx - 130, cy - 130), (cx + 130, cy + 130)], fill=(8, 45, 60), outline=(34, 197, 94), width=3)
    d2.ellipse([(cx - 60, cy - 60), (cx + 60, cy + 60)], fill=(0, 0, 0))
    # Burning green code on retina
    f_code = get_font("consola.ttf", 26)
    draw_centered_text(d2, "COMPILING USER_ABHRANKAN", cx, cy - 18, f_code, (74, 222, 128))
    draw_centered_text(d2, "PROGRESS: 41%", cx, cy + 18, f_code, (239, 68, 68))
    im2.save(os.path.join(kf_dir, "scene_18.jpg"), quality=95)

    # 3. Scene 19: MDF Server Vault & Cisco Backbone
    im3 = Image.new("RGB", (w, h), (4, 8, 16))
    d3 = ImageDraw.Draw(im3)
    # Rack frame
    d3.rectangle([(100, 160), (620, 1100)], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    for y_u in range(200, 1080, 50):
        d3.rectangle([(120, y_u), (600, y_u + 42)], fill=(2, 6, 23), outline=(30, 41, 59), width=1)
        # Port LEDs
        for p in range(140, 580, 24):
            color = (56, 189, 248) if (p + y_u) % 7 == 0 else (34, 197, 94)
            d3.ellipse([(p, y_u + 16), (p + 8, y_u + 24)], fill=color)
    d3.text((140, 215), "MDF-CORE-SW01 [CATALYST 9600 BARE METAL]", fill=(234, 179, 8), font=get_font("consola.ttf", 18))
    im3.save(os.path.join(kf_dir, "scene_19.jpg"), quality=95)

    # 4. Scene 20: Serial Console Hook /dev/ttyUSB0
    im4 = Image.new("RGB", (w, h), (6, 10, 18))
    d4 = ImageDraw.Draw(im4)
    # Laptop screen
    d4.rectangle([(80, 360), (640, 840)], fill=(2, 6, 23), outline=(56, 189, 248), width=3)
    f_t = get_font("consola.ttf", 22)
    d4.text((110, 400), "$ screen /dev/ttyUSB0 115200", fill=(255, 255, 255), font=f_t)
    d4.text((110, 450), "MDF-CORE-SW01> enable", fill=(74, 222, 128), font=f_t)
    d4.text((110, 500), "Password: ************", fill=(148, 163, 184), font=f_t)
    d4.text((110, 550), "MDF-CORE-SW01#", fill=(74, 222, 128), font=f_t)
    # Doorway vanishing into flat gray wall in background
    d4.rectangle([(240, 80), (480, 320)], fill=(71, 85, 105), outline=(100, 116, 139), width=2)
    draw_centered_text(d4, "[EXIT DOOR CULLED]", 360, 200, f_t, (239, 68, 68))
    im4.save(os.path.join(kf_dir, "scene_20.jpg"), quality=95)

    # 5. Scene 21: 8-Bit VGA Snapping (67%)
    im5 = Image.new("RGB", (w, h), (10, 14, 24))
    d5 = ImageDraw.Draw(im5)
    # VGA Dithering blocks
    for bx in range(0, w, 16):
        for by in range(0, h, 16):
            if (bx // 16 + by // 16) % 2 == 0:
                d5.rectangle([(bx, by), (bx + 16, by + 16)], fill=(20, 20, 40))
            else:
                d5.rectangle([(bx, by), (bx + 16, by + 16)], fill=(10, 30, 60))
    d5.rectangle([(80, 460), (640, 620)], fill=(0, 0, 128), outline=(255, 255, 255), width=4)
    draw_centered_text(d5, "VGA 8-BIT PALETTE QUANTIZATION", 360, 510, get_font("arialbd.ttf", 26), (255, 255, 255))
    draw_centered_text(d5, "COMPILING USER_ABHRANKAN... 67%", 360, 570, get_font("consola.ttf", 24), (255, 255, 0))
    im5.save(os.path.join(kf_dir, "scene_21.jpg"), quality=95)

    # 6. Scene 22: Hardware ACL Access-List
    im6 = Image.new("RGB", (w, h), (4, 8, 16))
    d6 = ImageDraw.Draw(im6)
    d6.rectangle([(60, 340), (660, 720)], fill=(15, 23, 42), outline=(239, 68, 68), width=3)
    f_acl = get_font("consola.ttf", 22)
    d6.text((80, 380), "MDF-CORE-SW01(config)# ip access-list BLOCK_COMPILER", fill=(255, 255, 255), font=f_acl)
    d6.text((80, 430), "  deny udp any any eq 8080", fill=(239, 68, 68), font=f_acl)
    d6.text((80, 480), "  deny ip host 0.0.0.0 any", fill=(239, 68, 68), font=f_acl)
    d6.text((80, 530), "  permit ip any any", fill=(74, 222, 128), font=f_acl)
    d6.text((80, 620), "[DRIVER HOOK DETECTED: LEFT BRACHIAL PLEXUS]", fill=(234, 179, 8), font=f_acl)
    im6.save(os.path.join(kf_dir, "scene_22.jpg"), quality=95)

    # 7. Scene 23: The 0ms Timeless Freeze (89%)
    im7 = Image.new("RGB", (w, h), (2, 4, 10))
    d7 = ImageDraw.Draw(im7)
    # Keyboard Enter key macro
    d7.rectangle([(160, 480), (560, 700)], fill=(30, 41, 59), outline=(56, 189, 248), width=4)
    draw_centered_text(d7, "ENTER ↵", 360, 590, get_font("arialbd.ttf", 52), (255, 255, 255))
    # Frozen time HUD
    d7.rectangle([(100, 200), (620, 290)], fill=(0, 0, 0, 220), outline=(234, 179, 8), width=2)
    draw_centered_text(d7, "TIME STATUS: 0.00ms [TIMESTEP FROZEN]", 360, 245, get_font("consola.ttf", 22), (234, 179, 8))
    draw_centered_text(d7, "COMPILING USER_ABHRANKAN... 89%", 360, 800, get_font("consola.ttf", 26), (239, 68, 68))
    im7.save(os.path.join(kf_dir, "scene_23.jpg"), quality=95)

    # 8. Scene 24: Connection Reset by Peer & 3-Inch Wall Offset
    im8 = Image.new("RGB", (w, h), (6, 10, 20))
    d8 = ImageDraw.Draw(im8)
    # Misaligned door frame
    d8.rectangle([(160, 280), (360, 940)], fill=(30, 41, 59), outline=(148, 163, 184), width=3)
    # Sheared right side of door (3 inches / 36px offset)
    d8.rectangle([(360, 316), (560, 976)], fill=(30, 41, 59), outline=(239, 68, 68), width=3)
    d8.line([(160, 280), (360, 280)], fill=(234, 179, 8), width=3)
    d8.line([(360, 316), (560, 316)], fill=(234, 179, 8), width=3)
    d8.line([(360, 280), (360, 316)], fill=(239, 68, 68), width=4)
    draw_centered_text(d8, "SECTOR 4 PERIMETER: +3.0 INCH OFFSET", 360, 220, get_font("consola.ttf", 20), (234, 179, 8))
    draw_centered_text(d8, "%ACL-I-APPLIED: Connection reset by peer.", 360, 1050, get_font("consola.ttf", 22), (74, 222, 128))
    im8.save(os.path.join(kf_dir, "scene_24.jpg"), quality=95)

    print("✅ All 8 keyframes (scene_17.jpg - scene_24.jpg) created in", kf_dir)

def create_vertical_poster(repo_dir):
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    out_dir = os.path.join(repo_dir, "episodes")
    base_p = os.path.join(kf_dir, "scene_18.jpg")
    
    img = Image.open(base_p).convert("RGB").resize((720, 1280), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.30)

    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(280):
        alpha = int(240 * (1 - y / 280))
        draw.rectangle([(0, y), (720, y + 1)], fill=(5, 8, 18, alpha))
    for y in range(800, 1280):
        alpha = int(250 * ((y - 800) / 480))
        draw.rectangle([(0, y), (720, y + 1)], fill=(4, 6, 14, alpha))

    # Top Warning Badge
    draw.rectangle([(60, 60), (660, 130)], fill=(0, 0, 0, 230), outline=(239, 68, 68), width=2)
    draw_centered_text(draw, "COMPILING USER_ABHRANKAN... 89%", 360, 95, get_font("arialbd.ttf", 26), (239, 68, 68))

    # Center Callout
    draw_centered_text(draw, "THE HARDWARE IS HIS BRAIN", 360, 200, get_font("arialbd.ttf", 28), (234, 179, 8))

    # Bottom Titles
    draw_centered_text(draw, "SERVER ROOM B", 360, 920, get_font("arialbd.ttf", 52), (255, 255, 255))
    draw_centered_text(draw, "CHAPTER 3 • LINK STAGE", 360, 985, get_font("arialbd.ttf", 30), (56, 189, 248))
    draw_centered_text(draw, "0ms TIME FREEZE • BARE-METAL CISCO ACL", 360, 1040, get_font("consola.ttf", 20), (148, 163, 184))

    # Creator Credit
    draw.rectangle([(80, 1100), (640, 1160)], fill=(15, 23, 42, 240), outline=(234, 179, 8), width=2)
    draw_centered_text(draw, "Story by Abhrankan Chakrabarti", 360, 1130, get_font("arialbd.ttf", 22), (255, 255, 255))
    draw_centered_text(draw, "Abhrankan Creates • Official Sci-Fi Thriller", 360, 1210, get_font("consola.ttf", 18), (192, 132, 252))

    out_p = os.path.join(out_dir, "thumbnail_episode_03.jpg")
    img.save(out_p, quality=95)
    print(f"✅ Vertical poster: {out_p}")

def create_landscape_cover(repo_dir):
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")
    out_dir = os.path.join(repo_dir, "episodes")
    base_p = os.path.join(kf_dir, "scene_19.jpg")

    img = Image.open(base_p).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.30)

    draw = ImageDraw.Draw(img, "RGBA")
    # Left vignette
    for x in range(600):
        alpha = int(240 * (1 - x / 600))
        draw.rectangle([(x, 0), (x + 1, 720)], fill=(4, 6, 15, alpha))

    # Top badge
    draw.rectangle([(60, 50), (560, 110)], fill=(0, 0, 0, 230), outline=(239, 68, 68), width=2)
    draw_centered_text(draw, "CRITICAL: BARE METAL CISCO OVERRIDE", 310, 80, get_font("arialbd.ttf", 22), (239, 68, 68))

    draw.text((60, 170), "SERVER ROOM B", fill=(255, 255, 255), font=get_font("arialbd.ttf", 64))
    draw.text((60, 250), "CHAPTER 3: LINK STAGE", fill=(56, 189, 248), font=get_font("arialbd.ttf", 36))
    draw.text((60, 310), "When reality decompiles, drop the hardware ACL.", fill=(234, 179, 8), font=get_font("consola.ttf", 24))

    # Specs
    draw.text((60, 420), "• Cisco MDF-CORE-SW01 Serial Injection (/dev/ttyUSB0)", fill=(148, 163, 184), font=get_font("consola.ttf", 20))
    draw.text((60, 460), "• 8-Bit VGA Quantization & Memory Register Overwrite", fill=(148, 163, 184), font=get_font("consola.ttf", 20))
    draw.text((60, 500), "• 0.00ms Time Freeze at 89% Compilation", fill=(148, 163, 184), font=get_font("consola.ttf", 20))
    draw.text((60, 540), "• Connection Reset by Peer & 3-Inch Wall Offset", fill=(148, 163, 184), font=get_font("consola.ttf", 20))

    # Creator Credit
    draw.text((60, 630), "Story by Abhrankan Chakrabarti", fill=(255, 255, 255), font=get_font("arialbd.ttf", 24))
    draw.text((600, 630), "YouTube & Facebook: Abhrankan Creates", fill=(192, 132, 252), font=get_font("consola.ttf", 20))

    out_p = os.path.join(out_dir, "thumbnail_episode_03_16x9.jpg")
    img.save(out_p, quality=95)
    print(f"✅ Landscape cover: {out_p}")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_keyframes(repo_dir)
    create_vertical_poster(repo_dir)
    create_landscape_cover(repo_dir)

if __name__ == "__main__":
    main()
