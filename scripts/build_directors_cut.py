import os
import subprocess
import imageio_ffmpeg

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    episodes_dir = os.path.join(repo_dir, "episodes")
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    ep1 = os.path.join(episodes_dir, "episode-01-the-packet.mp4")
    ep2 = os.path.join(episodes_dir, "episode-01-part-02.mp4")
    out_full = os.path.join(episodes_dir, "chapter-01-complete-directors-cut.mp4")
    
    concat_txt = os.path.join(episodes_dir, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.write(f"file '{ep1}'\nfile '{ep2}'\n")
        
    cmd = [ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", out_full]
    subprocess.run(cmd, check=True)
    
    if os.path.exists(concat_txt):
        os.remove(concat_txt)
        
    print(f"Rendered Complete Director's Cut: {out_full} ({os.path.getsize(out_full)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
