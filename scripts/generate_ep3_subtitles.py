import os
import yaml

def format_timestamp_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_timestamp_vtt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-03-link-stage.yaml")
    srt_path = os.path.join(repo_dir, "subtitles", "episode-03-link-stage.srt")
    vtt_path = os.path.join(repo_dir, "subtitles", "episode-03-link-stage.vtt")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    srt_entries = []
    vtt_entries = ["WEBVTT - Server Room B: Episode 3 (Link Stage)\n"]

    current_t = 0.4
    idx = 1
    for sc in data.get("scenes", []):
        narr = sc["narration"]
        dur = sc["duration_seconds"]
        
        # Audio speech length is roughly dur - 1.2s
        speech_end = current_t + dur - 1.0

        srt_entries.append(f"{idx}\n{format_timestamp_srt(current_t)} --> {format_timestamp_srt(speech_end)}\n{narr}\n")
        vtt_entries.append(f"{idx}\n{format_timestamp_vtt(current_t)} --> {format_timestamp_vtt(speech_end)}\n{narr}\n")
        
        current_t += dur
        idx += 1

    # End Title Card entry
    srt_entries.append(f"{idx}\n{format_timestamp_srt(76.5)} --> {format_timestamp_srt(78.0)}\nSERVER ROOM B — Chapter 3: Link Stage\nStory by Abhrankan Chakrabarti | TO BE CONTINUED IN CHAPTER 4\n")
    vtt_entries.append(f"{idx}\n{format_timestamp_vtt(76.5)} --> {format_timestamp_vtt(78.0)}\nSERVER ROOM B — Chapter 3: Link Stage\nStory by Abhrankan Chakrabarti | TO BE CONTINUED IN CHAPTER 4\n")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"Generated SRT: {srt_path} ({os.path.getsize(srt_path)} bytes)")

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_entries))
    print(f"Generated VTT: {vtt_path} ({os.path.getsize(vtt_path)} bytes)")

if __name__ == "__main__":
    main()
