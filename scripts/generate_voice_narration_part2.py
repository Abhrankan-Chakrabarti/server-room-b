"""
Generates narration voice audio files (.wav) for Server Room B Episode 1 Part 2
using Windows SAPI Text-to-Speech with natural pacing and dramatic delivery.
"""

import os
import yaml
import win32com.client

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-01-part-02.yaml")
    audio_dir = os.path.join(repo_dir, "audio", "narration_part2")
    os.makedirs(audio_dir, exist_ok=True)
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    scenes = data.get("assets", {})
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    
    voices = speaker.GetVoices()
    for v in voices:
        desc = v.GetDescription()
        if "David" in desc or "Zira" in desc or "Mark" in desc or "English" in desc:
            speaker.Voice = v
            print(f"Using SAPI Voice: {desc}")
            break
            
    speaker.Rate = -1 # deliberate sci-fi thriller pacing
    
    for scene_id, content in scenes.items():
        narration = content.get("narration", "").strip()
        if not narration:
            continue
            
        out_wav = os.path.join(audio_dir, f"{scene_id}_narration.wav")
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        file_stream.Open(out_wav, 3, False)
        speaker.AudioOutputStream = file_stream
        speaker.Speak(narration)
        file_stream.Close()
        print(f"Generated: {out_wav} -> \"{narration}\"")
        
    print("\nAll narration audio files generated successfully in audio/narration_part2/")

if __name__ == "__main__":
    main()
