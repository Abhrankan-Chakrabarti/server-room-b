"""
Server Room B - Episode 2: Force Quit
Full 67-Second Vertical (9:16) Master Video Renderer with Synchronized Audio, Dynamic HUD & VFX.
Screenplay & Story by Abhrankan Chakrabarti.
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

def render_episode_02_video(out_raw_video, width=720, height=1280, fps=30, total_duration=67.0):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kf_dir = os.path.join(repo_dir, "episodes", "keyframes")

    # Load high-res keyframes for scenes
    kf_map = {
        1: os.path.join(kf_dir, "scene_02.jpg"),
        2: os.path.join(kf_dir, "scene_04.jpg"),
        3: os.path.join(kf_dir, "scene_07.jpg"),
        4: os.path.join(kf_dir, "scene_09.jpg"),
        5: os.path.join(kf_dir, "scene_10.jpg"),
        6: os.path.join(kf_dir, "scene_12.jpg"),
        7: os.path.join(kf_dir, "scene_14.jpg"),
        8: os.path.join(kf_dir, "scene_15.jpg")
    }

    loaded_kfs = {}
    for sc, p in kf_map.items():
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            loaded_kfs[sc] = im

    # Fallback default image
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
    # Scene 1: 0.0s - 8.4s
    # Scene 2: 8.4s - 17.6s
    # Scene 3: 17.6s - 26.5s
    # Scene 4: 26.5s - 35.4s
    # Scene 5: 35.4s - 42.6s
    # Scene 6: 42.6s - 49.7s
    # Scene 7: 49.7s - 57.3s
    # Scene 8: 57.3s - 67.0s
    segments = [
        (0.0, 8.4, 1, "PROCESS: BIOLOGICAL_COMPILER_v0x7F", "Abhrankan's reflex wasn't flight. It was to isolate the process, kill it, and reclaim the resources.", (56, 189, 248)),
        (8.4, 17.6, 2, "kill: (pid 1): Operation not permitted", "He types the kill command. The shell rejects it immediately: PID 1. You cannot kill the init process of reality.", (239, 68, 68)),
        (17.6, 26.5, 3, "SYSRQ HARDWARE INTERRUPT REMAPPED", "He forces a raw kernel reboot. Nothing. The kernel no longer answers to hardware interrupts from this side of existence.", (245, 158, 11)),
        (26.5, 35.4, 4, "WARN: PRIVILEGE DEMOTED TO RING_3", "A warning floods the room. His privilege level is demoted to userland. Physics locks to a fixed sixteen-millisecond loop.", (239, 68, 68)),
        (35.4, 42.6, 5, "TIMESTEP: 16.67ms (60 FPS FIXED)", "Time becomes quantized. The universe wasn't being haunted... the runtime itself was breaking.", (168, 85, 247)),
        (42.6, 49.7, 6, "COLLISION MESH: isTrigger = true", "Collision meshes are unloaded. He sprints and phases directly through the solid steel security door.", (56, 189, 248)),
        (49.7, 57.3, 7, "CORRIDOR SECTOR B-NORTH • Z-BUFFER COLLAPSE", "The hallway beyond is decompiling. Sodium lights flicker at sixty hertz as server racks tear through the floor.", (234, 179, 8)),
        (57.3, 67.0, 8, "COMPILING USER_ABHRANKAN... 23%", "The terminal prints: Compiling User Abhrankan, twenty-three percent. But until the build finishes, he still owns himself.", (239, 68, 68))
    ]

    print(f"🎬 Rendering {total_frames} frames ({total_duration}s @ {fps}fps)...")

    for f in range(total_frames):
        t = f / fps

        # Find active segment
        cur_seg = segments[-1]
        for seg in segments:
            if seg[0] <= t < seg[1]:
                cur_seg = seg
                break

        t_start, t_end, sc_num, badge_text, narr_text, accent_color = cur_seg
        rel_t = (t - t_start) / max(0.1, (t_end - t_start))

        # Base Image with slow camera push (zoom 1.0 -> 1.15)
        base_im = loaded_kfs.get(sc_num, default_im)
        zoom = 1.0 + rel_t * 0.12
        crop_w = int(base_im.width / zoom)
        crop_h = int(base_im.height / zoom)
        x1 = (base_im.width - crop_w) // 2
        y1 = (base_im.height - crop_h) // 2
        frame_im = base_im.crop((x1, y1, x1 + crop_w, y1 + crop_h)).resize((width, height), Image.Resampling.LANCZOS)

        # 60Hz flickering strobe effect on Scene 4, 7, 8
        if sc_num in [4, 7, 8] and (f % 4 == 0):
            frame_im = ImageEnhance.Brightness(frame_im).enhance(1.25)
        elif sc_num == 2 and rel_t > 0.4 and (f % 6 < 3):
            # Flash red on PID 1 error
            tint = Image.new("RGB", (width, height), (60, 0, 0))
            frame_im = Image.blend(frame_im, tint, 0.25)

        # Subtle scanlines
        scanlines = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(scanlines)
        for y in range(0, height, 4):
            s_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 20), width=1)
        frame_im = Image.alpha_composite(frame_im.convert("RGBA"), scanlines).convert("RGB")

        # Vignette overlays
        draw = ImageDraw.Draw(frame_im, "RGBA")
        for y in range(180):
            alpha = int(220 * (1 - y / 180))
            draw.rectangle([(0, y), (width, y + 1)], fill=(2, 4, 10, alpha))
        for y in range(960, height):
            alpha = int(245 * ((y - 960) / 320))
            draw.rectangle([(0, y), (width, y + 1)], fill=(2, 4, 10, alpha))

        # Top Header Bar
        draw.text((28, 28), "NODE SECTOR 4: SERVER ROOM B", fill=(148, 163, 184), font=font_hud)
        timecode_str = f"00:{int(t):02d}.{int((t%1)*100):02d}"
        draw.text((width - 150, 28), timecode_str, fill=(234, 179, 8), font=font_hud)

        # Top Badge Callout
        draw_centered_badge(draw, badge_text, width // 2, 85, font_badge, outline=accent_color, fill_text=accent_color)

        # Center Glitch Graphics for Scene 2 (Terminal Command)
        if sc_num == 2:
            draw.rectangle([(50, 480), (670, 600)], fill=(15, 23, 42, 230), outline=(239, 68, 68), width=2)
            draw.text((70, 500), "$ sudo kill -9 $(pgrep -f COMPILER)", fill=(255, 255, 255), font=font_hud)
            if rel_t > 0.35:
                draw.text((70, 545), "kill: (pid 1): Operation not permitted", fill=(239, 68, 68), font=font_hud)

        # Center Glitch Graphics for Scene 8 (Compilation Counter)
        if sc_num == 8:
            pct = min(23, int(rel_t * 23 * 1.5))
            draw.rectangle([(50, 480), (670, 600)], fill=(15, 23, 42, 230), outline=(239, 68, 68), width=2)
            draw.text((70, 505), "COMPILING USER_ABHRANKAN...", fill=(255, 255, 255), font=font_hud)
            draw.text((70, 550), f"BUILD PROGRESS: {pct}% [ALLOCATING BRAIN HARDWARE]", fill=(239, 68, 68), font=font_hud)

        # Subtitle & Credits Section
        if t < 65.8:
            # Bottom Subtitle & Narration Block
            lines = wrap_text(narr_text, font_narr, 620, draw)
            start_y = 1010
            for i, line in enumerate(lines):
                # Text drop shadow
                draw_centered_text(draw, line, width // 2 + 2, start_y + i * 36 + 2, font_narr, (0, 0, 0))
                draw_centered_text(draw, line, width // 2, start_y + i * 36, font_narr, (255, 255, 255))

            # Non-Overlapping Bottom Credits HUD (251px clean safety gap)
            draw.text((32, height - 44), "Story: Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit)
            chan_bbox = draw.textbbox((0, 0), "Abhrankan Creates", font=font_credit)
            chan_w = chan_bbox[2] - chan_bbox[0]
            draw.text((width - 32 - chan_w, height - 44), "Abhrankan Creates", fill=(192, 132, 252), font=font_credit)
        else:
            # Climax Blackout & Centered Credits Card (65.8s - 67.0s)
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            draw_centered_text(draw, "SERVER ROOM B", width // 2, 480, font_big, (255, 255, 255))
            draw_centered_text(draw, "Chapter 2 • Force Quit", width // 2, 540, font_narr, (234, 179, 8))
            draw_centered_badge(draw, "Story by Abhrankan Chakrabarti", width // 2, 630, font_badge, outline=(56, 189, 248), fill_text=(255, 255, 255))
            draw_centered_text(draw, "TO BE CONTINUED IN CHAPTER 3", width // 2, 720, font_badge, (234, 179, 8))
            draw_centered_text(draw, "Abhrankan Creates", width // 2, 780, font_hud, (192, 132, 252))

        # Border
        if t < 65.8:
            draw.rectangle([(10, 10), (width - 10, height - 10)], outline=(*accent_color, 120), width=2)

        # Write frame to video
        frame_cv = cv2.cvtColor(np.array(frame_im), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)

        if f % 150 == 0:
            print(f"  Frame {f}/{total_frames} ({f/total_frames*100:.1f}%) rendered...")

    out.release()
    print("✅ Raw video frames rendered successfully!")

def multiplex_audio_and_video(repo_dir, raw_vid, out_mp4):
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    audio_wav = os.path.join(repo_dir, "audio", "episode_02_soundtrack.wav")

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

    raw_vid = os.path.join(episodes_dir, "ep2_raw_temp.mp4")
    out_mp4 = os.path.join(episodes_dir, "episode-02-force-quit.mp4")

    render_episode_02_video(raw_vid)
    multiplex_audio_and_video(repo_dir, raw_vid, out_mp4)

if __name__ == "__main__":
    main()
