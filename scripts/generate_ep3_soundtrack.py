"""
Synthesizes the custom sound design and master soundtrack for Server Room B - Episode 3: Link Stage.
Audio Elements:
- MDF industrial cooling roar + 60Hz ground hum
- 15.7kHz retinal CRT whine (41% burnout)
- 115200 baud serial connection chatter & Cisco fan spin-up
- 8-bit VGA bitcrush quantization distortion at 67%
- Biological driver tension heartbeat at 89%
- The 0ms Timeless Freeze (complete dead-air silence on Enter key)
- Digital rain dissolve & Connection reset by peer chime
- Synchronized voice narration stems from audio/narration_ep3/
"""

import os
import wave
import numpy as np
import subprocess
import imageio_ffmpeg

EP3_SCENE_TIMINGS = {
    "scene_01": 0.4,
    "scene_02": 9.2,
    "scene_03": 19.0,
    "scene_04": 28.8,
    "scene_05": 38.2,
    "scene_06": 47.8,
    "scene_07": 57.4,
    "scene_08": 67.0
}
TOTAL_DURATION = 78.0
SAMPLE_RATE = 44100

def create_ep3_audio(out_wav, total_duration=TOTAL_DURATION, sample_rate=SAMPLE_RATE):
    total_samples = int(total_duration * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)

    # 1. Base Ambient: 60Hz hum + deep MDF cooling airflow
    base_hum = (
        0.10 * np.sin(2 * np.pi * 60 * t) +
        0.05 * np.sin(2 * np.pi * 120 * t) +
        0.02 * np.sin(2 * np.pi * 180 * t)
    )
    # Pink noise airflow
    np.random.seed(42)
    noise = np.random.randn(total_samples).astype(np.float32)
    # Simple lowpass moving average
    kernel_size = 120
    kernel = np.ones(kernel_size, dtype=np.float32) / kernel_size
    smooth_noise = np.convolve(noise, kernel, mode='same') * 0.08

    audio += base_hum + smooth_noise

    # 2. Retinal CRT Whine (Scene 2: 9.0s - 18.8s)
    s2_start = int(9.0 * sample_rate)
    s2_len = int(9.8 * sample_rate)
    t_crt = np.linspace(0, 9.8, s2_len)
    crt_whine = 0.04 * np.sin(2 * np.pi * 12500 * t_crt) * (1 + 0.3 * np.sin(2 * np.pi * 4 * t_crt))
    audio[s2_start:s2_start+s2_len] += crt_whine

    # 3. Serial 115200 Baud Clicks (Scene 4: 28.6s - 38.0s)
    s4_start = int(28.6 * sample_rate)
    s4_end = int(38.0 * sample_rate)
    for i in range(s4_start, s4_end, int(0.08 * sample_rate)):
        click_len = min(15, total_samples - i)
        audio[i:i+click_len] += 0.12 * (np.random.rand(click_len) * 2 - 1)

    # 4. 8-Bit VGA Bitcrush / Quantization Noise (Scene 5: 38.0s - 47.6s)
    s5_start = int(38.0 * sample_rate)
    s5_len = int(9.6 * sample_rate)
    t_vga = np.linspace(0, 9.6, s5_len)
    vga_tone = 0.08 * np.sign(np.sin(2 * np.pi * 440 * t_vga + np.sin(2 * np.pi * 8 * t_vga) * 2))
    audio[s5_start:s5_start+s5_len] += vga_tone

    # 5. Heartbeat & Spasm Tension (Scene 6: 47.6s - 57.2s)
    s6_start = int(47.6 * sample_rate)
    s6_len = int(9.6 * sample_rate)
    for hb in range(s6_start, s6_start + s6_len, int(0.75 * sample_rate)):
        hb_len = min(int(0.2 * sample_rate), total_samples - hb)
        t_hb = np.linspace(0, 0.2, hb_len)
        thump = 0.30 * np.sin(2 * np.pi * 55 * t_hb) * np.exp(-t_hb * 18)
        audio[hb:hb+hb_len] += thump

    # 6. Mechanical Enter Slam + 0ms DEAD AIR FREEZE (Scene 7: ~62.0s to 66.8s)
    idx_enter = int(62.0 * sample_rate)
    # Loud mechanical key click
    click_len = int(0.04 * sample_rate)
    t_click = np.linspace(0, 0.04, click_len)
    key_click = 0.50 * np.sin(2 * np.pi * 1200 * t_click) * np.exp(-t_click * 100)
    audio[idx_enter:idx_enter+click_len] += key_click

    # Complete silence from 62.05s to 66.8s (The 0ms timeless frame)
    idx_freeze_start = int(62.05 * sample_rate)
    idx_freeze_end = int(66.8 * sample_rate)
    audio[idx_freeze_start:idx_freeze_end] = 0.0

    # 7. Connection Reset by Peer Chime & Digital Rain (Scene 8: 66.8s - 78.0s)
    idx_reset = int(66.8 * sample_rate)
    t_chime = np.linspace(0, 2.5, int(2.5 * sample_rate))
    ack_chime = (
        0.25 * np.sin(2 * np.pi * 880 * t_chime) +
        0.18 * np.sin(2 * np.pi * 1760 * t_chime)
    ) * np.exp(-t_chime * 1.8)
    audio[idx_reset:idx_reset+len(ack_chime)] += ack_chime

    # Digital rain noise wash
    t_rain = np.linspace(0, 10.0, total_samples - idx_reset)
    rain_noise = np.random.randn(len(t_rain)).astype(np.float32) * 0.06 * np.exp(-t_rain * 0.3)
    audio[idx_reset:] += rain_noise

    # 8. Mix in Voice Narration Stems from audio/narration_ep3/
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    narr_dir = os.path.join(repo_dir, "audio", "narration_ep3")

    for sc_id, start_sec in EP3_SCENE_TIMINGS.items():
        wav_file = os.path.join(narr_dir, f"{sc_id}_narration.wav")
        if os.path.exists(wav_file):
            wf = wave.open(wav_file, "rb")
            n_frames = wf.getnframes()
            rate = wf.getframerate()
            raw = wf.readframes(n_frames)
            wf.close()
            narr_data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

            if rate != sample_rate:
                indices = np.round(np.linspace(0, n_frames - 1, int(n_frames * sample_rate / rate))).astype(int)
                narr_data = narr_data[indices]

            start_idx = int(start_sec * sample_rate)
            end_idx = min(start_idx + len(narr_data), total_samples)
            copy_len = end_idx - start_idx
            # Duck ambient under narration
            audio[start_idx:end_idx] *= 0.45
            audio[start_idx:end_idx] += narr_data[:copy_len] * 1.05

    peak = np.max(np.abs(audio))
    if peak > 0.95:
        audio = (audio / peak) * 0.95

    int_data = (audio * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_data.tobytes())
    print(f"Master Soundtrack WAV rendered: {out_wav} ({os.path.getsize(out_wav)} bytes)")

def convert_to_mp3(wav_path, mp3_path):
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_bin, "-y", "-i", wav_path, "-b:a", "320k", mp3_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Exported MP3: {mp3_path} ({os.path.getsize(mp3_path)} bytes)")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(repo_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    wav_out = os.path.join(audio_dir, "episode_03_soundtrack.wav")
    mp3_out = os.path.join(audio_dir, "episode_03_soundtrack.mp3")

    create_ep3_audio(wav_out)
    convert_to_mp3(wav_out, mp3_out)

if __name__ == "__main__":
    main()
