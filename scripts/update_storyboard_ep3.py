import os
import shutil

storyboard_path = "storyboard.html"
with open(storyboard_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Ep 3 tab button
target_tab = '''          <button id="tabEp2" onclick="switchEpisode('ep2')" class="px-3 py-1 rounded-lg font-semibold transition-all text-rose-400 hover:text-rose-300 flex items-center gap-1">
            <span>⚡</span>
            <span>Ep 2: Force Quit (67s)</span>
          </button>'''

replacement_tab = '''          <button id="tabEp2" onclick="switchEpisode('ep2')" class="px-3 py-1 rounded-lg font-semibold transition-all text-rose-400 hover:text-rose-300 flex items-center gap-1">
            <span>⚡</span>
            <span>Ep 2: Force Quit (67s)</span>
          </button>
          <button id="tabEp3" onclick="switchEpisode('ep3')" class="px-3 py-1 rounded-lg font-semibold transition-all text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
            <span>⚡</span>
            <span>Ep 3: Link Stage (78s)</span>
          </button>'''

if target_tab in content:
    content = content.replace(target_tab, replacement_tab, 1)
    print("Added Ep 3 Tab Button.")
else:
    print("Warning: target_tab not found")

# 2. Add Ep 3 download links
target_downloads = '''            <a href="episodes/episode-02-force-quit.mp4" download class="text-rose-400 hover:text-rose-300 font-bold">Ep 2 (19.0 MB)</a>
            <span>•</span>
            <a href="episodes/chapter-01-complete-directors-cut.mp4" download class="text-purple-400 hover:text-purple-300 font-bold">Director Cut (37.3 MB)</a>'''

replacement_downloads = '''            <a href="episodes/episode-02-force-quit.mp4" download class="text-rose-400 hover:text-rose-300 font-bold">Ep 2 (19.0 MB)</a>
            <span>•</span>
            <a href="episodes/episode-03-link-stage.mp4" download class="text-emerald-400 hover:text-emerald-300 font-bold">Ep 3 (6.9 MB)</a>
            <span>•</span>
            <a href="episodes/chapter-01-complete-directors-cut.mp4" download class="text-purple-400 hover:text-purple-300 font-bold">Director Cut (37.3 MB)</a>'''

if target_downloads in content:
    content = content.replace(target_downloads, replacement_downloads, 1)
    print("Added Ep 3 Download Link.")
else:
    print("Warning: target_downloads not found")

# 2b. Add Ep 3 Covers in covers bar
target_covers = '''          <a href="episodes/thumbnail_directors_cut.jpg" download class="text-purple-400 hover:text-purple-300 underline font-bold">DirCut 9:16</a>
          <span class="text-slate-600">•</span>
          <a href="episodes/thumbnail_directors_cut_16x9.jpg" download class="text-purple-400 hover:text-purple-300 underline font-bold">DirCut 16:9</a>'''

replacement_covers = '''          <a href="episodes/thumbnail_episode_03.jpg" download class="text-emerald-400 hover:text-emerald-300 underline font-bold">Ep3 9:16</a>
          <span class="text-slate-600">•</span>
          <a href="episodes/thumbnail_episode_03_16x9.jpg" download class="text-emerald-400 hover:text-emerald-300 underline font-bold">Ep3 16:9</a>
          <span class="text-slate-600">•</span>
          <a href="episodes/thumbnail_directors_cut.jpg" download class="text-purple-400 hover:text-purple-300 underline font-bold">DirCut 9:16</a>
          <span class="text-slate-600">•</span>
          <a href="episodes/thumbnail_directors_cut_16x9.jpg" download class="text-purple-400 hover:text-purple-300 underline font-bold">DirCut 16:9</a>'''

if target_covers in content:
    content = content.replace(target_covers, replacement_covers, 1)
    print("Added Ep 3 Covers.")
else:
    print("Warning: target_covers not found")

# 3. Add scenesEpisode3 definition
scenes_ep3_code = '''    const scenesEpisode3 = [
      {
        id: "scene_01",
        num: 1,
        title: "The Circular Buffer",
        duration: 9.0,
        startTime: 0,
        endTime: 9.0,
        timecode: "00:00 - 00:09.0",
        camera: "Tracking dolly ahead of sprinting engineer, subtle frame judder as corridor geometry repeats",
        prompt: "First-person perspective running through endless dark industrial data center corridor with repeating doors and flickering emergency sodium lights, wall textures degenerating into low poly pixelated surfaces, cinematic cyber horror, 35mm lens, photorealistic 8k",
        narration: "The corridor didn't end; it looped. With every pass, the walls rendered at lower resolution as the system ran out of memory.",
        overlay: ["TOPOLOGY: CIRCULAR_BUFFER_0x03", "LOD: AGGRESSIVE_CULLING_ACTIVE"],
        badge: "EP3 SCENE 01: CIRCULAR BUFFER",
        visualType: "servers",
        sfx: "glitch",
        audioSrc: "audio/narration_ep3/scene_01_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_02",
        num: 2,
        title: "Retinal Burn-in",
        duration: 9.8,
        startTime: 9.0,
        endTime: 18.8,
        timecode: "00:09.0 - 00:18.8",
        camera: "Extreme macro push into human eye, reflection of glowing terminal characters etched across iris",
        prompt: "Extreme macro close-up of brown human eye, dilated pupil reflecting sharp glowing green terminal code COMPILING USER 41 percent, chromatic aberration on eyelid, sweating brow, cinematic suspense lighting, photorealistic 8k",
        narration: "Compiling User Abhrankan, forty-one percent. The text no longer printed on the monitors. It burned directly into his retina.",
        overlay: ["COMPILING USER_ABHRANKAN... 41%", "DISPLAY: RETINAL_BURNOUT_L0"],
        badge: "EP3 SCENE 02: RETINAL BURN-IN",
        visualType: "eye_glitch",
        sfx: "shriek",
        audioSrc: "audio/narration_ep3/scene_02_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_03",
        num: 3,
        title: "The MDF Ingress",
        duration: 9.8,
        startTime: 18.8,
        endTime: 28.6,
        timecode: "00:18.8 - 00:28.6",
        camera: "Low-angle wide shot looking up at towering Cisco backbone server rack, cold volumetric fog rising from raised floor tiles",
        prompt: "Wide cinematic interior of freezing dark server vault, cold cyan fog along floor, towering black server rack filled with heavy Cisco enterprise switches, thousands of rapid blinking blue and amber fiber LEDs, cinematic sci-fi atmosphere",
        narration: "He breaks into the Main Distribution Frame. Here, the core Cisco backbone switch is still running on bare metal, untouched by the compiler.",
        overlay: ["NODE: MDF-CORE-SW01", "STATUS: BARE_METAL_RUNNING"],
        badge: "EP3 SCENE 03: MDF INGRESS",
        visualType: "servers",
        sfx: "hum",
        audioSrc: "audio/narration_ep3/scene_03_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_04",
        num: 4,
        title: "Serial Interface Hook",
        duration: 9.4,
        startTime: 28.6,
        endTime: 38.0,
        timecode: "00:28.6 - 00:38.0",
        camera: "Macro tracking shot of serial console cable clicking into laptop port, whip-pan to rear wall where doorway disappears into void",
        prompt: "Macro close-up shot of hands with trailing ghost polygon lag plugging thick light-blue console cable into rugged laptop in dark server room, terminal screen flashes green MDF-CORE-SW01 prompt, in background solid door melts into flat gray wall",
        narration: "Latency spikes to one hundred and fifty milliseconds. He plugs into the serial console as the exit behind him completely vanishes.",
        overlay: ["$ screen /dev/ttyUSB0 115200", "LATENCY: +150ms [DOOR CULLED]"],
        badge: "EP3 SCENE 04: SERIAL HOOK",
        visualType: "engineer",
        sfx: "keystroke",
        audioSrc: "audio/narration_ep3/scene_04_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_05",
        num: 5,
        title: "8-Bit VGA Snapping",
        duration: 9.6,
        startTime: 38.0,
        endTime: 47.6,
        timecode: "00:38.0 - 00:47.6",
        camera: "POV view of server room rapidly pixelating, color channels crushing into retro 8-bit VGA quantization",
        prompt: "POV looking at server rack as reality suddenly degrades into harsh 8-bit VGA dithering and 256 color palette, geometric crushing, glitched CRT scanlines, surreal cyber horror, atmospheric lighting",
        narration: "Sixty-seven percent. His vision drops from true color to harsh eight-bit VGA. The compiler begins overwriting his memories.",
        overlay: ["COMPILING USER_ABHRANKAN... 67%", "COLOR_DEPTH: 8-BIT_VGA_PALETTE"],
        badge: "EP3 SCENE 05: 8-BIT DITHERING",
        visualType: "memory_dash",
        sfx: "glitch",
        audioSrc: "audio/narration_ep3/scene_05_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_06",
        num: 6,
        title: "Hardware Access-Control List",
        duration: 9.6,
        startTime: 47.6,
        endTime: 57.2,
        timecode: "00:47.6 - 00:57.2",
        camera: "Tense medium side profile of young Indian software engineer typing with one hand while left arm is locked rigid, veins faintly glowing neon blue",
        prompt: "Cinematic side angle of male software engineer typing frantically on backlit keyboard with right hand, left arm locked rigid and trembling, cyan glowing cybernetic veins on forearm, cold terminal glow on sweaty face, intense drama",
        narration: "His left arm locks in a rigid spasm as foreign drivers load into his nerves. With one hand, he writes a hardware access control list.",
        overlay: ["deny udp any any eq 8080", "deny ip host 0.0.0.0 any", "DRIVER_HOOK: NERVOUS_SYS"],
        badge: "EP3 SCENE 06: HARDWARE ACL",
        visualType: "engineer",
        sfx: "pulse",
        audioSrc: "audio/narration_ep3/scene_06_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_07",
        num: 7,
        title: "The Timeless 0ms Frame",
        duration: 9.6,
        startTime: 57.2,
        endTime: 66.8,
        timecode: "00:57.2 - 01:06.8",
        camera: "Extreme slow motion push into finger slamming mechanical keyboard Enter key, visual reality freezing solid in mid-air",
        prompt: "Macro shot of index finger pressing Enter key on mechanical keyboard, surrounding dust motes and air frozen completely motionless in time, extreme stillness, cold blue and red lighting, cinematic depth of field",
        narration: "Eighty-nine percent. He binds the firewall and strikes Enter. The fans die. Time freezes to zero milliseconds.",
        overlay: ["interface Gi0/1: ip access-group in", "TIMESTEP: 0.00ms [CLOCK HALT]"],
        badge: "EP3 SCENE 07: 0ms CLOCK HALT",
        visualType: "frozen_cursor",
        sfx: "alarm",
        audioSrc: "audio/narration_ep3/scene_07_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_08",
        num: 8,
        title: "Connection Reset by Peer",
        duration: 11.2,
        startTime: 66.8,
        endTime: 78.0,
        timecode: "01:06.8 - 01:18.0",
        camera: "Terminal text snap, then wide pull back showing engineer slumped against server rack looking at concrete door frame permanently misaligned by 3 inches",
        prompt: "Wide cinematic shot of exhausted software engineer sitting on floor leaning against server rack in dark server room, green digital rain fading, in background concrete doorway has returned but cinder blocks are visibly misaligned and jagged by three inches, dramatic atmospheric thriller",
        narration: "Connection reset by peer. The packet is dropped. But the doorway returns misaligned by three inches. The bug in reality remains.",
        overlay: ["%ACL-I-APPLIED: Connection reset by peer", "SECTOR_FAULT: +3.0in OFFSET", "TO BE CONTINUED IN CHAPTER 4"],
        badge: "EP3 SCENE 08: RESET BY PEER",
        visualType: "packet_stream",
        sfx: "shriek",
        audioSrc: "audio/narration_ep3/scene_08_narration.wav",
        aiRender: ""
      }
    ];

    const episodesConfig = {'''

if "const episodesConfig = {" in content:
    content = content.replace("const episodesConfig = {", scenes_ep3_code, 1)
    print("Added scenesEpisode3.")
else:
    print("Warning: const episodesConfig = { not found")

# 4. Add ep3 to episodesConfig
target_ep2_cfg = '''      ep2: {
        title: "Episode 2 — Force Quit (Chapter 2)",
        videoSrc: "episodes/episode-02-force-quit.mp4",
        size: "19.0 MB",
        srt: "subtitles/episode-02-force-quit.srt",
        vtt: "subtitles/episode-02-force-quit.vtt",
        yaml: "episodes/episode-02-force-quit.yaml",
        duration: 67,
        scenes: scenesEpisode2
      }
    };'''

replacement_ep3_cfg = '''      ep2: {
        title: "Episode 2 — Force Quit (Chapter 2)",
        videoSrc: "episodes/episode-02-force-quit.mp4",
        size: "19.0 MB",
        srt: "subtitles/episode-02-force-quit.srt",
        vtt: "subtitles/episode-02-force-quit.vtt",
        yaml: "episodes/episode-02-force-quit.yaml",
        duration: 67,
        scenes: scenesEpisode2
      },
      ep3: {
        title: "Episode 3 — Link Stage (Chapter 3)",
        videoSrc: "episodes/episode-03-link-stage.mp4",
        size: "6.9 MB",
        srt: "subtitles/episode-03-link-stage.srt",
        vtt: "subtitles/episode-03-link-stage.vtt",
        yaml: "episodes/episode-03-link-stage.yaml",
        duration: 78,
        scenes: scenesEpisode3
      }
    };'''

if target_ep2_cfg in content:
    content = content.replace(target_ep2_cfg, replacement_ep3_cfg, 1)
    print("Added ep3 to episodesConfig.")
else:
    print("Warning: target_ep2_cfg not found")

# 5. Update switchEpisode loop for tabs styling
target_switch_loop = '''      // Update Tabs styling
      ["part1", "part2", "full", "ep2"].forEach(k => {
        const btn = document.getElementById(k === "part1" ? "tabPart1" : (k === "part2" ? "tabPart2" : (k === "full" ? "tabFull" : "tabEp2")));'''

replacement_switch_loop = '''      // Update Tabs styling
      ["part1", "part2", "full", "ep2", "ep3"].forEach(k => {
        const btn = document.getElementById(k === "part1" ? "tabPart1" : (k === "part2" ? "tabPart2" : (k === "full" ? "tabFull" : (k === "ep2" ? "tabEp2" : "tabEp3"))));'''

if target_switch_loop in content:
    content = content.replace(target_switch_loop, replacement_switch_loop, 1)
    print("Updated switchEpisode tab styling loop.")
else:
    print("Warning: target_switch_loop not found")

# Save updated storyboard.html
with open(storyboard_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved storyboard.html.")

# Copy to storyboard/index.html
os.makedirs("storyboard", exist_ok=True)
shutil.copyfile("storyboard.html", "storyboard/index.html")
print("Mirrored to storyboard/index.html.")

# Also mirror to brain artifact if exists
artifact_dir = r"C:\Users\Abhrankan\.gemini\antigravity\brain\946ca535-00ce-4883-aa38-de850d0752db"
if os.path.exists(artifact_dir):
    shutil.copyfile("storyboard.html", os.path.join(artifact_dir, "storyboard_player.html"))
    print("Mirrored to brain artifact storyboard_player.html.")
