"""
Server Room B - Episode 1: The Packet
Full 60-Second Vertical (9:16) Video Renderer with Synchronized Audio & VFX
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

def render_video_frames(out_raw_video, width=720, height=1280, fps=30, total_duration=60):
    total_frames = int(fps * total_duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_raw_video, fourcc, fps, (width, height))
    
    # Try finding system font
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_med = ImageFont.truetype("arial.ttf", 26)
        font_bold = ImageFont.truetype("arialbd.ttf", 32)
        font_title = ImageFont.truetype("arialbd.ttf", 44)
    except:
        font_large = font_med = font_bold = font_title = ImageFont.load_default()

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
        for s in scenes_data:
            if s["start"] <= t < s["end"]:
                cur_sc = s
                break
                
        rel_t = t - cur_sc["start"]
        sc_dur = cur_sc["end"] - cur_sc["start"]
        
        img = Image.new("RGB", (width, height), (3, 7, 18))
        draw = ImageDraw.Draw(img)
        
        stype = cur_sc["type"]
        
        if stype == "servers":
            # SCENE 1: Server corridor with dolly zoom
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
            cx = int(width * 0.5)
            draw.ellipse([(cx - 45, int(height * 0.52)), (cx + 45, int(height * 0.62))], fill=(2, 6, 23))
            draw.ellipse([(cx - 90, int(height * 0.62)), (cx + 90, int(height * 0.78))], fill=(2, 6, 23))

        elif stype == "memory":
            # SCENE 3: Memory loss telemetry
            cx, cy = int(width * 0.5), int(height * 0.38)
            rad = 140
            # Gauge circle
            draw.ellipse([(cx - rad, cy - rad), (cx + rad, cy + rad)], outline=(30, 41, 59), width=16)
            drop_deg = int(360 * min(1.0, rel_t / sc_dur))
            draw.arc([(cx - rad, cy - rad), (cx + rad, cy + rad)], start=-90, end=-90 + (360 - drop_deg), fill=(239, 68, 68), width=16)
            
            bytes_left = max(0, 1024 - int(rel_t * 64))
            draw.text((cx - 80, cy - 25), f"{bytes_left} MB", fill=(248, 250, 252), font=font_title)
            draw.text((cx - 100, cy + 35), "-64 BYTES / MIN", fill=(239, 68, 68), font=font_bold)
            
            # Memory block map
            draw.text((60, int(height * 0.58)), "HEAP FRAGMENTATION (ADDR: 0x7FFF80)", fill=(148, 163, 184), font=font_med)
            cols, rows = 12, 6
            bw, bh = 48, 30
            for r in range(rows):
                for c in range(cols):
                    is_leak = (r * cols + c) < int((rel_t / sc_dur) * 72)
                    color = (239, 68, 68) if is_leak else (56, 189, 248)
                    draw.rectangle([(60 + c * bw, int(height * 0.62) + r * bh), (60 + c * bw + bw - 6, int(height * 0.62) + r * bh + bh - 6)], fill=color)

        elif stype == "scan":
            # SCENE 4: Rapid packet scanning stream
            draw.text((40, 160), "$ foxpipe --interface=eth0 --dump-raw --hex", fill=(56, 189, 248), font=font_bold)
            for line_i in range(28):
                y_pos = 230 + line_i * 28
                seq = (f * 13 + line_i * 97) % 65535
                hex_val = f"{seq:04X}"
                alpha_c = (56, 189, 248) if line_i % 3 == 0 else (148, 163, 184)
                draw.text((40, y_pos), f"[eth0] IP 10.0.4.12:8080 > 10.0.4.1:{40000+line_i} ACK 0x{hex_val}", fill=alpha_c, font=font_med)

        elif stype == "freeze":
            # SCENE 5: Terminal freeze & blinking cursor
            draw.text((40, 160), "$ foxpipe --interface=eth0 --dump-raw --hex", fill=(148, 163, 184), font=font_bold)
            draw.text((40, 230), ">> STREAM BUFFER HALTED <<", fill=(234, 179, 8), font=font_title)
            draw.text((40, 310), "Kernel socket pipeline deadlocked. 0 pkts/sec.", fill=(239, 68, 68), font=font_bold)
            if (f // 15) % 2 == 0:
                draw.rectangle([(40, 380), (70, 425)], fill=(56, 189, 248))

        elif stype == "null_packet":
            # SCENE 6: Source 0.0.0.0
            cx, cy = int(width * 0.5), int(height * 0.38)
            draw.text((cx - 160, cy - 80), "ANOMALOUS INBOUND PACKET", fill=(148, 163, 184), font=font_bold)
            draw.text((cx - 130, cy - 20), "0.0.0.0", fill=(248, 250, 252), font=font_title)
            draw.text((cx - 150, cy + 60), "SOURCE: NULL_ORIGIN", fill=(56, 189, 248), font=font_bold)
            draw.text((cx - 170, cy + 120), "PAYLOAD REASSEMBLY IN PROGRESS...", fill=(234, 179, 8), font=font_med)

        elif stype == "recompile":
            # SCENE 7: Biological Compiler Alert
            cx = int(width * 0.5)
            # Digital corruption lines
            for cor_i in range(10):
                cy_line = 240 + cor_i * 30
                draw.text((60, cy_line), "43 52 49 54 49 43 41 4C 20 46 41 55 4C 54 21", fill=(239, 68, 68), font=font_med)
            
            draw.rectangle([(40, int(height * 0.46)), (width - 40, int(height * 0.62))], fill=(69, 10, 10), outline=(239, 68, 68), width=3)
            draw.text((cx - 210, int(height * 0.48)), "[CRITICAL SYSTEM FAULT]", fill=(254, 202, 202), font=font_bold)
            draw.text((cx - 240, int(height * 0.53)), "[BIOLOGICAL COMPILER ACTIVE]", fill=(254, 202, 202), font=font_bold)
            draw.text((cx - 230, int(height * 0.57)), "[TARGET: USER_ABHRANKAN]", fill=(254, 240, 138), font=font_title)

        elif stype == "eye":
            # SCENE 8: Human eye & reality glitch
            cx, cy = int(width * 0.5), int(height * 0.42)
            draw.ellipse([(cx - 220, cy - 110), (cx + 220, cy + 110)], outline=(100, 116, 139), width=8)
            # Iris
            draw.ellipse([(cx - 95, cy - 95), (cx + 95, cy + 95)], fill=(3, 105, 161), outline=(56, 189, 248), width=4)
            # Pupil pulsing
            pupil_r = int(45 + math.sin(f * 0.4) * 12)
            draw.ellipse([(cx - pupil_r, cy - pupil_r), (cx + pupil_r, cy + pupil_r)], fill=(0, 0, 0))
            # Screen reflection
            draw.text((cx - 40, cy - 15), "0.0.0.0", fill=(255, 255, 255), font=font_bold)
            
            # Glitch slices
            if f % 4 < 2:
                for _ in range(4):
                    gy = int(height * 0.35 + np.random.rand() * 200)
                    draw.rectangle([(0, gy), (width, gy + 12)], fill=(239, 68, 68))

        # TOP HUD
        draw.rectangle([(40, 40), (220, 90)], fill=(0, 0, 0, 180), outline=(56, 189, 248), width=2)
        mins, secs = int(t // 60), int(t % 60)
        draw.text((55, 52), f"03:14 AM  {mins:02d}:{secs:02d}", fill=(56, 189, 248), font=font_bold)
        draw.text((width - 180, 52), "REC ● 60s", fill=(239, 68, 68), font=font_bold)
        
        # ACTIVE SCENE BADGE
        draw.text((40, 110), cur_sc["name"], fill=(148, 163, 184), font=font_med)

        # OVERLAY BADGE
        if cur_sc["overlay"]:
            draw.rectangle([(width//2 - 240, int(height * 0.72)), (width//2 + 240, int(height * 0.78))], fill=(0, 0, 0), outline=(234, 179, 8), width=2)
            draw.text((width//2 - 210, int(height * 0.735)), cur_sc["overlay"], fill=(250, 204, 21), font=font_bold)

        # SUBTITLES (BOTTOM)
        draw.rectangle([(40, int(height * 0.82)), (width - 40, int(height * 0.94))], fill=(10, 15, 30), outline=(56, 189, 248), width=2)
        draw.text((60, int(height * 0.835)), "NARRATION:", fill=(148, 163, 184), font=font_med)
        draw.text((60, int(height * 0.875)), f'"{cur_sc["sub"]}"', fill=(255, 255, 255), font=font_bold)

        # ENDING BLACK SCREEN (at 58-60s)
        if t >= 58.0:
            fade = min(1.0, (t - 58.0) / 1.0)
            draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0))
            draw.text((int(width * 0.5) - 180, int(height * 0.48)), "TO BE CONTINUED...", fill=(248, 250, 252), font=font_title)

        # Convert PIL Image to OpenCV BGR
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)
        
        if f % 150 == 0:
            print(f"Progress: {f}/{total_frames} frames ({int(f/total_frames*100)}%)")
            
    out.release()
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
