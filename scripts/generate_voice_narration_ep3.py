import os
import wave
import yaml
import win32com.client

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-03-link-stage.yaml")
    out_dir = os.path.join(repo_dir, "audio", "narration_ep3")
    os.makedirs(out_dir, exist_ok=True)

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    for v in speaker.GetVoices():
        if "David" in v.GetDescription():
            speaker.Voice = v
            break
    speaker.Rate = 1  # Natural cadence, crisp delivery

    durations = {}
    for sc in data.get("scenes", []):
        sc_id = sc["scene_id"]
        text = sc["narration"]
        wav_path = os.path.join(out_dir, f"{sc_id}_narration.wav")

        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(wav_path, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()

        with wave.open(wav_path, "rb") as wf:
            dur = wf.getnframes() / float(wf.getframerate())
            durations[sc_id] = dur
            buffer = sc["duration_seconds"] - dur
            print(f"🎙️ {sc_id}: {dur:.2f}s (Scene duration: {sc['duration_seconds']}s, Buffer: {buffer:.2f}s)")

    print(f"✅ All 8 voice narration stems generated in {out_dir}")

if __name__ == "__main__":
    main()
