"""
Server Room B - Episode 3: Link Stage
Full 78-Second Vertical (9:16) Master Video Renderer with Synchronized Audio, Dynamic HUD & VFX.
Screenplay & Story by Abhrankan Chakrabarti.
Channel: Abhrankan Creates
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import cv2
import imageio_ffmpeg

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_centered_text(draw, text, cx, cy, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)

def draw_centered_badge(draw, text, cx, cy, font, fill_bg=(0, 0, 0, 235), outline=(234, 179, 8), fill_text=(250, 204, 21), pad_x=20, pad_y=8):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx1 = cx - tw // 2 - pad_x
    by1 = cy - th // 2 - pad_y
    bx2 = cx + tw // 2 + pad_x
    by2 = cy + th // 2 + pad_y
    draw.rectangle([(bx1, by1), (bx2, by2)], fill=fill_bg, outline=outline, width=2)
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=fill_text, font=font)

def render_episode_03_video(out_raw_video, width=720, height=1280, fps=30, total_duration=78.0):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")

    # Load high-res keyframes for scenes
    kf_map = {
        1: os.path.join(kf_dir, "scene_17.jpg"),
        2: os.path.join(kf_dir, "scene_18.jpg"),
        3: os.path.join(kf_dir, "scene_19.jpg"),
        4: os.path.join(kf_dir, "scene_20.jpg"),
        5: os.path.join(kf_dir, "scene_21.jpg"),
        6: os.path.join(kf_dir, "scene_22.jpg"),
        7: os.path.join(kf_dir, "scene_23.jpg"),
        8: os.path.join(kf_dir, "scene_24.jpg")
    }

    loaded_kfs = {}
    for sc, p in kf_map.items():
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            loaded_kfs[sc] = im

    default_im = Image.new("RGB", (width, height), (5, 5, 12))

    try:
        font_hud = ImageFont.truetype("consola.ttf", 22)
        font_credit = ImageFont.truetype("consola.ttf", 17)
        font_narr = ImageFont.truetype("arialbd.ttf", 28)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_big = ImageFont.truetype("arialbd.ttf", 44)
    except:
        font_hud = font_credit = font_narr = font_badge = font_big = ImageFont.load_default()

    # Timeline segments:
    # Scene 1: 0.0s - 9.0s
    # Scene 2: 9.0s - 18.8s
    # Scene 3: 18.8s - 28.6s
    # Scene 4: 28.6s - 38.0s
    # Scene 5: 38.0s - 47.6s
    # Scene 6: 47.6s - 57.2s
    # Scene 7: 57.2s - 66.8s
    # Scene 8: 66.8s - 78.0s
    segments = [
        (0.0, 9.0, 1, "TOPOLOGY: CIRCULAR_BUFFER_0x03", "The corridor didn't end; it looped. With every pass, the walls rendered at lower resolution as the system ran out of memory.", (56, 189, 248)),
        (9.0, 18.8, 2, "COMPILING USER_ABHRANKAN... 41%", "Compiling User Abhrankan, forty-one percent. The text no longer printed on the monitors. It burned directly into his retina.", (74, 222, 128)),
        (18.8, 28.6, 3, "NODE: MDF-CORE-SW01 (BARE METAL)", "He breaks into the Main Distribution Frame. Here, the core Cisco backbone switch is still running on bare metal, untouched by the compiler.", (234, 179, 8)),
        (28.6, 38.0, 4, "screen /dev/ttyUSB0 115200", "Latency spikes to one hundred and fifty milliseconds. He plugs into the serial console as the exit behind him completely vanishes.", (56, 189, 248)),
        (38.0, 47.6, 5, "COLOR_DEPTH: 8-BIT_VGA_PALETTE", "Sixty-seven percent. His vision drops from true color to harsh eight-bit VGA. The compiler begins overwriting his memories.", (239, 68, 68)),
        (47.6, 57.2, 6, "deny ip host 0.0.0.0 any", "His left arm locks in a rigid spasm as foreign drivers load into his nerves. With one hand, he writes a hardware access control list.", (239, 68, 68)),
        (57.2, 66.8, 7, "TIMESTEP: 0.00ms [CLOCK HALT]", "Eighty-nine percent. He binds the firewall and strikes Enter. The fans die. Time freezes to zero milliseconds.", (234, 179, 8)),
        (66.8, 78.0, 8, "%ACL-I-APPLIED: Connection reset", "Connection reset by peer. The packet is dropped. But the doorway returns misaligned by three inches. The bug in reality remains.", (74, 222, 128))
    ]

    print(f"🎬 Rendering {total_frames} frames ({total_duration}s @ {fps}fps)...")

    for f in range(total_frames):
        t = f / fps

        # Find current segment
        cur_seg = segments[-1]
        for seg in segments:
            if seg[0] <= t < seg[1]:
                cur_seg = seg
                break

        t_start, t_end, sc_num, badge_text, narr_text, accent_color = cur_seg
        rel_t = (t - t_start) / (t_end - t_start)

        # Base Image with slow zoom
        base_im = loaded_kfs.get(sc_num, default_im)
        zoom = 1.0 + rel_t * 0.05
        new_w = int(width * zoom)
        new_h = int(height * zoom)
        resized = base_im.resize((new_w, new_h), Image.Resampling.BILINEAR)

        x_crop = (new_w - width) // 2
        y_crop = (new_h - height) // 2
        frame_im = resized.crop((x_crop, y_crop, x_crop + width, y_crop + height))

        # Chromatic & glitch tint
        if sc_num in [2, 5, 7] and (f % 18 < 3):
            tint = Image.new("RGB", (width, height), (accent_color[0] // 3, accent_color[1] // 3, accent_color[2] // 3))
            frame_im = Image.blend(frame_im, tint, 0.22)

        # Scanlines
        scanlines = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(scanlines)
        for y in range(0, height, 4):
            s_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 18), width=1)
        frame_im = Image.alpha_composite(frame_im.convert("RGBA"), scanlines).convert("RGB")

        # Vignette overlays
        draw = ImageDraw.Draw(frame_im, "RGBA")
        for y in range(180):
            alpha = int(220 * (1 - y / 180))
            draw.rectangle([(0, y), (width, y + 1)], fill=(2, 4, 10, alpha))
        for y in range(960, height):
            alpha = int(245 * ((y - 960) / 320))
            draw.rectangle([(0, y), (width, y + 1)], fill=(2, 4, 10, alpha))

        if t < 76.5:
            # Top Header Bar
            draw.text((28, 28), "MDF-CORE-SW01: GIGABITETHERNET0/1", fill=(148, 163, 184), font=font_hud)
            timecode_str = f"00:{int(t):02d}.{int((t%1)*100):02d}"
            draw.text((width - 150, 28), timecode_str, fill=(234, 179, 8), font=font_hud)

            # Top Badge Callout
            draw_centered_badge(draw, badge_text, width // 2, 85, font_badge, outline=accent_color, fill_text=accent_color)

            # Center Glitch Graphics for Scene 6 (Cisco ACL injection)
            if sc_num == 6:
                draw.rectangle([(50, 480), (670, 600)], fill=(15, 23, 42, 230), outline=(239, 68, 68), width=2)
                draw.text((70, 500), "MDF-CORE-SW01(config)# ip access-list BLOCK_COMPILER", fill=(255, 255, 255), font=font_hud)
                draw.text((70, 545), "  deny ip host 0.0.0.0 any", fill=(239, 68, 68), font=font_hud)

            # Center Glitch Graphics for Scene 7 (0ms Freeze)
            if sc_num == 7:
                draw.rectangle([(50, 480), (670, 600)], fill=(15, 23, 42, 230), outline=(234, 179, 8), width=2)
                draw.text((70, 505), "TIMESTEP: 0.00ms [SPACETIME HALTED]", fill=(234, 179, 8), font=font_hud)
                draw.text((70, 550), "COMPILING USER_ABHRANKAN... 89%", fill=(239, 68, 68), font=font_hud)

            # Bottom Subtitle & Narration Block
            lines = wrap_text(narr_text, font_narr, 620, draw)
            start_y = 1010
            for i, line in enumerate(lines):
                draw_centered_text(draw, line, width // 2 + 2, start_y + i * 36 + 2, font_narr, (0, 0, 0))
                draw_centered_text(draw, line, width // 2, start_y + i * 36, font_narr, (255, 255, 255))

            # Non-Overlapping Bottom Credits HUD
            draw.text((32, height - 44), "Story: Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit)
            chan_bbox = draw.textbbox((0, 0), "Abhrankan Creates", font=font_credit)
            chan_w = chan_bbox[2] - chan_bbox[0]
            draw.text((width - 32 - chan_w, height - 44), "Abhrankan Creates", fill=(192, 132, 252), font=font_credit)

            # Border
            draw.rectangle([(10, 10), (width - 10, height - 10)], outline=(*accent_color, 120), width=2)

        else:
            # Climax Blackout & Centered Credits Card (76.5s - 78.0s)
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            draw_centered_text(draw, "SERVER ROOM B", width // 2, 480, font_big, (255, 255, 255))
            draw_centered_text(draw, "Chapter 3 • Link Stage", width // 2, 540, font_narr, (234, 179, 8))
            draw_centered_badge(draw, "Story by Abhrankan Chakrabarti", width // 2, 630, font_badge, outline=(56, 189, 248), fill_text=(255, 255, 255))
            draw_centered_text(draw, "TO BE CONTINUED IN CHAPTER 4", width // 2, 720, font_badge, (234, 179, 8))
            draw_centered_text(draw, "Abhrankan Creates", width // 2, 780, font_hud, (192, 132, 252))

        # Write frame to video
        frame_cv = cv2.cvtColor(np.array(frame_im), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)

        if f % 180 == 0:
            print(f"  Frame {f}/{total_frames} ({f/total_frames*100:.1f}%) rendered...")

    out.release()
    print("✅ Raw video frames rendered successfully!")

def multiplex_audio_and_video(repo_dir, raw_vid, out_mp4):
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    audio_wav = os.path.join(repo_dir, "audio", "episode_03_soundtrack.wav")

    cmd = [
        ffmpeg_bin, "-y",
        "-i", raw_vid,
        "-i", audio_wav,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    print(f"🎬 Multiplexing audio and video into final master: {out_mp4}...")
    subprocess.run(cmd, check=True)
    if os.path.exists(raw_vid):
        os.remove(raw_vid)
    print(f"🎉 Master Video Ready: {out_mp4} ({os.path.getsize(out_mp4)/(1024*1024):.2f} MB)")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    episodes_dir = os.path.join(repo_dir, "episodes")
    os.makedirs(episodes_dir, exist_ok=True)

    raw_vid = os.path.join(episodes_dir, "ep3_raw_temp.mp4")
    final_mp4 = os.path.join(episodes_dir, "episode-03-link-stage.mp4")

    render_episode_03_video(raw_vid, width=720, height=1280, fps=30, total_duration=78.0)
    multiplex_audio_and_video(repo_dir, raw_vid, final_mp4)

if __name__ == "__main__":
    main()
