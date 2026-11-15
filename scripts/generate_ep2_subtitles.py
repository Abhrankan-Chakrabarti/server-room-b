"""
Generate synchronized .SRT and .VTT subtitle files for Episode 2: Force Quit
Aligned with the exact audio timestamps and breathing buffers.
Creator: Abhrankan Chakrabarti / Series: Server Room B
"""

import os

entries = [
    {"start": "00:00:00,400", "end": "00:00:07,800", "text": "Abhrankan's reflex wasn't flight. It was to isolate the process, kill it, and reclaim the resources."},
    {"start": "00:00:08,400", "end": "00:00:16,800", "text": "He types the kill command. The shell rejects it immediately: PID 1. You cannot kill the init process of reality."},
    {"start": "00:00:17,600", "end": "00:00:25,800", "text": "He forces a raw kernel reboot. Nothing. The kernel no longer answers to hardware interrupts from this side of existence."},
    {"start": "00:00:26,500", "end": "00:00:34,800", "text": "A warning floods the room. His privilege level is demoted to userland. Physics locks to a fixed sixteen-millisecond loop."},
    {"start": "00:00:35,400", "end": "00:00:41,800", "text": "Time becomes quantized. The universe wasn't being haunted... the runtime itself was breaking."},
    {"start": "00:00:42,600", "end": "00:00:49,000", "text": "Collision meshes are unloaded. He sprints and phases directly through the solid steel security door."},
    {"start": "00:00:49,700", "end": "00:00:56,800", "text": "The hallway beyond is decompiling. Sodium lights flicker at sixty hertz as server racks tear through the floor."},
    {"start": "00:00:57,300", "end": "00:01:05,800", "text": "The terminal prints: Compiling User Abhrankan, twenty-three percent. But until the build finishes, he still owns himself."},
    {"start": "00:01:06,000", "end": "00:01:07,000", "text": "SERVER ROOM B — Chapter 2: Force Quit\nStory by Abhrankan Chakrabarti | TO BE CONTINUED IN CHAPTER 3"}
]

def generate():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sub_dir = os.path.join(repo_dir, "subtitles")
    os.makedirs(sub_dir, exist_ok=True)

    srt_path = os.path.join(sub_dir, "episode-02-force-quit.srt")
    vtt_path = os.path.join(sub_dir, "episode-02-force-quit.vtt")

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
