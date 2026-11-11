"""
Server Room B - 2.5D Cinematic Keyframe Animator
Generates fluid, cinematic 9:16 video shots from photorealistic keyframes with
dynamic camera dolly, zoom, lens breathing, film grain, and VFX.
"""

import os
import math
import numpy as np
from PIL import Image, ImageEnhance
import cv2

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYFRAMES_DIR = os.path.join(REPO_DIR, "episodes", "keyframes")
RENDERS_DIR = os.path.join(REPO_DIR, "episodes", "kling_renders")

def apply_film_grain(img_cv, intensity=0.025):
    """Add subtle 35mm cinema film grain to frame."""
    noise = np.random.normal(0, intensity * 255, img_cv.shape).astype(np.float32)
    noisy = np.clip(img_cv.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return noisy

def apply_chromatic_aberration(img_cv, shift_px=3):
    """Split color channels slightly for sci-fi lens dispersion."""
    if shift_px <= 0:
        return img_cv
    b, g, r = cv2.split(img_cv)
    h, w = img_cv.shape[:2]
    M_r = np.float32([[1, 0, shift_px], [0, 1, 0]])
    M_b = np.float32([[1, 0, -shift_px], [0, 1, 0]])
    r_shifted = cv2.warpAffine(r, M_r, (w, h), borderMode=cv2.BORDER_REFLECT)
    b_shifted = cv2.warpAffine(b, M_b, (w, h), borderMode=cv2.BORDER_REFLECT)
    return cv2.merge([b_shifted, g, r_shifted])

def render_shot(input_image_path, output_video_path, duration=6.0, fps=30, shot_type="dolly_in", target_w=720, target_h=1280):
    """
    Renders high-quality 9:16 vertical video from a high-resolution keyframe
    with smooth sub-pixel camera interpolation and cinematic VFX.
    """
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input image not found: {input_image_path}")

    src_img = Image.open(input_image_path).convert("RGB")
    src_w, src_h = src_img.size
    
    # Ensure source image covers the 9:16 frame with bleed margin for camera movement
    scale_factor = max((target_w * 1.25) / src_w, (target_h * 1.25) / src_h)
    new_w = int(src_w * scale_factor)
    new_h = int(src_h * scale_factor)
    src_img = src_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (target_w, target_h))
    
    print(f"🎬 Animating shot '{shot_type}': {total_frames} frames ({duration}s @ {fps}fps) -> {os.path.basename(output_video_path)}")
    
    cx_src = new_w / 2.0
    cy_src = new_h / 2.0
    
    for f in range(total_frames):
        t_norm = f / float(total_frames)
        
        # Camera motion math
        if shot_type == "dolly_in":
            # Smooth ease-in-out zoom
            zoom = 1.0 + 0.16 * (math.sin(t_norm * math.pi / 2.0))
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shift_x = math.sin(t_norm * 2.0 * math.pi) * 6.0
            shift_y = (t_norm * 12.0)
            
        elif shot_type == "dramatic_push":
            # Accelerating dramatic push-in
            zoom = 1.0 + 0.22 * (t_norm ** 1.3)
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shift_x = math.sin(t_norm * math.pi) * 4.0
            shift_y = -t_norm * 15.0
            
        elif shot_type == "panic_zoom":
            # Crash zoom into screen with camera shake
            zoom = 1.0 + 0.32 * (t_norm ** 1.2)
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shake = (t_norm > 0.5)
            shift_x = (np.random.rand() - 0.5) * 8.0 if shake else 0
            shift_y = (np.random.rand() - 0.5) * 8.0 if shake else 0
            
        elif shot_type == "slow_drift":
            # Subtle parallax float
            zoom = 1.04 + 0.08 * math.sin(t_norm * math.pi)
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shift_x = math.sin(t_norm * math.pi) * 12.0
            shift_y = math.cos(t_norm * math.pi) * 8.0
            
        elif shot_type == "static_freeze":
            # Slow steady zoom, then dead static
            if t_norm < 0.4:
                zoom = 1.0 + 0.06 * (t_norm / 0.4)
            else:
                zoom = 1.06
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shift_x = 0
            shift_y = 0
            
        elif shot_type == "macro_glitch":
            # Eye macro dilation & reality jitter
            zoom = 1.06 + 0.24 * (t_norm ** 1.3)
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            jitter = (t_norm > 0.6) and (f % 3 == 0)
            shift_x = (np.random.rand() - 0.5) * 12.0 if jitter else 0
            shift_y = (np.random.rand() - 0.5) * 12.0 if jitter else 0
            
        else:
            zoom = 1.0 + 0.10 * t_norm
            crop_w = target_w / zoom
            crop_h = target_h / zoom
            shift_x = 0
            shift_y = 0
            
        x1 = cx_src + shift_x - crop_w / 2.0
        y1 = cy_src + shift_y - crop_h / 2.0
        x2 = x1 + crop_w
        y2 = y1 + crop_h
        
        # Crop & resize to target viewport
        frame_pil = src_img.crop((x1, y1, x2, y2)).resize((target_w, target_h), Image.Resampling.BILINEAR)
        
        # Screen glow & subtle flicker
        flicker = 1.0 + 0.02 * math.sin(f * 0.9)
        if abs(flicker - 1.0) > 0.005:
            frame_pil = ImageEnhance.Brightness(frame_pil).enhance(flicker)
            
        # Convert to OpenCV BGR
        frame_cv = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        
        # Apply sci-fi VFX
        if shot_type in ["panic_zoom", "macro_glitch"]:
            aberration_px = int(t_norm * 5.0) if shot_type == "macro_glitch" else int(t_norm * 3.5)
            frame_cv = apply_chromatic_aberration(frame_cv, shift_px=aberration_px)
            
        # Subtle cinema film grain
        frame_cv = apply_film_grain(frame_cv, intensity=0.02)
        
        out.write(frame_cv)
        
    out.release()
    print(f"✓ Saved: {output_video_path} ({os.path.getsize(output_video_path)/(1024*1024):.2f} MB)")

def batch_animate_all():
    """Batch animate all keyframes into scene videos."""
    shots_spec = [
        {"scene_id": "scene_02", "duration": 8.0, "type": "dramatic_push"},
        {"scene_id": "scene_03", "duration": 6.0, "type": "dolly_in"},
        {"scene_id": "scene_04", "duration": 8.0, "type": "slow_drift"},
        {"scene_id": "scene_05", "duration": 8.0, "type": "static_freeze"},
        {"scene_id": "scene_06", "duration": 8.0, "type": "dramatic_push"},
        {"scene_id": "scene_07", "duration": 10.0, "type": "panic_zoom"},
        {"scene_id": "scene_08", "duration": 6.0, "type": "macro_glitch"},
    ]
    
    print("\n" + "="*70)
    print("🚀 BATCH ANIMATING 2.5D PHOTOREALISTIC SHOTS (SCENES 2 - 8)")
    print("="*70)
    
    for shot in shots_spec:
        sc_id = shot["scene_id"]
        in_img = os.path.join(KEYFRAMES_DIR, f"{sc_id}.jpg")
        out_vid = os.path.join(RENDERS_DIR, f"{sc_id}.mp4")
        if os.path.exists(in_img):
            render_shot(in_img, out_vid, duration=shot["duration"], fps=30, shot_type=shot["type"])
        else:
            print(f"Skipping {sc_id}: image not found ({in_img})")
            
    print("="*70 + "\nAll shots rendered successfully!\n")

if __name__ == "__main__":
    batch_animate_all()
