"""
Updates storyboard.html to support:
- Multi-Episode / Multi-Part Switcher:
  * Part 1: The Packet (0-60s)
  * Part 2: Reality Uninstall (0-60s)
  * Complete Director's Cut (0-120s, 16 Scenes)
- Author credit: Story & Screenplay by Abhrankan Chakrabarti
- Direct download links for all 3 master videos and subtitles
"""

import os

def update():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sb_path = os.path.join(repo_dir, "storyboard.html")
    with open(sb_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Title and Subtitle in Header
    old_h1_block = """      <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight mt-1.5 text-slate-50">
        Server Room B: <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-cyan-300">Episode 1 — The Packet</span>
      </h1>
      <p class="text-xs md:text-sm text-slate-400 mt-1">
        Hard Sci-Fi Adaptation by Abhrankan Chakrabarti • Real-Time Visual Simulator & AI Prompt Director
      </p>"""

    new_h1_block = """      <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight mt-1.5 text-slate-50">
        Server Room B: <span id="headerEpisodeTitle" class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-cyan-300">Chapter 1 — Out of Memory</span>
      </h1>
      <p class="text-xs md:text-sm text-slate-400 mt-1">
        Story & Screenplay by <strong class="text-sky-300 font-semibold">Abhrankan Chakrabarti</strong> • Interactive Storyboard & Video Player
      </p>
      
      <!-- Episode / Part Selector Tabs -->
      <div class="flex items-center gap-2 mt-3">
        <span class="text-xs font-mono text-slate-400 uppercase tracking-wider">Episode Cut:</span>
        <div class="inline-flex p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono">
          <button id="tabPart1" onclick="switchEpisode('part1')" class="px-3 py-1 rounded-lg font-semibold transition-all bg-sky-600 text-white shadow-sm">
            Part 1: The Packet (60s)
          </button>
          <button id="tabPart2" onclick="switchEpisode('part2')" class="px-3 py-1 rounded-lg font-semibold transition-all text-slate-400 hover:text-slate-200">
            Part 2: Reality Uninstall (60s)
          </button>
          <button id="tabFull" onclick="switchEpisode('full')" class="px-3 py-1 rounded-lg font-semibold transition-all text-purple-400 hover:text-purple-300 flex items-center gap-1">
            <span>🎬</span>
            <span>Director's Cut (120s)</span>
          </button>
        </div>
      </div>"""

    if old_h1_block in html:
        html = html.replace(old_h1_block, new_h1_block)
        print("Updated Header H1 & Tabs")

    # 2. Update Production Assets Bar
    old_assets_bar = """      <!-- Asset Downloads Bar -->
      <div class="w-full max-w-[360px] mt-3 p-3 bg-slate-900/80 border border-slate-800 rounded-xl text-xs font-mono flex flex-col gap-2 text-slate-300 shadow-md">
        <div class="flex items-center justify-between">
          <span class="text-slate-400 font-bold">Production Assets:</span>
          <a href="episodes/episode-01-the-packet.mp4" download class="text-emerald-400 font-bold hover:text-emerald-300 underline flex items-center gap-1">
            <span>📥</span>
            <span>Download Master MP4 (17.6 MB - Full 8-Scene Film)</span>
          </a>
        </div>
        <div class="flex flex-wrap items-center justify-between pt-1 border-t border-slate-800 text-slate-400 text-xs">
          <span>Specs:</span>
          <a href="subtitles/episode-01.srt" download class="hover:text-sky-300 underline">.SRT</a>
          <a href="subtitles/episode-01.vtt" download class="hover:text-sky-300 underline">.VTT</a>
          <a href="episodes/kling_prompts_episode_01.json" download class="hover:text-sky-300 underline">.JSON</a>
          <a href="episodes/episode-01-the-packet.yaml" download class="hover:text-sky-300 underline">.YAML</a>
          <a href="episodes/kling_renders/scene_01.mp4" download class="text-amber-400 hover:text-amber-300 underline">Scene 1 Kling AI (5MB) ↗</a>
          <a href="https://invideo.io/@abhrankan/server-room-b-episode-1/tree/main/seq-1.1" target="_blank" class="text-purple-400 hover:text-purple-300 underline">InVideo Timeline ↗</a>
        </div>
        <div class="flex items-center justify-between pt-1 border-t border-slate-800/80 text-slate-400 text-[11px]">
          <span>InVideo Cloud:</span>
          <a href="https://invideo.io/@abhrankan/server-room-b-episode-1/notebook/seq-16.1" target="_blank" class="text-sky-400 hover:text-sky-300 underline">Asset seq-16.1 ↗</a>
          <span class="text-slate-600">•</span>
          <a href="https://invideo.io/@abhrankan/server-room-b-episode-1/notebook/seq-17.1" target="_blank" class="text-purple-400 hover:text-purple-300 underline">Export Stream ↗</a>
        </div>
      </div>"""

    new_assets_bar = """      <!-- Asset Downloads Bar -->
      <div class="w-full max-w-[360px] mt-3 p-3 bg-slate-900/80 border border-slate-800 rounded-xl text-xs font-mono flex flex-col gap-2 text-slate-300 shadow-md">
        <div class="flex items-center justify-between">
          <span class="text-slate-400 font-bold">Production Assets:</span>
          <span class="text-[11px] text-sky-400 font-semibold" id="activeAssetLabel">Part 1 (17.6 MB)</span>
        </div>
        
        <!-- Video Download Options -->
        <div class="flex flex-col gap-1.5 pt-1 border-t border-slate-800 text-[11px]">
          <a id="downloadActiveMp4" href="episodes/episode-01-the-packet.mp4" download class="text-emerald-400 font-bold hover:text-emerald-300 underline flex items-center justify-between">
            <span>📥 Download Active Video MP4</span>
            <span id="activeVideoSizeBadge">17.6 MB</span>
          </a>
          <div class="flex items-center justify-between text-slate-400 text-[10px]">
            <a href="episodes/episode-01-the-packet.mp4" download class="hover:text-emerald-300">Part 1 (17.6 MB)</a>
            <span>•</span>
            <a href="episodes/episode-01-part-02.mp4" download class="hover:text-emerald-300">Part 2 (19.7 MB)</a>
            <span>•</span>
            <a href="episodes/chapter-01-complete-directors-cut.mp4" download class="text-purple-400 hover:text-purple-300 font-bold">Director Cut (37.3 MB)</a>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between pt-1 border-t border-slate-800 text-slate-400 text-xs">
          <span>Specs:</span>
          <a id="specSrtLink" href="subtitles/episode-01.srt" download class="hover:text-sky-300 underline">.SRT</a>
          <a id="specVttLink" href="subtitles/episode-01.vtt" download class="hover:text-sky-300 underline">.VTT</a>
          <a id="specYamlLink" href="episodes/episode-01-the-packet.yaml" download class="hover:text-sky-300 underline">.YAML</a>
          <a href="episodes/kling_prompts_episode_01.json" download class="hover:text-sky-300 underline">.JSON</a>
          <a href="episodes/kling_renders/scene_01.mp4" download class="text-amber-400 hover:text-amber-300 underline">Scene 1 Kling AI (5MB) ↗</a>
        </div>
        <div class="flex items-center justify-between pt-1 border-t border-slate-800/80 text-slate-400 text-[11px]">
          <span>InVideo Cloud:</span>
          <a href="https://invideo.io/@abhrankan/server-room-b-episode-1/tree/main/seq-1.1" target="_blank" class="text-purple-400 hover:text-purple-300 underline">Studio Timeline ↗</a>
          <span class="text-slate-600">•</span>
          <a href="https://invideo.io/@abhrankan/server-room-b-episode-1/notebook/seq-17.1" target="_blank" class="text-sky-400 hover:text-sky-300 underline">Export Stream ↗</a>
        </div>
      </div>"""

    if old_assets_bar in html:
        html = html.replace(old_assets_bar, new_assets_bar)
        print("Updated Production Assets Bar")

    with open(sb_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Storyboard HTML updated successfully!")

if __name__ == "__main__":
    update()
