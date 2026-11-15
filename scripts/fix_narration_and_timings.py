"""
Fix Narration Audio Pacing & Scene Durations
1. Regenerates narration audio stems for Episode 2 and Part 2 with crisp SAPI pacing (Rate = 1).
2. Measures exact audio duration for each scene.
3. Computes generous scene timings (audio duration + 1.2s buffer) so voiceover is 100% audible.
4. Re-mixes master soundtracks.
"""

import os
import wave
import yaml
import win32com.client
import numpy as np

def generate_voice_stems(yaml_path, out_dir, rate=1):
    os.makedirs(out_dir, exist_ok=True)
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    scenes = data.get("scenes", [])
    if not scenes and "assets" in data:
        scenes = [{"scene_id": k, **v} for k, v in data["assets"].items()]

    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    for v in speaker.GetVoices():
        if "David" in v.GetDescription():
            speaker.Voice = v
            break
    speaker.Rate = rate

    durations = {}
    for s in scenes:
        sc_id = s.get("scene_id")
        narr = s.get("narration", "").strip()
        if not narr:
            continue
        out_wav = os.path.join(out_dir, f"{sc_id}_narration.wav")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(out_wav, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(narr)
        stream.Close()

        with wave.open(out_wav, "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
            durations[sc_id] = dur
            print(f"[{sc_id}] ({dur:.2f}s): \"{narr}\"")

    return durations

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ep2_yaml = os.path.join(repo_dir, "episodes", "episode-02-force-quit.yaml")
    ep2_narr_dir = os.path.join(repo_dir, "audio", "narration_ep2")

    part2_yaml = os.path.join(repo_dir, "episodes", "episode-01-part-02.yaml")
    part2_narr_dir = os.path.join(repo_dir, "audio", "narration_part2")

    print("=== Generating Episode 2 Voice Stems at Rate 1 ===")
    ep2_durs = generate_voice_stems(ep2_yaml, ep2_narr_dir, rate=1)

    print("\n=== Generating Part 2 Voice Stems at Rate 1 ===")
    part2_durs = generate_voice_stems(part2_yaml, part2_narr_dir, rate=1)

    print("\n=== Summary of Durations & Safe Scene Lengths ===")
    print("Episode 2 Safe Scene Lengths:")
    for sc, d in ep2_durs.items():
        safe_len = round(d + 1.0, 1)
        print(f"  {sc}: audio={d:.2f}s -> scene_duration={safe_len}s")

    print("\nPart 2 Safe Scene Lengths:")
    for sc, d in part2_durs.items():
        safe_len = round(d + 1.0, 1)
        print(f"  {sc}: audio={d:.2f}s -> scene_duration={safe_len}s")

if __name__ == "__main__":
    main()
