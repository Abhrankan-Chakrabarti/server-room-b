"""
Generates narration voice audio files (.wav) for each scene in Server Room B Episode 1
using Windows SAPI Text-to-Speech (native, zero-dependency).
"""

import os
import yaml
import win32com.client

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-01-the-packet.yaml")
    audio_dir = os.path.join(repo_dir, "audio", "narration")
    os.makedirs(audio_dir, exist_ok=True)
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    scenes = data.get("assets", {})
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    
    # Try selecting a natural sounding English voice if available
    voices = speaker.GetVoices()
    for v in voices:
        desc = v.GetDescription()
        if "David" in desc or "Zira" in desc or "Mark" in desc or "English" in desc:
            speaker.Voice = v
            print(f"Using SAPI Voice: {desc}")
            break
            
    speaker.Rate = -1 # slightly slower, deliberate sci-fi pacing
    
    for scene_id, content in scenes.items():
        narration = content.get("narration", "").strip()
        if not narration:
            continue
            
        out_wav = os.path.join(audio_dir, f"{scene_id}_narration.wav")
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        # 39 = SAFT48kHz16BitStereo or standard WAV format
        file_stream.Open(out_wav, 3, False)
        speaker.AudioOutputStream = file_stream
        speaker.Speak(narration)
        file_stream.Close()
        print(f"Generated: {out_wav} -> \"{narration}\"")
        
    print("\nAll narration audio files generated successfully in audio/narration/")

if __name__ == "__main__":
    main()
