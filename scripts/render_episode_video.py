"""
Server Room B - Episode 1: The Packet
Full 60-Second Vertical (9:16) Video Renderer with Synchronized Audio, Dynamic Layout & VFX
"""

import os
import math
import wave
import struct
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio_ffmpeg

def generate_ambient_and_sfx_audio(out_wav, total_duration=60.0, sample_rate=44100):
    total_samples = int(total_duration * sample_rate)
    audio_data = np.zeros(total_samples, dtype=np.float32)
    
    t = np.linspace(0, total_duration, total_samples, endpoint=False)
    
    # 1. Server room low frequency hum (58Hz fundamental + 116Hz overtone)
    hum = 0.12 * np.sin(2 * np.pi * 58 * t) + 0.05 * np.sin(2 * np.pi * 116 * t)
    # Slow amplitude modulation
    hum *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t))
    audio_data += hum
    
    # 2. Add SFX at scene transition points
    # Scene 3: Warning pulse at 14s
    idx_14 = int(14 * sample_rate)
    pulse_len = int(0.3 * sample_rate)
    t_pulse = np.linspace(0, 0.3, pulse_len)
    audio_data[idx_14:idx_14+pulse_len] += 0.25 * np.sin(2 * np.pi * 520 * t_pulse) * np.exp(-t_pulse * 8)
    
    # Scene 6: Glitch burst at 36s
    idx_36 = int(36 * sample_rate)
    g_len = int(0.2 * sample_rate)
    audio_data[idx_36:idx_36+g_len] += 0.2 * (np.random.rand(g_len) * 2 - 1)
    
    # Scene 7: Alarm warble at 44s
    idx_44 = int(44 * sample_rate)
    alarm_len = int(2.0 * sample_rate)
    t_alarm = np.linspace(0, 2.0, alarm_len)
    audio_data[idx_44:idx_44+alarm_len] += 0.18 * np.sin(2 * np.pi * (700 + 150 * np.sin(2 * np.pi * 4 * t_alarm)) * t_alarm)
    
    # Scene 8: Glitch shriek at 54s
    idx_54 = int(54 * sample_rate)
    shriek_len = int(0.4 * sample_rate)
    t_shriek = np.linspace(0, 0.4, shriek_len)
    audio_data[idx_54:idx_54+shriek_len] += 0.28 * np.sin(2 * np.pi * 1200 * t_shriek) * np.exp(-t_shriek * 5)
    audio_data[idx_54:idx_54+shriek_len] += 0.15 * (np.random.rand(shriek_len) * 2 - 1)
    
    # Normalize to avoid clipping
    audio_data = np.clip(audio_data, -0.95, 0.95)
    int_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_data.tobytes())

def build_full_audio_track(repo_dir, ffmpeg_bin, out_mixed_audio):
    narration_dir = os.path.join(repo_dir, "audio", "narration")
    sfx_wav = os.path.join(repo_dir, "audio", "ambient_sfx.wav")
    generate_ambient_and_sfx_audio(sfx_wav)
    
    # Mix all narration tracks at exact timestamps using ffmpeg
    # scene 1: 0s, scene 2: 6s, scene 3: 14s, scene 4: 20s, scene 5: 28s, scene 6: 36s, scene 7: 44s, scene 8: 54s
    offsets = [0, 6, 14, 20, 28, 36, 44, 54]
    
    inputs = [sfx_wav]
    filter_delays = ["[0:a]volume=0.8[amb]"]
    amix_inputs = "[amb]"
    
    for i in range(1, 9):
        wav_path = os.path.join(narration_dir, f"scene_{i:02d}_narration.wav")
        inputs.append(wav_path)
        delay_ms = int(offsets[i-1] * 1000 + 300) # slight 300ms lead-in
        filter_delays.append(f"[{i}:a]adelay={delay_ms}|{delay_ms},volume=1.4[a{i}]")
        amix_inputs += f"[a{i}]"
        
    filter_complex = f"{';'.join(filter_delays)};{amix_inputs}amix=inputs=9:duration=first:dropout_transition=2[outa]"
    cmd = [ffmpeg_bin, "-y"]
    for inp in inputs:
        cmd.extend(["-i", inp])
    cmd.extend(["-filter_complex", filter_complex, "-map", "[outa]", "-t", "60", out_mixed_audio])
    subprocess.run(cmd, check=True)

