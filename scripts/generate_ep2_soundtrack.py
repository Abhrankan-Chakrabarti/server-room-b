"""
Synthesizes the custom sound design and master soundtrack for Server Room B - Episode 2: Force Quit.
Audio Elements:
- 60Hz electrical grid drone + 16.67ms temporal frame-lock ticking
- PID 1 kill denial harsh buzz at 8.5s
- SysRq hardware interrupt dead-air silence at 17.5s
- Sub-bass reality phasing sweep (steel door no-clip) at 42.4s
- Z-buffer polygon interpenetration flutter at 49.5s
- Synchronized SAPI voice narration stems (Rate = 1) with zero cutoffs
"""

import os
import wave
import numpy as np
import subprocess
import imageio_ffmpeg

EP2_SCENE_TIMINGS = {
    "scene_01": 0.4,
    "scene_02": 8.4,
    "scene_03": 17.6,
    "scene_04": 26.5,
    "scene_05": 35.4,
    "scene_06": 42.6,
    "scene_07": 49.7,
    "scene_08": 57.3
}
TOTAL_DURATION = 67.0
SAMPLE_RATE = 44100

def create_ep2_audio(out_wav, total_duration=TOTAL_DURATION, sample_rate=SAMPLE_RATE):
    total_samples = int(total_duration * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)

    # 1. Base Ambient: 60Hz ground hum with 120Hz & 180Hz transformer harmonics
    base_hum = (
        0.14 * np.sin(2 * np.pi * 60 * t) +
        0.08 * np.sin(2 * np.pi * 120 * t) +
        0.04 * np.sin(2 * np.pi * 180 * t)
    )
    audio += base_hum

    # 2. 16.67ms (60 FPS) Physics Frame-Lock Ticks starting at Scene 4 (26.5s) to end
    start_tick = int(26.5 * sample_rate)
    tick_period = int(0.01667 * sample_rate)
    for i in range(start_tick, total_samples, tick_period):
        burst_len = min(40, total_samples - i)
        audio[i:i+burst_len] += 0.10 * np.hanning(burst_len) * (np.random.rand(burst_len) * 2 - 1)

    # 3. PID 1 Kill Denial Harsh Error Buzz (Scene 2: ~8.8s)
    idx_err = int(8.8 * sample_rate)
    err_len = int(1.2 * sample_rate)
    t_err = np.linspace(0, 1.2, err_len)
    err_buzz = 0.22 * np.sign(np.sin(2 * np.pi * 150 * t_err)) * np.exp(-t_err * 1.5)
    audio[idx_err:idx_err+err_len] += err_buzz

    # 4. SysRq Dead-Air Tension Drop (Scene 3: ~18.0s)
    idx_sysrq = int(18.0 * sample_rate)
    drop_len = int(3.0 * sample_rate)
    audio[idx_sysrq:idx_sysrq+drop_len] *= 0.4

    # 5. Steel Door Phase Sub-Bass Sweep (Scene 6: ~42.6s)
    idx_phase = int(42.6 * sample_rate)
    phase_len = int(5.5 * sample_rate)
    t_p = np.linspace(0, 5.5, phase_len)
    freq_sweep = np.linspace(120, 28, phase_len)
    sub_phase = 0.38 * np.sin(2 * np.pi * freq_sweep * t_p) * np.exp(-t_p * 0.35)
    audio[idx_phase:idx_phase+phase_len] += sub_phase

    # 6. Z-Buffer Polygon Flutter (Scene 7: ~49.7s)
    idx_z = int(49.7 * sample_rate)
    z_len = int(7.0 * sample_rate)
    t_z = np.linspace(0, 7.0, z_len)
    z_flutter = 0.07 * np.sin(2 * np.pi * 6000 * t_z + np.sin(2 * np.pi * 30 * t_z) * 5)
    audio[idx_z:idx_z+z_len] += z_flutter

    # 7. Mix in Voice Narration Stems from audio/narration_ep2/
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    narr_dir = os.path.join(repo_dir, "audio", "narration_ep2")

    for sc_id, start_sec in EP2_SCENE_TIMINGS.items():
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
            # Duck ambient slightly under narration
            audio[start_idx:end_idx] *= 0.50
            audio[start_idx:end_idx] += narr_data[:copy_len] * 1.0

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

    wav_out = os.path.join(audio_dir, "episode_02_soundtrack.wav")
    mp3_out = os.path.join(audio_dir, "episode_02_soundtrack.mp3")

    create_ep2_audio(wav_out)
    convert_to_mp3(wav_out, mp3_out)

if __name__ == "__main__":
    main()
