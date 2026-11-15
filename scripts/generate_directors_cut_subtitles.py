"""
Server Room B - Director's Cut Subtitle Generator
Generates full 120-second synchronized .SRT and .VTT subtitle files for the complete film.
Combines Part 1 (0:00-1:00) and Part 2 (1:00-2:00) with precise timestamps.
Creator: Abhrankan Chakrabarti / Series: Server Room B
"""

import os

SUBTITLES_DATA = [
    # Part 1: The Packet (0:00 - 1:00)
    {"start": "00:00:01,000", "end": "00:00:05,000", "text": "3:14 AM. Server Room B."},
    {"start": "00:00:07,000", "end": "00:00:13,000", "text": "Abhrankan sits alone, tracking a mysterious memory leak."},
    {"start": "00:00:15,000", "end": "00:00:19,000", "text": "Every minute, the system loses exactly sixty-four bytes."},
    {"start": "00:00:21,000", "end": "00:00:27,000", "text": "He launches a network scan. Everything looks normal."},
    {"start": "00:00:29,000", "end": "00:00:34,000", "text": "Then the scrolling stops."},
    {"start": "00:00:37,000", "end": "00:00:43,000", "text": "A single packet appears. Source address: zero point zero point zero point zero."},
    {"start": "00:00:45,000", "end": "00:00:52,000", "text": "The packet begins rearranging itself into words."},
    {"start": "00:00:54,500", "end": "00:00:57,000", "text": "Ah!"},
    {"start": "00:00:57,500", "end": "00:01:00,000", "text": "[ PART 1: THE PACKET CONCLUDED ]"},

    # Part 2: Reality Uninstall (1:00 - 2:00)
    {"start": "00:01:00,300", "end": "00:01:07,500", "text": "The server hum has changed. Instead of a smooth mechanical drone, it now stutters like a broken audio file."},
    {"start": "00:01:07,700", "end": "00:01:14,500", "text": "Abhrankan slowly rises from his chair. He reaches for his phone... and freezes."},
    {"start": "00:01:14,800", "end": "00:01:22,500", "text": "Behind his hand hangs a trail. Not motion blur, but solid frozen copies lingering in the air."},
    {"start": "00:01:22,800", "end": "00:01:29,500", "text": "The security keypad isn't asking for a passcode anymore. It races through endless system messages."},
    {"start": "00:01:29,800", "end": "00:01:38,000", "text": "The wall flickers, vanishing into an infinite black void. The universe wasn't being haunted. It was being uninstalled."},
    {"start": "00:01:38,300", "end": "00:01:45,500", "text": "A deep rumble shakes the room. His workstation monitor flashes violently, casting a blinding strobe pattern."},
    {"start": "00:01:45,800", "end": "00:01:53,500", "text": "The terminal is compiling a new process. And the hardware it's using to build it... is Abhrankan's own brain."},
    {"start": "00:01:55,000", "end": "00:02:00,000", "text": "SERVER ROOM B — Chapter 1: Out of Memory (Complete Director's Cut)\nStory by Abhrankan Chakrabarti | TO BE CONTINUED IN CHAPTER 2"}
]

def generate():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sub_dir = os.path.join(repo_dir, "subtitles")
    os.makedirs(sub_dir, exist_ok=True)

    srt_path = os.path.join(sub_dir, "chapter-01-complete-directors-cut.srt")
    vtt_path = os.path.join(sub_dir, "chapter-01-complete-directors-cut.vtt")

    # 1. Build .SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, entry in enumerate(SUBTITLES_DATA, 1):
            f.write(f"{idx}\n")
            f.write(f"{entry['start']} --> {entry['end']}\n")
            f.write(f"{entry['text']}\n\n")

    # 2. Build .VTT (comma replaced with period in timestamps)
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT - Server Room B: Chapter 1 Out of Memory (Complete Director's Cut)\n\n")
        for idx, entry in enumerate(SUBTITLES_DATA, 1):
            vtt_start = entry['start'].replace(',', '.')
            vtt_end = entry['end'].replace(',', '.')
            f.write(f"{idx}\n")
            f.write(f"{vtt_start} --> {vtt_end}\n")
            f.write(f"{entry['text']}\n\n")

    print(f"Generated SRT: {srt_path} ({os.path.getsize(srt_path)} bytes)")
    print(f"Generated VTT: {vtt_path} ({os.path.getsize(vtt_path)} bytes)")

if __name__ == "__main__":
    generate()
