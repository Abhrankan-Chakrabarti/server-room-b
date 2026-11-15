"""
Export Kling AI Prompts for Episode 2: Force Quit
Reads episodes/episode-02-force-quit.yaml and exports JSON and Markdown prompt guides.
"""

import os
import json
import yaml

def export_prompts():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-02-force-quit.yaml")
    json_path = os.path.join(repo_dir, "episodes", "kling_prompts_episode_02.json")
    md_path = os.path.join(repo_dir, "episodes", "kling_prompts_episode_02.md")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Build JSON
    json_out = {
        "project": data["project"],
        "episode": data["episode"],
        "format": "Vertical 9:16 (720x1280)",
        "target_duration": data["episode"]["target_duration_seconds"],
        "scenes": []
    }

    negative_prompt = "daylight, cartoon, 3d animation, deformed, extra limbs, blurry, low resolution, watermark, smiling, casual"

    for s in data["scenes"]:
        scene_entry = {
            "scene_id": s["scene_id"],
            "scene_number": s["scene_number"],
            "title": s["title"],
            "target_duration_seconds": s["duration_seconds"],
            "kling_duration_seconds": min(s["duration_seconds"], 10),
            "aspect_ratio": "Vertical 9:16",
            "kling_prompt": f"{s['kling_prompt']}, Vertical 9:16 mobile framing, {s['camera_direction']}, cinematic anamorphic bokeh, 8k resolution, photorealistic, 35mm film grain, ARRI Alexa LF style",
            "camera_direction": s["camera_direction"],
            "negative_prompt": negative_prompt,
            "narration": s["narration"],
            "overlay_text": s.get("overlay_text", []),
        }
        json_out["scenes"].append(scene_entry)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, indent=2)

    # Build Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Server Room B — Episode 2: Force Quit\n")
        f.write(f"## Kling AI Video Generation Prompts & Camera Direction Guide\n\n")
        f.write(f"**Series:** Server Room B • **Episode:** 2 • **Runtime:** 60s (Scenes 01–08)\n")
        f.write(f"**Author & Director:** Abhrankan Chakrabarti\n\n---\n\n")

        for s in json_out["scenes"]:
            f.write(f"### Scene {s['scene_number']:02d}: {s['title']} ({s['target_duration_seconds']}s)\n")
            f.write(f"- **Kling Video Prompt:**\n  > `{s['kling_prompt']}`\n")
            f.write(f"- **Camera Direction:** {s['camera_direction']}\n")
            f.write(f"- **Negative Prompt:** `{s['negative_prompt']}`\n")
            f.write(f"- **Voice Narration:** *\"{s['narration']}\"*\n")
            f.write(f"- **Overlay Text:** `{', '.join(s['overlay_text'])}`\n\n")

    print(f"Exported JSON: {json_path} ({os.path.getsize(json_path)} bytes)")
    print(f"Exported Markdown: {md_path} ({os.path.getsize(md_path)} bytes)")

if __name__ == "__main__":
    export_prompts()
