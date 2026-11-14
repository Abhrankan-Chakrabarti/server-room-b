"""
Server Room B - 15-Second High-Octane Hype Teaser
Designed for Facebook Stories, Instagram Reels, and YouTube Shorts.
Hook: "Dropping This Sunday on Abhrankan Creates"
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio_ffmpeg

def generate_teaser_audio(out_wav, total_duration=15.0, sample_rate=44100):
    total_samples = int(total_duration * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)
    
    # 0s - 3s: Ambient fan hum
    hum = 0.18 * np.sin(2 * np.pi * 58 * t) + 0.08 * np.sin(2 * np.pi * 116 * t)
    audio += hum
    
    # 3s: Sudden sub drop & silence
    idx_3 = int(3.0 * sample_rate)
    t_d = np.linspace(0, 1.5, int(1.5 * sample_rate))
    audio[idx_3:idx_3+len(t_d)] += 0.35 * np.sin(2 * np.pi * (120 - 40 * t_d) * t_d) * np.exp(-t_d * 2.5)
    
    # 6s: Alarm pulse
    idx_6 = int(6.0 * sample_rate)
    t_a = np.linspace(0, 2.5, int(2.5 * sample_rate))
    audio[idx_6:idx_6+len(t_a)] += 0.25 * np.sin(2 * np.pi * 880 * t_a) * (np.sin(2 * np.pi * 4 * t_a) > 0)
    
    # 9s - 12.5s: Glitch riser & 2ms stutter burst
    idx_9 = int(9.0 * sample_rate)
    riser_len = int(3.5 * sample_rate)
    t_r = np.linspace(0, 3.5, riser_len)
    chirp = 0.30 * np.sin(2 * np.pi * (200 + 180 * (t_r**2)) * t_r)
    # Stutter gate
    gate = ((np.arange(riser_len) % int(0.004 * sample_rate)) < int(0.002 * sample_rate)).astype(np.float32)
    audio[idx_9:idx_9+riser_len] += chirp * gate + 0.15 * (np.random.rand(riser_len) * 2 - 1) * gate
    
    # 12.5s: Heavy cinematic impact thud
    idx_12 = int(12.5 * sample_rate)
    thud_len = int(2.2 * sample_rate)
    t_th = np.linspace(0, 2.2, thud_len)
    audio[idx_12:idx_12+thud_len] += 0.50 * np.sin(2 * np.pi * 45 * t_th) * np.exp(-t_th * 1.8)
    
    audio = np.clip(audio, -0.92, 0.92)
    int_data = (audio * 32767).astype(np.int16)
    
    with open(out_wav, "wb") as f:
        import wave
        wf = wave.open(f, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_data.tobytes())
        wf.close()

def render_teaser_video(out_raw_video, width=720, height=1280, fps=30, total_duration=15):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))
    
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kling_dir = os.path.join(repo_dir, "episodes", "kling_renders")
    
    # Load sample scene clips
    clip_files = {
        "corridor": os.path.join(kling_dir, "scene_01.mp4"),
        "terminal": os.path.join(kling_dir, "scene_04.mp4"),
        "compiler": os.path.join(kling_dir, "scene_07.mp4"),
        "eye": os.path.join(kling_dir, "scene_08.mp4"),
        "hand": os.path.join(kling_dir, "scene_11.mp4"),
        "void": os.path.join(kling_dir, "scene_13.mp4"),
        "strobe": os.path.join(kling_dir, "scene_14.mp4")
    }
    
    caps = {}
    for k, v in clip_files.items():
        if os.path.exists(v):
            caps[k] = cv2.VideoCapture(v)
            
    try:
        font_hook = ImageFont.truetype("arialbd.ttf", 44)
        font_main = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
        font_credit = ImageFont.truetype("arial.ttf", 22)
    except:
        font_hook = font_main = font_sub = font_credit = ImageFont.load_default()
        
    for f in range(total_frames):
        t = f / fps
        cx, cy = width // 2, height // 2
        
        # Timeline Beats:
        # 0.0 - 3.0s: Corridor
        # 3.0 - 6.0s: Terminal Stream
        # 6.0 - 9.0s: Biological Compiler Alert
        # 9.0 - 9.7s: Hand trail glitch
        # 9.7 - 10.4s: The Void
        # 10.4 - 11.2s: Eye macro glitch
        # 11.2 - 12.3s: Strobe flash
        # 12.3 - 15.0s: TITLE & DROPPING THIS SUNDAY
        
        active_key = "corridor"
        if 3.0 <= t < 6.0:
            active_key = "terminal"
        elif 6.0 <= t < 9.0:
            active_key = "compiler"
        elif 9.0 <= t < 9.7:
            active_key = "hand"
        elif 9.7 <= t < 10.4:
            active_key = "void"
        elif 10.4 <= t < 11.2:
            active_key = "eye"
        elif 11.2 <= t < 12.3:
            active_key = "strobe"
        elif t >= 12.3:
            active_key = "title"
            
        if active_key in caps and active_key != "title":
            cap = caps[active_key]
            total_c_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 100
            cap.set(cv2.CAP_PROP_POS_FRAMES, f % total_c_frames)
            ret, frame = cap.read()
            if ret:
                if (frame.shape[1], frame.shape[0]) != (width, height):
                    frame = cv2.resize(frame, (width, height))
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                img = Image.new("RGB", (width, height), (3, 7, 18))
        else:
            img = Image.new("RGB", (width, height), (2, 6, 23))
            
        draw = ImageDraw.Draw(img, "RGBA")
        
        # Text Overlays
        if t < 3.0:
            # Beat 1
            draw.rectangle([(60, int(height * 0.76)), (width - 60, int(height * 0.86))], fill=(0, 0, 0, 220), outline=(56, 189, 248), width=2)
            draw.text((cx, int(height * 0.81)), "AT 03:14 AM...", fill=(255, 255, 255), font=font_hook, anchor="mm")
            
        elif 3.0 <= t < 6.0:
            # Beat 2
            draw.rectangle([(40, int(height * 0.76)), (width - 40, int(height * 0.86))], fill=(0, 0, 0, 225), outline=(234, 179, 8), width=2)
            draw.text((cx, int(height * 0.81)), "AN IMPOSSIBLE PACKET APPEARED", fill=(234, 179, 8), font=font_sub, anchor="mm")
            
        elif 6.0 <= t < 9.0:
            # Beat 3
            draw.rectangle([(40, int(height * 0.76)), (width - 40, int(height * 0.86))], fill=(185, 28, 28, 230), outline=(254, 202, 202), width=3)
            draw.text((cx, int(height * 0.81)), "TARGET: USER_ABHRANKAN", fill=(255, 255, 255), font=font_hook, anchor="mm")
            
        elif 9.0 <= t < 12.3:
            # Rapid Glitch Flash Overlay
            if f % 4 < 2:
                draw.rectangle([(0, 0), (width, height)], fill=(255, 255, 255, 40))
            draw.text((cx, int(height * 0.84)), "REALITY IS DECOMPILING", fill=(239, 68, 68), font=font_main, anchor="mm")
            
        else:
            # Beat 4: Title Card & Launch Date
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            
            # Glowing badge
            draw.rectangle([(cx - 240, 360), (cx + 240, 420)], fill=(185, 28, 28, 220), outline=(254, 202, 202), width=2)
            draw.text((cx, 390), "ORIGINAL SCI-FI SERIES", fill=(255, 255, 255), font=font_sub, anchor="mm")
            
            draw.text((cx, 500), "SERVER ROOM B", fill=(255, 255, 255), font=font_hook, anchor="mm")
            draw.text((cx, 560), "Chapter 1: Out of Memory", fill=(56, 189, 248), font=font_main, anchor="mm")
            
            draw.line([(cx - 260, 620), (cx + 260, 620)], fill=(56, 189, 248), width=2)
            
            # Massive Release Callout
            draw.rectangle([(60, 680), (width - 60, 770)], fill=(16, 185, 129, 230), outline=(167, 243, 208), width=3)
            draw.text((cx, 725), "DROPPING THIS SUNDAY", fill=(255, 255, 255), font=font_hook, anchor="mm")
            
            draw.text((cx, 840), "On Facebook & YouTube", fill=(234, 179, 8), font=font_main, anchor="mm")
            draw.text((cx, 900), "@AbhrankanCreates", fill=(255, 255, 255), font=font_main, anchor="mm")
            draw.text((cx, 970), "Story & Screenplay by Abhrankan Chakrabarti", fill=(148, 163, 184), font=font_credit, anchor="mm")

        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)
        
    out.release()
    for cap in caps.values():
        cap.release()
    print("Teaser frames rendered.")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    raw_video = os.path.join(repo_dir, "episodes", "temp_teaser_raw.mp4")
    teaser_audio = os.path.join(repo_dir, "audio", "teaser_15s_audio.wav")
    final_mp4 = os.path.join(repo_dir, "episodes", "chapter-01-teaser-15s.mp4")
    
    print("1/3: Generating 15s teaser sound design...")
    generate_teaser_audio(teaser_audio)
    
    print("2/3: Rendering fast-paced teaser visual frames...")
    render_teaser_video(raw_video, total_duration=15)
    
    print("3/3: Muxing teaser video & audio with FFmpeg...")
    cmd = [ffmpeg_bin, "-y", "-i", raw_video, "-i", teaser_audio, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", final_mp4]
    subprocess.run(cmd, check=True)
    
    if os.path.exists(raw_video):
        os.remove(raw_video)
        
    print(f"✓ Teaser Rendered: {final_mp4} ({os.path.getsize(final_mp4)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
