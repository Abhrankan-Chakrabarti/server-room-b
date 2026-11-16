import os
import json
import yaml

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-03-link-stage.yaml")
    md_path = os.path.join(repo_dir, "episodes", "kling_prompts_episode_03.md")
    json_path = os.path.join(repo_dir, "episodes", "kling_prompts_episode_03.json")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 1. Generate JSON
    kling_json = {
        "project": data.get("project", "Server Room B"),
        "episode": data.get("episode", {}),
        "prompts": []
    }

    for sc in data.get("scenes", []):
        kling_json["prompts"].append({
            "scene_number": sc["scene_number"],
            "scene_id": sc["scene_id"],
            "title": sc["title"],
            "duration_seconds": sc["duration_seconds"],
            "timecode": f"{sc['start_time']} - {sc['end_time']}",
            "kling_prompt": f"{sc['kling_prompt']} --ar 9:16 --v 1.5",
            "camera": sc["camera_direction"],
            "narration": sc["narration"],
            "overlay_text": sc["overlay_text"]
        })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(kling_json, f, indent=2)
    print(f"Exported JSON: {json_path}")

    # 2. Generate Markdown Cheat Sheet
    md_lines = [
        f"# Server Room B — Episode 3: Link Stage (Chapter 3 Adaptation)",
        f"**Director & Writer:** {data['episode']['creator']} | **Channel:** {data['episode']['channel']}",
        f"**Format:** Vertical 9:16 (720x1280 @ 30fps) | **Duration:** {data['episode']['target_duration_seconds']}s (8 Scenes @ 8.5s each)\n",
        f"---",
        f"## Kling AI & Midjourney Production Matrix\n"
    ]

    for sc in data.get("scenes", []):
        md_lines.append(f"### Scene {sc['scene_number']}: {sc['title']} ({sc['start_time']} - {sc['end_time']} | {sc['duration_seconds']}s)")
        md_lines.append(f"- **Camera Movement:** `{sc['camera_direction']}`")
        md_lines.append(f"- **Narration Voiceover:** *\"{sc['narration']}\"*")
        md_lines.append(f"- **HUD Overlays:** `{'` • `'.join(sc['overlay_text'])}`")
        md_lines.append(f"```text\n{sc['kling_prompt']} --ar 9:16 --v 1.5\n```\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Exported Markdown: {md_path}")

if __name__ == "__main__":
    main()
