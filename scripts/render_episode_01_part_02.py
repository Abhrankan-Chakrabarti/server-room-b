"""
Server Room B - Episode 1 Part 2: Reality Uninstall
Full 60-Second Vertical (9:16) Video Renderer with Synchronized Audio, Dynamic Layout & VFX
Completes 100% of Chapter 1 Screenplay Adaptation.
Credit: Story by Abhrankan Chakrabarti
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio_ffmpeg

def build_part2_full_audio(repo_dir, ffmpeg_bin, out_mixed_audio):
    narration_dir = os.path.join(repo_dir, "audio", "narration_part2")
    sfx_wav = os.path.join(repo_dir, "audio", "part2_ambient_sfx.wav")
    
    # Timing spec:
    # Scene 09: 0.0s - 7.5s (offset 300ms, atempo=1.20)
    # Scene 10: 7.5s - 14.5s (offset 7700ms, atempo=1.06)
    # Scene 11: 14.5s - 22.5s (offset 14800ms, atempo=1.05)
    # Scene 12: 22.5s - 29.5s (offset 22800ms, atempo=1.18)
    # Scene 13: 29.5s - 38.0s (offset 29800ms, atempo=1.25)
    # Scene 14: 38.0s - 45.5s (offset 38300ms, atempo=1.22)
    # Scene 15: 45.5s - 53.5s (offset 45800ms, atempo=1.12)
    # Scene 16: 53.5s - 60.0s (offset 55000ms, atempo=1.00)
    
    specs = [
        (9, 300, 1.20),
        (10, 7700, 1.06),
        (11, 14800, 1.05),
        (12, 22800, 1.18),
        (13, 29800, 1.25),
        (14, 38300, 1.22),
        (15, 45800, 1.12),
        (16, 55000, 1.00),
    ]
    
    inputs = [sfx_wav]
    filter_delays = ["[0:a]volume=0.85[amb]"]
    amix_inputs = "[amb]"
    
    for idx, (sc_num, delay_ms, tempo) in enumerate(specs, start=1):
        wav_path = os.path.join(narration_dir, f"scene_{sc_num:02d}_narration.wav")
        inputs.append(wav_path)
        filter_delays.append(f"[{idx}:a]atempo={tempo},adelay={delay_ms}|{delay_ms},volume=1.45[a{idx}]")
        amix_inputs += f"[a{idx}]"
        
    filter_complex = f"{';'.join(filter_delays)};{amix_inputs}amix=inputs=9:duration=first:dropout_transition=2[outa]"
    cmd = [ffmpeg_bin, "-y"]
    for inp in inputs:
        cmd.extend(["-i", inp])
    cmd.extend(["-filter_complex", filter_complex, "-map", "[outa]", "-t", "60", out_mixed_audio])
    subprocess.run(cmd, check=True)
    print(f"Full mixed audio created at: {out_mixed_audio}")

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

def draw_centered_badge(draw, text, cx, cy, font, fill_bg=(0, 0, 0, 230), outline=(234, 179, 8), fill_text=(250, 204, 21), pad_x=22, pad_y=10):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx1 = cx - tw // 2 - pad_x
    by1 = cy - th // 2 - pad_y
    bx2 = cx + tw // 2 + pad_x
    by2 = cy + th // 2 + pad_y
    draw.rectangle([(bx1, by1), (bx2, by2)], fill=fill_bg, outline=outline, width=2)
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=fill_text, font=font)

def render_part2_video_frames(out_raw_video, width=720, height=1280, fps=30, total_duration=60):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))
    
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kling_dir = os.path.join(repo_dir, "episodes", "kling_renders")
    
    clips = {}
    for sc_idx in range(9, 17):
        sc_file = os.path.join(kling_dir, f"scene_{sc_idx:02d}.mp4")
        if os.path.exists(sc_file):
            cap = cv2.VideoCapture(sc_file)
            c_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            c_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            clips[sc_idx] = {
                "cap": cap,
                "fps": c_fps,
                "frames": c_frames,
                "path": sc_file
            }
            print(f"🎬 Loaded Scene {sc_idx}: {c_frames} frames @ {c_fps:.1f}fps")
            
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_large = ImageFont.truetype("arialbd.ttf", 29)
        font_sub = ImageFont.truetype("arialbd.ttf", 25)
        font_badge = ImageFont.truetype("arialbd.ttf", 21)
        font_med = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 17)
        try:
            font_mono = ImageFont.truetype("consola.ttf", 18)
        except:
            font_mono = font_med
    except:
        font_title = font_large = font_sub = font_badge = font_med = font_small = font_mono = ImageFont.load_default()

    scenes_data = [
        {"name": "SCENE 9: THE ACOUSTIC STUTTER", "start": 0.0, "end": 7.5, "num": 9, "overlay": "TIMESTEP: 2.00ms FIXED", "sub": "The server hum has changed. Instead of a smooth mechanical drone, it now stutters like a broken audio file."},
        {"name": "SCENE 10: TACTILE DELAY", "start": 7.5, "end": 14.5, "num": 10, "overlay": "INPUT LATENCY: +47ms", "sub": "Abhrankan slowly rises from his chair. He reaches for his phone... and freezes."},
        {"name": "SCENE 11: GEOMETRIC HAND CASCADE", "start": 14.5, "end": 22.5, "num": 11, "overlay": "ARTIFACT ACCUMULATION", "sub": "Behind his hand hangs a trail. Not motion blur, but solid frozen copies lingering in the air."},
        {"name": "SCENE 12: KEYPAD LOG OVERFLOW", "start": 22.5, "end": 29.5, "num": 12, "overlay": "LOG STREAM: SECTOR 4", "sub": "The security keypad isn't asking for a passcode anymore. It races through endless system messages."},
        {"name": "SCENE 13: THE VOID & MESH CLIPPING", "start": 29.5, "end": 38.0, "num": 13, "overlay": "COLLISION MESH UNLOADED", "sub": "The wall flickers, vanishing into an infinite black void. The universe wasn't being haunted. It was being uninstalled."},
        {"name": "SCENE 14: VIOLENT MONITOR STROBE", "start": 38.0, "end": 45.5, "num": 14, "overlay": "SECTOR 4 DECOMPILING", "sub": "A deep rumble shakes the room. His workstation monitor flashes violently, casting a blinding strobe pattern."},
        {"name": "SCENE 15: BIOLOGICAL HOST DETECTED", "start": 45.5, "end": 53.5, "num": 15, "overlay": "BIOLOGICAL HOST: USER_ABHRANKAN", "sub": "The terminal is compiling a new process. And the hardware it's using to build it... is Abhrankan's own brain."},
        {"name": "SCENE 16: CUT TO BLACK & CREDITS", "start": 53.5, "end": 60.0, "num": 16, "overlay": None, "sub": "TO BE CONTINUED."}
    ]

    print(f"Rendering {total_frames} frames ({width}x{height} @ {fps}fps)...")
    
    for f in range(total_frames):
        t = f / fps
        
        cur_sc = scenes_data[-1]
        for s in scenes_data:
            if s["start"] <= t < s["end"]:
                cur_sc = s
                break
                
        sc_num = cur_sc["num"]
        rel_t = t - cur_sc["start"]
        cx = width // 2
        
        # Load frame from 2.5D video clip
        has_clip = sc_num in clips and clips[sc_num]["frames"] > 0
        if has_clip:
            c_info = clips[sc_num]
            target_f = min(int(rel_t * c_info["fps"]), c_info["frames"] - 1)
            c_info["cap"].set(cv2.CAP_PROP_POS_FRAMES, target_f)
            ret, k_frame = c_info["cap"].read()
            if ret:
                if (k_frame.shape[1], k_frame.shape[0]) != (width, height):
                    k_frame = cv2.resize(k_frame, (width, height), interpolation=cv2.INTER_LINEAR)
                img = Image.fromarray(cv2.cvtColor(k_frame, cv2.COLOR_BGR2RGB))
            else:
                img = Image.new("RGB", (width, height), (3, 7, 18))
        else:
            img = Image.new("RGB", (width, height), (3, 7, 18))
            
        draw = ImageDraw.Draw(img)
        
        # TOP HUD
        draw.rectangle([(40, 40), (270, 90)], fill=(0, 0, 0, 190), outline=(56, 189, 248), width=2)
        mins, secs = int(t // 60), int(t % 60)
        draw.text((55, 52), f"03:15 AM  {mins:02d}:{secs:02d}", fill=(56, 189, 248), font=font_sub)
        draw.text((width - 190, 52), "REC ● 60s", fill=(239, 68, 68), font=font_sub)
        
        # ACTIVE SCENE BADGE (Left top)
        draw.text((45, 108), cur_sc["name"], fill=(148, 163, 184), font=font_med)

        # DYNAMIC CENTERED OVERLAY BADGE
        if cur_sc["overlay"]:
            draw_centered_badge(draw, cur_sc["overlay"], cx=cx, cy=int(height * 0.74), font=font_badge)

        # SUBTITLES (BOTTOM) WITH AUTOMATIC WORD-WRAPPING
        sub_box_y1 = int(height * 0.81)
        sub_box_y2 = int(height * 0.95)
        draw.rectangle([(40, sub_box_y1), (width - 40, sub_box_y2)], fill=(10, 15, 30), outline=(56, 189, 248), width=2)
        draw.text((60, sub_box_y1 + 14), "NARRATION:", fill=(148, 163, 184), font=font_small)
        
        wrapped_subs = wrap_text(f'"{cur_sc["sub"]}"', font_sub, max_width=580, draw=draw)
        line_y = sub_box_y1 + 46
        for s_line in wrapped_subs:
            draw.text((60, line_y), s_line, fill=(255, 255, 255), font=font_sub)
            line_y += 34

        # ENDING BLACKOUT & CREDITS (56.0s - 60.0s)
        if t >= 56.0:
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            draw_centered_text(draw, "SERVER ROOM B", cx, int(height * 0.38), font_title, (248, 250, 252))
            draw_centered_text(draw, "Chapter 1: Out of Memory", cx, int(height * 0.44), font_sub, (148, 163, 184))
            
            # AUTHOR & CREATOR CREDIT
            draw_centered_badge(draw, "Story by Abhrankan Chakrabarti", cx=cx, cy=int(height * 0.52), font=font_large, outline=(56, 189, 248), fill_text=(255, 255, 255))
            
            draw_centered_text(draw, "TO BE CONTINUED...", cx, int(height * 0.61), font_title, (234, 179, 8))
            draw_centered_text(draw, "Episode 2: Force Quit — Coming Soon", cx, int(height * 0.67), font_med, (56, 189, 248))

        # Convert PIL Image to OpenCV BGR
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)
        
        if f % 150 == 0:
            print(f"Progress: {f}/{total_frames} frames ({int(f/total_frames*100)}%)")
            
    out.release()
    for c_info in clips.values():
        c_info["cap"].release()
    print("Part 2 video frame generation completed.")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    raw_video = os.path.join(repo_dir, "episodes", "temp_part2_raw_video.mp4")
    mixed_audio = os.path.join(repo_dir, "audio", "episode_01_part_02_soundtrack.wav")
    final_mp4 = os.path.join(repo_dir, "episodes", "episode-01-part-02.mp4")
    
    print("1/3: Generating Part 2 soundtrack with narration, 2ms acoustic stutter & SFX...")
    build_part2_full_audio(repo_dir, ffmpeg_bin, mixed_audio)
    
    print("2/3: Rendering Part 2 9:16 vertical video frames...")
    render_part2_video_frames(raw_video, width=720, height=1280, fps=30, total_duration=60)
    
    print("3/3: Muxing high-quality video and audio with FFmpeg...")
    mux_cmd = [ffmpeg_bin, "-y", "-i", raw_video, "-i", mixed_audio, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", final_mp4]
    subprocess.run(mux_cmd, check=True)
    
    if os.path.exists(raw_video):
        os.remove(raw_video)
        
    print(f"\nSUCCESS! Production video rendered at: {final_mp4}")
    print(f"File size: {os.path.getsize(final_mp4) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
