"""
Server Room B - Kling AI Video Generation Pipeline
Automated scene dispatch, status polling, and rendering asset manager.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_FILE = os.path.join(REPO_DIR, "episodes", "kling_prompts_episode_01.json")
OUTPUT_DIR = os.path.join(REPO_DIR, "episodes", "kling_renders")
TASKS_FILE = os.path.join(OUTPUT_DIR, "tasks.json")
ENV_FILE = os.path.join(REPO_DIR, ".env")

def load_env():
    """Load configuration from .env or OS environment variables."""
    config = {
        "KLINGAI_API_KEY": os.environ.get("KLINGAI_API_KEY", ""),
        "KLINGAI_BASE_URL": os.environ.get("KLINGAI_BASE_URL", "https://api-singapore.klingai.com")
    }
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        config[k] = v
    return config

def load_prompts():
    """Load scene prompts specification."""
    if not os.path.exists(PROMPTS_FILE):
        raise FileNotFoundError(f"Prompts file not found at: {PROMPTS_FILE}")
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_tasks():
    """Load persistent tasks registry."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_tasks(tasks):
    """Save persistent tasks registry."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def make_api_request(endpoint, payload=None, method="GET", api_key=None, base_url=None):
    """Execute authenticated HTTP request to Kling AI API."""
    if not api_key:
        raise ValueError("Missing KLINGAI_API_KEY. Provide it in .env or via environment variable.")
    
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return json.loads(err_body)
        except Exception:
            raise RuntimeError(f"HTTP Error {e.code}: {err_body}")
    except Exception as e:
        raise RuntimeError(f"Network error connecting to {url}: {e}")

def check_balance(api_key, base_url):
    """Query account billing and balance information."""
    now_ms = int(time.time() * 1000)
    start_ms = now_ms - (30 * 24 * 3600 * 1000)
    payload = {"start_time": start_ms, "end_time": now_ms}
    res = make_api_request("account/billing/balance", payload=payload, method="POST", api_key=api_key, base_url=base_url)
    return res

def list_scenes():
    """Display summary of all 8 scenes configured in Kling format."""
    data = load_prompts()
    tasks = load_tasks()
    
    print("\n" + "="*80)
    print(f"🎬 {data.get('project', 'Project')} — {data.get('episode', 'Episode')}")
    print(f"Format: {data.get('format')} | Target Duration: {data.get('target_duration')}")
    print("="*80)
    
    for s in data.get("scenes", []):
        sc_id = s["scene_id"]
        dur = s["kling_duration_seconds"]
        task_info = tasks.get(sc_id, {})
        status = task_info.get("status", "NOT_GENERATED")
        task_id = task_info.get("task_id", "-")
        
        print(f"\n▶ [{sc_id.upper()}] (Kling duration: {dur}s | Status: {status})")
        print(f"   Camera: {s.get('camera_direction', '-')}")
        print(f"   Narration: \"{s.get('narration', '-')}\"")
        if task_id != "-":
            print(f"   Task ID: {task_id}")
        prompt_snippet = s.get("kling_prompt", "")
        if len(prompt_snippet) > 120:
            prompt_snippet = prompt_snippet[:117] + "..."
        print(f"   Prompt: {prompt_snippet}")
    print("\n" + "="*80 + "\n")

def submit_scene(scene_id, model="kling-v2-6", mode="std", api_key=None, base_url=None):
    """Submit a text2video generation job for a specific scene."""
    data = load_prompts()
    scene = None
    for s in data.get("scenes", []):
        if s["scene_id"] == scene_id or s["scene_id"].endswith(f"_{scene_id}") or s["scene_id"] == f"scene_{int(scene_id):02d}":
            scene = s
            break
            
    if not scene:
        raise ValueError(f"Scene identifier '{scene_id}' not found in prompts specification.")
        
    actual_sc_id = scene["scene_id"]
    dur = scene["kling_duration_seconds"]
    
    payload = {
        "model_name": model,
        "prompt": scene["kling_prompt"],
        "negative_prompt": scene.get("negative_prompt", "blurry, low quality, distortion, cartoon, 3d render"),
        "aspect_ratio": "9:16",
        "duration": str(dur),
        "mode": mode
    }
    
    print(f"\nSubmitting [{actual_sc_id}] to Kling AI ({model}, mode={mode}, duration={dur}s, 9:16)...")
    res = make_api_request("v1/videos/text2video", payload=payload, method="POST", api_key=api_key, base_url=base_url)
    
    code = res.get("code")
    if code == 0:
        task_data = res.get("data", {})
        task_id = task_data.get("task_id")
        print(f"SUCCESS! Task submitted successfully.")
        print(f"Task ID: {task_id}")
        
        tasks = load_tasks()
        tasks[actual_sc_id] = {
            "task_id": task_id,
            "scene_id": actual_sc_id,
            "duration": dur,
            "model": model,
            "mode": mode,
            "status": "submitted",
            "submitted_at": time.time(),
            "updated_at": time.time()
        }
        save_tasks(tasks)
        return task_id
    else:
        msg = res.get("message", "Unknown error")
        print(f"FAILED to submit task [{actual_sc_id}]: {msg} (code: {code})")
        if code == 1102:
            print("\n[!] Error 1102: 'Account balance not enough'")
            print("    The Kling AI Developer / Open Platform API requires an API Resource Pack.")
            print("    Note: Kling AI Web subscription credits (klingai.com) are separate from API platform units.")
            print("    To resolve: Log into your Kling AI Developer Console and add an API Video Resource Pack.\n")
        return None

def query_status(task_id, api_key=None, base_url=None):
    """Check current status of a generation task."""
    res = make_api_request(f"v1/videos/text2video/{task_id}", method="GET", api_key=api_key, base_url=base_url)
    return res

def watch_task(task_id, out_file=None, interval=15, api_key=None, base_url=None):
    """Poll a task until completion and download video upon success."""
    print(f"\nWatching task: {task_id} (polling every {interval}s)...")
    
    while True:
        res = query_status(task_id, api_key=api_key, base_url=base_url)
        if res.get("code") != 0:
            print(f"Error checking status: {res.get('message')} (code {res.get('code')})")
            return False
            
        data = res.get("data", {})
        status = data.get("task_status", "unknown").lower()
        print(f"[{time.strftime('%H:%M:%S')}] Task Status: {status.upper()}")
        
        # Update registry if task exists
        tasks = load_tasks()
        for sc_id, t_info in tasks.items():
            if t_info.get("task_id") == task_id:
                t_info["status"] = status
                t_info["updated_at"] = time.time()
                save_tasks(tasks)
                break
                
        if status == "succeed":
            videos = data.get("task_result", {}).get("videos", [])
            if not videos:
                print("Task succeeded but no video URL returned.")
                return False
                
            video_url = videos[0].get("url")
            print(f"\n🎉 Generation Finished! Video URL: {video_url}")
            
            if out_file:
                download_video(video_url, out_file)
            return True
            
        elif status == "failed":
            print(f"\n❌ Task failed: {data.get('task_status_msg', 'Unknown error')}")
            return False
            
        time.sleep(interval)

def download_video(url, out_path):
    """Download video asset from URL to local file."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    print(f"Downloading video to: {out_path} ...")
    urllib.request.urlretrieve(url, out_path)
    file_size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Saved: {out_path} ({file_size_mb:.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Server Room B - Kling AI Scene Generator")
    parser.add_argument("--balance", action="store_true", help="Check Kling API account balance & status")
    parser.add_argument("--list", action="store_true", help="List all 8 scenes and their generation status")
    parser.add_argument("--scene", type=str, help="Generate a specific scene by ID (e.g. scene_01 or 1)")
    parser.add_argument("--all", action="store_true", help="Generate all 8 scenes sequentially")
    parser.add_argument("--status", type=str, help="Query task status by task_id")
    parser.add_argument("--watch", type=str, help="Watch a task_id until completion and download output")
    parser.add_argument("--model", type=str, default="kling-v2-6", choices=["kling-v2-6", "kling-v3"], help="Kling model name (default: kling-v2-6)")
    parser.add_argument("--mode", type=str, default="std", choices=["std", "pro"], help="Generation quality tier (std=720p, pro=1080p)")
    args = parser.parse_args()
    
    env = load_env()
    api_key = env.get("KLINGAI_API_KEY")
    base_url = env.get("KLINGAI_BASE_URL", "https://api-singapore.klingai.com")
    
    if not api_key:
        print("ERROR: KLINGAI_API_KEY is not configured in .env or environment.")
        sys.exit(1)
        
    if args.balance:
        print(f"Connecting to Kling AI at {base_url}...")
        bal = check_balance(api_key, base_url)
        print("Balance Response:")
        print(json.dumps(bal, indent=2))
        return
        
    if args.list:
        list_scenes()
        return
        
    if args.status:
        st = query_status(args.status, api_key=api_key, base_url=base_url)
        print(json.dumps(st, indent=2))
        return
        
    if args.watch:
        out_file = os.path.join(OUTPUT_DIR, f"task_{args.watch}.mp4")
        watch_task(args.watch, out_file=out_file, api_key=api_key, base_url=base_url)
        return
        
    if args.scene:
        task_id = submit_scene(args.scene, model=args.model, mode=args.mode, api_key=api_key, base_url=base_url)
        if task_id:
            out_file = os.path.join(OUTPUT_DIR, f"{args.scene}.mp4")
            watch_task(task_id, out_file=out_file, api_key=api_key, base_url=base_url)
        return
        
    if args.all:
        data = load_prompts()
        print(f"Preparing batch generation for {len(data.get('scenes', []))} scenes...")
        for s in data.get("scenes", []):
            sc_id = s["scene_id"]
            task_id = submit_scene(sc_id, model=args.model, mode=args.mode, api_key=api_key, base_url=base_url)
            if not task_id:
                print(f"\n[!] Batch generation halted due to submission failure on {sc_id}.")
                return
            time.sleep(2)
        print("\nAll scenes submitted successfully. Run with --list to review tasks status.")
        return
        
    # Default behavior if no args: list scenes
    list_scenes()

if __name__ == "__main__":
    main()