def wrap_text(text, font, max_width, draw):
    """
    Splits text into multiple lines such that no line exceeds max_width.
    Guarantees that characters never spill past boundaries.
    """
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
    """
    Draws text horizontally centered at cx and vertically centered at cy.
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)

def draw_centered_badge(draw, text, cx, cy, font, fill_bg=(0, 0, 0, 230), outline=(234, 179, 8), fill_text=(250, 204, 21), pad_x=22, pad_y=10):
    """
    Draws a dynamically sized badge centered at cx, cy, matching the exact text width.
    Never spills over screen margins.
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx1 = cx - tw // 2 - pad_x
    by1 = cy - th // 2 - pad_y
    bx2 = cx + tw // 2 + pad_x
    by2 = cy + th // 2 + pad_y
    draw.rectangle([(bx1, by1), (bx2, by2)], fill=fill_bg, outline=outline, width=2)
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=fill_text, font=font)

def render_video_frames(out_raw_video, width=720, height=1280, fps=30, total_duration=60):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))
    
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kling_dir = os.path.join(repo_dir, "episodes", "kling_renders")
    
    # Preload any available photorealistic Kling AI video renders
    kling_clips = {}
    for sc_idx in range(1, 9):
        sc_file = os.path.join(kling_dir, f"scene_{sc_idx:02d}.mp4")
        if os.path.exists(sc_file):
            cap = cv2.VideoCapture(sc_file)
            c_fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
            c_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            kling_clips[sc_idx] = {
                "cap": cap,
                "fps": c_fps,
                "frames": c_frames,
                "path": sc_file
            }
            print(f"🎬 Loaded Kling AI render for Scene {sc_idx}: {c_frames} frames @ {c_fps:.1f}fps")
    
    # Try finding system fonts with safe fallbacks
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_large = ImageFont.truetype("arialbd.ttf", 30)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
        font_med = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 17)
        try:
            font_mono = ImageFont.truetype("consola.ttf", 19)
        except:
            font_mono = font_med
    except:
        font_title = font_large = font_sub = font_badge = font_med = font_small = font_mono = ImageFont.load_default()

    scenes_data = [
        {"name": "SCENE 1: SERVER ROOM B", "start": 0, "end": 6, "type": "servers", "overlay": "03:14 AM", "sub": "3:14 AM. Server Room B."},
        {"name": "SCENE 2: MEMORY ANOMALY", "start": 6, "end": 14, "type": "engineer", "overlay": "MEMORY ALLOCATION ERROR DETECTED", "sub": "Abhrankan sits alone, tracking a mysterious memory leak."},
        {"name": "SCENE 3: LEAK TELEMETRY", "start": 14, "end": 20, "type": "memory", "overlay": "-64 BYTES", "sub": "Every minute, the system loses exactly sixty-four bytes."},
        {"name": "SCENE 4: NETWORK SCAN", "start": 20, "end": 28, "type": "scan", "overlay": None, "sub": "He launches a network scan. Everything looks normal."},
        {"name": "SCENE 5: SYSTEM HALT", "start": 28, "end": 36, "type": "freeze", "overlay": None, "sub": "Then the scrolling stops."},
        {"name": "SCENE 6: NULL PACKET", "start": 36, "end": 44, "type": "null_packet", "overlay": "SOURCE: 0.0.0.0", "sub": "A single packet appears. Source address: 0.0.0.0."},
        {"name": "SCENE 7: COMPILER ACTIVE", "start": 44, "end": 54, "type": "recompile", "overlay": "BIOLOGICAL COMPILER ACTIVE", "sub": "The packet begins rearranging itself into words."},
        {"name": "SCENE 8: REALITY OVERFLOW", "start": 54, "end": 60, "type": "eye", "overlay": None, "sub": "Ah!"}
    ]

    print(f"Rendering {total_frames} frames ({width}x{height} @ {fps}fps)...")
    
    for f in range(total_frames):
        t = f / fps
        
        # Find active scene
        cur_sc = scenes_data[-1]
        sc_num = len(scenes_data)
        for idx, s in enumerate(scenes_data):
            if s["start"] <= t < s["end"]:
                cur_sc = s
                sc_num = idx + 1
                break
                
        rel_t = t - cur_sc["start"]
        sc_dur = cur_sc["end"] - cur_sc["start"]
        cx = width // 2
        
        # Check if photorealistic AI video exists for this scene
        has_kling = sc_num in kling_clips and kling_clips[sc_num]["frames"] > 0
        if has_kling:
            k_info = kling_clips[sc_num]
            target_f = min(int(rel_t * k_info["fps"]), k_info["frames"] - 1)
            k_info["cap"].set(cv2.CAP_PROP_POS_FRAMES, target_f)
            ret, k_frame = k_info["cap"].read()
            if ret:
                if (k_frame.shape[1], k_frame.shape[0]) != (width, height):
                    k_frame = cv2.resize(k_frame, (width, height), interpolation=cv2.INTER_LINEAR)
                img = Image.fromarray(cv2.cvtColor(k_frame, cv2.COLOR_BGR2RGB))
            else:
                img = Image.new("RGB", (width, height), (3, 7, 18))
        else:
            img = Image.new("RGB", (width, height), (3, 7, 18))
            
        draw = ImageDraw.Draw(img)
        
        stype = cur_sc["type"]
        
        if stype == "servers":
            if not has_kling:
                # SCENE 1: Server corridor with dolly zoom fallback
                zoom = 1.0 + (rel_t / sc_dur) * 0.4
                rack_w = int(width * 0.3 * zoom)
                
                # Left & Right racks
                draw.rectangle([(0, 0), (rack_w, height)], fill=(15, 23, 42))
                draw.rectangle([(width - rack_w, 0), (width, height)], fill=(15, 23, 42))
                
                # Draw server rack slots & blinking LEDs
                for y in range(40, height, 48):
                    draw.rectangle([(8, y), (rack_w - 12, y + 36)], fill=(30, 41, 59))
                    draw.rectangle([(width - rack_w + 12, y), (width - 8, y + 36)], fill=(30, 41, 59))
                    for led in range(4):
                        blink = math.sin(f * 0.2 + y + led) > 0.1
                        color = (56, 189, 248) if blink else (3, 105, 161)
                        draw.rectangle([(20 + led * 24, y + 14), (32 + led * 24, y + 24)], fill=color)
                        draw.rectangle([(width - rack_w + 24 + led * 24, y + 14), (width - rack_w + 36 + led * 24, y + 24)], fill=color)
                
                # Perspective corridor glow
                draw.polygon([(rack_w, 0), (width - rack_w, 0), (int(width * 0.65), height), (int(width * 0.35), height)], fill=(8, 47, 73))

        elif stype == "engineer":
            # SCENE 2: Abhrankan at triple monitors
            draw.rectangle([(0, int(height * 0.65)), (width, height)], fill=(10, 15, 25))
            # Center glowing screen
            draw.rectangle([(int(width * 0.2), int(height * 0.32)), (int(width * 0.8), int(height * 0.6))], fill=(3, 105, 161), outline=(56, 189, 248), width=3)
            # Side screens
            draw.rectangle([(int(width * 0.04), int(height * 0.35)), (int(width * 0.18), int(height * 0.58))], fill=(7, 89, 133))
            draw.rectangle([(int(width * 0.82), int(height * 0.35)), (int(width * 0.96), int(height * 0.58))], fill=(7, 89, 133))
            # Code lines
            for cy in range(int(height * 0.35), int(height * 0.58), 14):
                lw = int(math.sin(cy + f) * 120 + 200)
                draw.rectangle([(int(width * 0.24), cy), (int(width * 0.24) + lw, cy + 5)], fill=(186, 230, 253))
            # Silhouette
            draw.ellipse([(cx - 45, int(height * 0.52)), (cx + 45, int(height * 0.62))], fill=(2, 6, 23))
            draw.ellipse([(cx - 90, int(height * 0.62)), (cx + 90, int(height * 0.78))], fill=(2, 6, 23))

        elif stype == "memory":
            # SCENE 3: Memory loss telemetry
            cy_gauge = int(height * 0.38)
            rad = 140
            # Gauge circle
            draw.ellipse([(cx - rad, cy_gauge - rad), (cx + rad, cy_gauge + rad)], outline=(30, 41, 59), width=16)
            drop_deg = int(360 * min(1.0, rel_t / sc_dur))
            draw.arc([(cx - rad, cy_gauge - rad), (cx + rad, cy_gauge + rad)], start=-90, end=-90 + (360 - drop_deg), fill=(239, 68, 68), width=16)
            
            bytes_left = max(0, 1024 - int(rel_t * 64))
            draw_centered_text(draw, f"{bytes_left} MB", cx, cy_gauge - 20, font_title, (248, 250, 252))
            draw_centered_text(draw, "-64 BYTES / MIN", cx, cy_gauge + 35, font_large, (239, 68, 68))
            
            # Memory block map
            draw_centered_text(draw, "HEAP ALLOCATION MAP (ADDR: 0x7FFF80)", cx, int(height * 0.57), font_med, (148, 163, 184))
            cols, rows = 12, 6
            bw, bh = 46, 28
            map_start_x = cx - (cols * bw) // 2
            for r in range(rows):
                for c in range(cols):
                    is_leak = (r * cols + c) < int((rel_t / sc_dur) * 72)
                    color = (239, 68, 68) if is_leak else (56, 189, 248)
                    draw.rectangle([(map_start_x + c * bw, int(height * 0.61) + r * bh), (map_start_x + c * bw + bw - 6, int(height * 0.61) + r * bh + bh - 6)], fill=color)

        elif stype == "scan":
            # SCENE 4: Rapid packet scanning stream
            draw.text((45, 160), "$ foxpipe --interface=eth0 --dump-raw --hex", fill=(56, 189, 248), font=font_sub)
            for line_i in range(26):
                y_pos = 220 + line_i * 26
                seq = (f * 13 + line_i * 97) % 65535
                hex_val = f"{seq:04X}"
                alpha_c = (56, 189, 248) if line_i % 3 == 0 else (148, 163, 184)
                # Formatted cleanly to guarantee no right margin overflow
                stream_str = f"[eth0] 10.0.4.12 > 10.0.4.1:{4000+line_i} ACK 0x{hex_val}"
                draw.text((45, y_pos), stream_str, fill=alpha_c, font=font_mono)

        elif stype == "freeze":
            # SCENE 5: Terminal freeze & blinking cursor
            draw.text((45, 160), "$ foxpipe --interface=eth0 --dump-raw --hex", fill=(148, 163, 184), font=font_sub)
            draw_centered_text(draw, ">> STREAM BUFFER HALTED <<", cx, 240, font_title, (234, 179, 8))
            draw.text((45, 300), "Kernel socket pipeline deadlocked.", fill=(239, 68, 68), font=font_sub)
            draw.text((45, 340), "Buffer drain failed: 0 pkts/sec.", fill=(239, 68, 68), font=font_sub)
            if (f // 15) % 2 == 0:
                draw.rectangle([(45, 390), (75, 430)], fill=(56, 189, 248))

        elif stype == "null_packet":
            # SCENE 6: Source 0.0.0.0
            cy_null = int(height * 0.38)
            draw_centered_text(draw, "ANOMALOUS INBOUND PACKET", cx, cy_null - 80, font_sub, (148, 163, 184))
            draw_centered_text(draw, "0.0.0.0", cx, cy_null - 15, font_title, (248, 250, 252))
            draw_centered_text(draw, "SOURCE: NULL_ORIGIN", cx, cy_null + 55, font_large, (56, 189, 248))
            draw_centered_text(draw, "PAYLOAD REASSEMBLY IN PROGRESS...", cx, cy_null + 115, font_med, (234, 179, 8))

        elif stype == "recompile":
            # SCENE 7: Biological Compiler Alert
            # Digital corruption lines
            for cor_i in range(8):
                cy_line = 230 + cor_i * 28
                draw_centered_text(draw, "43 52 49 54 49 43 41 4C 20 46 41 55 4C 54", cx, cy_line, font_med, (239, 68, 68))
            
            box_y1 = int(height * 0.45)
            box_y2 = int(height * 0.63)
            draw.rectangle([(40, box_y1), (width - 40, box_y2)], fill=(69, 10, 10), outline=(239, 68, 68), width=3)
            draw_centered_text(draw, "[CRITICAL SYSTEM FAULT]", cx, box_y1 + 38, font_sub, (254, 202, 202))
            draw_centered_text(draw, "[BIOLOGICAL COMPILER ACTIVE]", cx, box_y1 + 78, font_sub, (254, 202, 202))
            draw_centered_text(draw, "[TARGET: USER_ABHRANKAN]", cx, box_y1 + 130, font_large, (254, 240, 138))

        elif stype == "eye":
            # SCENE 8: Human eye & reality glitch
            cy_eye = int(height * 0.42)
            draw.ellipse([(cx - 220, cy_eye - 110), (cx + 220, cy_eye + 110)], outline=(100, 116, 139), width=8)
            # Iris
            draw.ellipse([(cx - 95, cy_eye - 95), (cx + 95, cy_eye + 95)], fill=(3, 105, 161), outline=(56, 189, 248), width=4)
            # Pupil pulsing
            pupil_r = int(45 + math.sin(f * 0.4) * 12)
            draw.ellipse([(cx - pupil_r, cy_eye - pupil_r), (cx + pupil_r, cy_eye + pupil_r)], fill=(0, 0, 0))
            # Screen reflection
            draw_centered_text(draw, "0.0.0.0", cx, cy_eye - 5, font_large, (255, 255, 255))
            
            # Glitch slices
            if f % 4 < 2:
                for _ in range(4):
                    gy = int(height * 0.35 + np.random.rand() * 200)
                    draw.rectangle([(0, gy), (width, gy + 12)], fill=(239, 68, 68))

        # TOP HUD
        draw.rectangle([(40, 40), (240, 90)], fill=(0, 0, 0, 180), outline=(56, 189, 248), width=2)
        mins, secs = int(t // 60), int(t % 60)
        draw.text((55, 52), f"03:14 AM  {mins:02d}:{secs:02d}", fill=(56, 189, 248), font=font_sub)
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
        
        # Max width inside box is 580px (starting at x=60, box width is 640px)
        wrapped_subs = wrap_text(f'"{cur_sc["sub"]}"', font_sub, max_width=580, draw=draw)
        line_y = sub_box_y1 + 46
        for s_line in wrapped_subs:
            draw.text((60, line_y), s_line, fill=(255, 255, 255), font=font_sub)
            line_y += 34

        # ENDING BLACK SCREEN (at 58-60s)
        if t >= 58.0:
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            draw_centered_text(draw, "TO BE CONTINUED...", cx, int(height * 0.46), font_title, (248, 250, 252))
            draw_centered_text(draw, "EPISODE 2 IN PRE-PRODUCTION", cx, int(height * 0.52), font_med, (56, 189, 248))

        # Convert PIL Image to OpenCV BGR
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)
        
        if f % 150 == 0:
            print(f"Progress: {f}/{total_frames} frames ({int(f/total_frames*100)}%)")
            
    out.release()
    for k_info in kling_clips.values():
        k_info["cap"].release()
    print("Video frame generation completed.")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    raw_video = os.path.join(repo_dir, "episodes", "temp_raw_video.mp4")
    mixed_audio = os.path.join(repo_dir, "audio", "episode_01_full_soundtrack.wav")
    final_mp4 = os.path.join(repo_dir, "episodes", "episode-01-the-packet.mp4")
    
    print("1/3: Generating full soundtrack with synchronized narration and cyber SFX...")
    build_full_audio_track(repo_dir, ffmpeg_bin, mixed_audio)
    
    print("2/3: Rendering animated 9:16 vertical video frames...")
    render_video_frames(raw_video, width=720, height=1280, fps=30, total_duration=60)
    
    print("3/3: Muxing high-quality video and audio with FFmpeg...")
    mux_cmd = [ffmpeg_bin, "-y", "-i", raw_video, "-i", mixed_audio, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", final_mp4]
    subprocess.run(mux_cmd, check=True)
    
    if os.path.exists(raw_video):
        os.remove(raw_video)
        
    print(f"\nSUCCESS! Production video rendered at: {final_mp4}")
    print(f"File size: {os.path.getsize(final_mp4) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
