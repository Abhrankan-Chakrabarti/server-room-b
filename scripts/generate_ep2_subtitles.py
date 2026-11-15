"""
Generate synchronized .SRT and .VTT subtitle files for Episode 2: Force Quit
Aligns with scenes 01-08 in episodes/episode-02-force-quit.yaml.
Creator: Abhrankan Chakrabarti / Series: Server Room B
"""

import os
import yaml

def generate():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-02-force-quit.yaml")
    sub_dir = os.path.join(repo_dir, "subtitles")
    os.makedirs(sub_dir, exist_ok=True)

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    srt_path = os.path.join(sub_dir, "episode-02-force-quit.srt")
    vtt_path = os.path.join(sub_dir, "episode-02-force-quit.vtt")

    # Timings map
    entries = [
        {"start": "00:00:00,500", "end": "00:00:06,500", "text": "Abhrankan's reflex wasn't flight. It was to isolate the process, kill it, and reclaim the resources."},
        {"start": "00:00:07,000", "end": "00:00:13,500", "text": "He types the kill command. The shell rejects it immediately: PID 1. You cannot kill the init process of reality."},
        {"start": "00:00:14,000", "end": "00:00:20,500", "text": "He forces a raw kernel reboot. Nothing. The kernel no longer answers to hardware interrupts from this side of existence."},
        {"start": "00:00:21,000", "end": "00:00:27,500", "text": "A warning floods the room. His privilege level is demoted to userland. Physics locks to a fixed sixteen-millisecond loop."},
        {"start": "00:00:28,000", "end": "00:00:34,500", "text": "Time becomes quantized. The universe wasn't being haunted... the runtime itself was breaking."},
        {"start": "00:00:35,000", "end": "00:00:42,500", "text": "Collision meshes are unloaded. He sprints and phases directly through the solid steel security door."},
        {"start": "00:00:43,000", "end": "00:00:51,500", "text": "The hallway beyond is decompiling. Sodium lights flicker at sixty hertz as server racks tear through the floor."},
        {"start": "00:00:52,000", "end": "00:00:58,000", "text": "The terminal prints: Compiling User Abhrankan, twenty-three percent. But until the build finishes, he still owns himself."},
        {"start": "00:00:58,500", "end": "00:01:00,000", "text": "SERVER ROOM B — Chapter 2: Force Quit\nStory by Abhrankan Chakrabarti | TO BE CONTINUED IN CHAPTER 3"}
    ]

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, e in enumerate(entries, 1):
            f.write(f"{idx}\n{e['start']} --> {e['end']}\n{e['text']}\n\n")

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT - Server Room B: Episode 2 (Force Quit)\n\n")
        for idx, e in enumerate(entries, 1):
            v_start = e['start'].replace(',', '.')
            v_end = e['end'].replace(',', '.')
            f.write(f"{idx}\n{v_start} --> {v_end}\n{e['text']}\n\n")

    print(f"Generated SRT: {srt_path} ({os.path.getsize(srt_path)} bytes)")
    print(f"Generated VTT: {vtt_path} ({os.path.getsize(vtt_path)} bytes)")

if __name__ == "__main__":
    generate()
