"""
Synthesizes the custom sound effects for Server Room B - Episode 1 Part 2: Reality Uninstall.
Includes:
- 2ms acoustic stuttering fan loop ('BZZ-T. BZZ-T. BZZ-T.')
- Propriception tactile lag pulse (Scene 10)
- Cascading window-drag artifact frequency shift (Scene 11)
- Keypad log rapid telemetry stream (Scene 12)
- Void collapse & reality clipping sub-drop (Scene 13)
- Deep room rumble & blinding strobe arc discharge (Scene 14)
- Neural compiler telemetry & bioscan hum (Scene 15)
"""

import os
import wave
import numpy as np

def generate_part2_ambient_sfx(out_wav, total_duration=60.0, sample_rate=44100):
    total_samples = int(total_duration * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)

    # 1. Base Server Fan Hum with 2ms Quantized Audio Stutter (Scene 09-16)
    # The fan sound isn't continuous anymore—it stutters in discrete 2ms blocks.
    base_fan = 0.14 * np.sin(2 * np.pi * 55 * t) + 0.08 * np.sin(2 * np.pi * 110 * t) + 0.04 * np.random.normal(0, 0.2, total_samples)
    
    # 2ms stutter gate: 2ms ON (88 samples at 44.1k), 2ms OFF
    stutter_period_samples = int(0.002 * sample_rate) * 2 # 4ms period (2ms on, 2ms off)
    stutter_gate = ((np.arange(total_samples) % stutter_period_samples) < (stutter_period_samples // 2)).astype(np.float32)
    
    # Scene 09 starts with normal hum dropping pitch into stutter at t=2.5s
    stutter_mix = np.clip((t - 2.0) / 1.5, 0.0, 1.0)
    audio += base_fan * (1.0 - stutter_mix * 0.7) + (base_fan * stutter_gate) * (stutter_mix * 1.2)
    
    # Add rhythmic 'BZZ-T' impulse accent every 0.8s during Scene 09
    for bzzt_t in [2.8, 3.6, 4.4, 5.2, 6.0, 6.8]:
        idx = int(bzzt_t * sample_rate)
        bz_len = int(0.12 * sample_rate)
        t_bz = np.linspace(0, 0.12, bz_len)
        bz_burst = 0.22 * np.sin(2 * np.pi * 180 * t_bz) * np.exp(-t_bz * 18) * (np.sin(2 * np.pi * 500 * t_bz) > 0)
        audio[idx:idx+bz_len] += bz_burst

    # Scene 10: Tactile lag tone at 10.5s (Abhrankan freezes)
    idx_10 = int(10.5 * sample_rate)
    l_len = int(1.2 * sample_rate)
    t_l = np.linspace(0, 1.2, l_len)
    audio[idx_10:idx_10+l_len] += 0.20 * np.sin(2 * np.pi * 320 * t_l) * np.exp(-t_l * 2.5)

    # Scene 11: Cascading polygon duplicates pitch riser (16s - 22s)
    idx_11 = int(16.0 * sample_rate)
    c_len = int(5.0 * sample_rate)
    t_c = np.linspace(0, 5.0, c_len)
    chirp = 0.15 * np.sin(2 * np.pi * (240 + 80 * t_c) * t_c) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * t_c))
    audio[idx_11:idx_11+c_len] += chirp

    # Scene 12: Keypad rapid data stream clicker (23s - 28s)
    for k_t in np.linspace(23.0, 28.5, 30):
        k_idx = int(k_t * sample_rate)
        k_len = int(0.015 * sample_rate)
        audio[k_idx:k_idx+k_len] += 0.12 * (np.random.rand(k_len) * 2 - 1)

    # Scene 13: Void collapse & reality clipping sub-bass drop at 30.5s
    idx_13 = int(30.5 * sample_rate)
    v_len = int(4.0 * sample_rate)
    t_v = np.linspace(0, 4.0, v_len)
    sub_drop = 0.35 * np.sin(2 * np.pi * (65 - 12 * t_v) * t_v) * np.exp(-t_v * 0.7)
    audio[idx_13:idx_13+v_len] += sub_drop

    # Scene 14: Deep room-shaking rumble & blinding strobe electrical crackle (38s - 45s)
    idx_14 = int(38.0 * sample_rate)
    r_len = int(7.0 * sample_rate)
    t_r = np.linspace(0, 7.0, r_len)
    rumble = 0.32 * np.sin(2 * np.pi * 38 * t_r) * (1.0 + 0.3 * np.sin(2 * np.pi * 2 * t_r))
    strobe_crackle = 0.18 * (np.random.rand(r_len) * 2 - 1) * (np.sin(2 * np.pi * 8 * t_r) > 0.4)
    audio[idx_14:idx_14+r_len] += (rumble + strobe_crackle)

    # Scene 15: Biological compiler neural alert & heart monitor spike (46s - 53s)
    idx_15 = int(46.0 * sample_rate)
    b_len = int(7.0 * sample_rate)
    t_b = np.linspace(0, 7.0, b_len)
    heartbeat = np.zeros(b_len, dtype=np.float32)
    for hb in [0.2, 0.45, 1.2, 1.45, 2.2, 2.45, 3.2, 3.45, 4.2, 4.45, 5.2, 5.45]:
        h_idx = int(hb * sample_rate)
        h_pulse = int(0.08 * sample_rate)
        if h_idx + h_pulse < b_len:
            t_hp = np.linspace(0, 0.08, h_pulse)
            heartbeat[h_idx:h_idx+h_pulse] += 0.38 * np.sin(2 * np.pi * 75 * t_hp) * np.exp(-t_hp * 35)
    audio[idx_15:idx_15+b_len] += heartbeat

    # Scene 16: Whiteout blast into pure silence (53.5s - 60s)
    idx_16 = int(53.5 * sample_rate)
    w_len = int(2.5 * sample_rate)
    t_w = np.linspace(0, 2.5, w_len)
    whiteout = 0.40 * np.exp(-t_w * 2.0) * (np.sin(2 * np.pi * 880 * t_w) + 0.5 * (np.random.rand(w_len) * 2 - 1))
    audio[idx_16:idx_16+w_len] += whiteout
    # Absolute cut to black silence after 56.5s
    idx_cut = int(56.5 * sample_rate)
    audio[idx_cut:] *= 0.0

    # Master clipping protection
    audio = np.clip(audio, -0.92, 0.92)
    int_data = (audio * 32767).astype(np.int16)

    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_data.tobytes())

    print(f"Generated Part 2 SFX Bed: {out_wav} ({total_duration}s)")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio", "part2_ambient_sfx.wav")
    generate_part2_ambient_sfx(out)
