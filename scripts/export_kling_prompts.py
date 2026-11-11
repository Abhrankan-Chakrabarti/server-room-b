"""
Export and optimize Kling AI video prompts from episode YAML specifications.
"""

import os
import json
import yaml

def load_episode(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def optimize_for_kling(scene_id, scene_data, format_ratio="9:16"):
    base_prompt = " ".join(scene_data.get("prompt", "").split())
    duration_str = scene_data.get("duration", "5s")
    duration_sec = int(''.join(filter(str.isdigit, duration_str)) or 5)
    
    # Kling AI clip duration is typically 5s or 10s per generation
    kling_duration = 10 if duration_sec > 7 else 5
    
    camera_hints = {
        "scene_01": "Dolly in, slow smooth camera push through server corridor, cinematic anamorphic bokeh",
        "scene_02": "Slow push in on subject, low angle medium shot, dramatic screen reflection",
        "scene_03": "Over-the-shoulder shot locked on glowing CRT/OLED console, subtle camera breathing",
        "scene_04": "Extreme close up on digital matrix terminal, subtle rack focus",
        "scene_05": "Static freeze frame with subtle floating dust particles, ominous stillness",
        "scene_06": "Sudden digital camera push toward center of display, anamorphic lens flare",
        "scene_07": "Dynamic zoom with chromatic aberration and phosphor decay, reality distortion",
        "scene_08": "Macro lens extreme close-up on pupil dialation, biometric scan reflections"
    }

    camera_guidance = camera_hints.get(scene_id, "Cinematic camera movement")
    
    full_prompt = (
        f"{base_prompt}, "
        f"Vertical 9:16 mobile framing, "
        f"{camera_guidance}, "
        f"8k resolution, photorealistic, 35mm film grain, ARRI Alexa LF style"
    )
    
    negative_prompt = (
        "daylight, cartoon, illustration, low resolution, 3d render, oversaturated, "
        "distorted face, extra fingers, deformed hands, blurry, watermark, smiling, happy, cheerful"
    )
    
    return {
        "scene_id": scene_id,
        "target_duration_seconds": duration_sec,
        "kling_duration_seconds": kling_duration,
        "aspect_ratio": format_ratio,
        "kling_prompt": full_prompt,
        "camera_direction": camera_guidance,
        "negative_prompt": negative_prompt,
        "narration": " ".join(scene_data.get("narration", "").split()),
        "overlay_text": scene_data.get("overlay_text", []),
        "audio_effects": scene_data.get("audio_effects", [])
    }

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(repo_dir, "episodes", "episode-01-the-packet.yaml")
    
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found.")
        return
        
    data = load_episode(yaml_path)
    project_info = data.get("project", {})
    title = project_info.get("title", "Server Room B")
    episode = project_info.get("episode", "Episode 1 - The Packet")
    fmt = project_info.get("format", "Vertical 9:16")
    target_dur = project_info.get("target_duration", "60s")
    
    scenes = data.get("assets", {})
    
    optimized_scenes = []
    for sc_id, sc_content in scenes.items():
        opt = optimize_for_kling(sc_id, sc_content, fmt)
        optimized_scenes.append(opt)
        
    # Write JSON export
    out_json = os.path.join(repo_dir, "episodes", "kling_prompts_episode_01.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "project": title,
            "episode": episode,
            "format": fmt,
            "target_duration": target_dur,
            "scenes": optimized_scenes
        }, f, indent=2)
    print(f"Exported JSON prompts to: {out_json}")
    
    # Write Markdown cheat sheet
    out_md = os.path.join(repo_dir, "episodes", "kling_prompts_episode_01.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# {title} - {episode}\n\n")
        f.write(f"**Format:** {fmt} | **Target Duration:** {target_dur}\n\n")
        f.write("---\n\n")
        
        current_time = 0
        for s in optimized_scenes:
            start_t = f"{current_time//60:02d}:{current_time%60:02d}"
            current_time += s["target_duration_seconds"]
            end_t = f"{current_time//60:02d}:{current_time%60:02d}"
            
            f.write(f"### {s['scene_id'].upper()} ({start_t} - {end_t} | {s['target_duration_seconds']}s)\n\n")
            f.write(f"- **Kling Prompt:**\n> `{s['kling_prompt']}`\n\n")
            f.write(f"- **Camera Direction:** {s['camera_direction']}\n")
            f.write(f"- **Kling Length:** {s['kling_duration_seconds']}s\n")
            f.write(f"- **Narration:** *\"{s['narration']}\"*\n")
            if s['overlay_text']:
                f.write(f"- **Overlay Text:** {', '.join([f'`{t}`' for t in s['overlay_text']])}\n")
            f.write(f"- **Negative Prompt:** `{s['negative_prompt']}`\n\n")
            f.write("---\n\n")
            
    print(f"Exported Markdown prompt guide to: {out_md}")

if __name__ == "__main__":
    main()
