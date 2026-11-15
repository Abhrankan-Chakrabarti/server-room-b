"""
Updates storyboard.html with Episode 2: Force Quit tab, scenes, subtitles, and downloads.
"""

import os

def update():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sb_path = os.path.join(repo_dir, "storyboard.html")
    sb_idx = os.path.join(repo_dir, "storyboard", "index.html")

    with open(sb_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add Episode 2 Button to the Tab bar
    old_tabs = """          <button id="tabFull" onclick="switchEpisode('full')" class="px-3 py-1 rounded-lg font-semibold transition-all text-purple-400 hover:text-purple-300 flex items-center gap-1">
            <span>🎬</span>
            <span>Director's Cut (120s)</span>
          </button>"""

    new_tabs = """          <button id="tabFull" onclick="switchEpisode('full')" class="px-3 py-1 rounded-lg font-semibold transition-all text-purple-400 hover:text-purple-300 flex items-center gap-1">
            <span>🎬</span>
            <span>Director's Cut (120s)</span>
          </button>
          <button id="tabEp2" onclick="switchEpisode('ep2')" class="px-3 py-1 rounded-lg font-semibold transition-all text-rose-400 hover:text-rose-300 flex items-center gap-1">
            <span>⚡</span>
            <span>Ep 2: Force Quit</span>
          </button>"""

    if old_tabs in html and 'id="tabEp2"' not in html:
        html = html.replace(old_tabs, new_tabs)

    # 2. Add Episode 2 OST to Audio downloads bar
    old_audio_bar = """          <a href="audio/part2_2ms_stutter_sfx.mp3" download class="text-amber-400 hover:text-amber-300 underline">2ms SFX</a>"""
    new_audio_bar = """          <a href="audio/part2_2ms_stutter_sfx.mp3" download class="text-amber-400 hover:text-amber-300 underline">2ms SFX</a>
          <span class="text-slate-600">•</span>
          <a href="audio/episode_02_soundtrack.mp3" download class="text-rose-400 hover:text-rose-300 underline font-bold">Ep 2 OST MP3</a>"""

    if old_audio_bar in html and 'episode_02_soundtrack.mp3' not in html:
        html = html.replace(old_audio_bar, new_audio_bar)

    # 3. Add Episode 2 Thumbnail to Covers bar
    old_covers_bar = """          <a href="episodes/thumbnail_part2.jpg" download class="text-sky-400 hover:text-sky-300 underline">Part 2</a>"""
    new_covers_bar = """          <a href="episodes/thumbnail_part2.jpg" download class="text-sky-400 hover:text-sky-300 underline">Part 2</a>
          <span class="text-slate-600">•</span>
          <a href="episodes/thumbnail_episode_02.jpg" download class="text-rose-400 hover:text-rose-300 underline font-semibold">Ep 2 Cover</a>"""

    if old_covers_bar in html and 'thumbnail_episode_02.jpg' not in html:
        html = html.replace(old_covers_bar, new_covers_bar)

    # 4. Inject scenesEpisode2 definition right after scenesPart2
    scenes_ep2_code = """
    const scenesEpisode2 = [
      {
        id: "scene_01",
        num: 1,
        title: "Process Tree Inspection",
        duration: 7.0,
        startTime: 0,
        endTime: 7.0,
        timecode: "00:00 - 00:07",
        camera: "Over-the-shoulder macro dolly toward mechanical keyboard, subtle 47ms input lag stutter",
        prompt: "Close up over shoulder shot of an Indian software engineer sitting in a dark server room reaching for a backlit mechanical keyboard, hands have subtle translucent ghost polygon trails, terminal screen displays green and red code process tree, cinematic cyber horror, 35mm film grain, 8k resolution",
        narration: "Abhrankan's reflex wasn't flight. It was to isolate the process, kill it, and reclaim the resources.",
        overlay: ["PROCESS: BIOLOGICAL_COMPILER_v0x7F", "LATENCY: +47ms"],
        badge: "EP2 SCENE 01: PROCESS TREE",
        visualType: "terminal",
        sfx: "keystroke",
        audioSrc: "audio/narration_ep2/scene_01_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_02",
        num: 2,
        title: "The PID 1 Shell Error",
        duration: 7.0,
        startTime: 7.0,
        endTime: 14.0,
        timecode: "00:07 - 00:14",
        camera: "Slow push in on CRT/LCD terminal screen, phosphor glow reflecting in glasses",
        prompt: "Macro close up of dark terminal console monitor, green text flashing command sudo kill -9 then flashing bright red error message kill: (pid 1): Operation not permitted, realistic CRT scanlines, cinematic lighting, 8k",
        narration: "He types the kill command. The shell rejects it immediately: PID 1. You cannot kill the init process of reality.",
        overlay: ["$ sudo kill -9 $(pgrep -f BIOLOGICAL_COMPILER)", "kill: (pid 1): Operation not permitted"],
        badge: "EP2 SCENE 02: PID 1 DENIAL",
        visualType: "terminal",
        sfx: "alarm",
        audioSrc: "audio/narration_ep2/scene_02_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_03",
        num: 3,
        title: "SysRq Hardware Interrupt Ignored",
        duration: 7.0,
        startTime: 14.0,
        endTime: 21.0,
        timecode: "00:14 - 00:21",
        camera: "Side profile shot of engineer illuminated by cyan monitor glow, tense jawline, rapid typing",
        prompt: "Cinematic side profile of young male software engineer typing frantically on keyboard in dark server room, face illuminated by cold cyan terminal light, sweat on temple, dark atmosphere, suspense thriller, photorealistic",
        narration: "He forces a raw kernel reboot. Nothing. The kernel no longer answers to hardware interrupts from this side of existence.",
        overlay: ["$ echo b > /proc/sysrq-trigger", "[SYSRQ INTERFACE REMAPPED]"],
        badge: "EP2 SCENE 03: SYSRQ REMAPPED",
        visualType: "terminal",
        sfx: "keystroke",
        audioSrc: "audio/narration_ep2/scene_03_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_04",
        num: 4,
        title: "Demoted to Ring 3 & 60Hz Frame Lock",
        duration: 7.0,
        startTime: 21.0,
        endTime: 28.0,
        timecode: "00:21 - 00:28",
        camera: "Macro tracking shot across server rack glass door reflecting red system warnings",
        prompt: "Macro shot of server rack glass door reflecting bold red warning text: PRIVILEGE LEVEL DEMOTED TO RING_3, PHYSICS TIMESTEP 16.67ms FIXED, harsh amber and crimson emergency lighting, cinematic depth of field",
        narration: "A warning floods the room. His privilege level is demoted to userland. Physics locks to a fixed sixteen-millisecond loop.",
        overlay: ["WARN: PRIVILEGE DEMOTED TO RING_3", "INF: PHYSICS TIMESTEP 16.67ms FIXED"],
        badge: "EP2 SCENE 04: RING_3 DEMOTION",
        visualType: "terminal",
        sfx: "hum",
        audioSrc: "audio/narration_ep2/scene_04_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_05",
        num: 5,
        title: "Quantized Motion & Collision Crash",
        duration: 7.0,
        startTime: 28.0,
        endTime: 35.0,
        timecode: "00:28 - 00:35",
        camera: "POV juddering camera rotation, discrete frame stepping effect, chromatic aberration",
        prompt: "First person perspective of looking around server room with discrete juddering motion blur, glitched frame artifacts, server racks slightly displaced, cold volumetric fog, cinematic cyberpunk realism",
        narration: "Time becomes quantized. The universe wasn't being haunted... the runtime itself was breaking.",
        overlay: ["TIMESTEP: 16.67ms (60 FPS)", "COLLISION: isTrigger = true"],
        badge: "EP2 SCENE 05: QUANTIZED MOTION",
        visualType: "mesh_wireframe",
        sfx: "hum",
        audioSrc: "audio/narration_ep2/scene_05_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_06",
        num: 6,
        title: "No-Clip Phase Through Steel Door",
        duration: 8.0,
        startTime: 35.0,
        endTime: 43.0,
        timecode: "00:35 - 00:43",
        camera: "Low-angle dynamic tracking shot following sprinting engineer passing through solid steel door",
        prompt: "Dynamic side angle of male engineer running in dark corridor and phasing through a heavy industrial steel security door, wireframe glitch shimmer, no physical impact, cinematic sci-fi VFX, photorealistic, 8k",
        narration: "Collision meshes are unloaded. He sprints and phases directly through the solid steel security door.",
        overlay: ["MESH COLLISION: NULL", "PHASING SECTOR 4 PERIMETER"],
        badge: "EP2 SCENE 06: STEEL NO-CLIP",
        visualType: "mesh_wireframe",
        sfx: "void_drop",
        audioSrc: "audio/narration_ep2/scene_06_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_07",
        num: 7,
        title: "Corrupted Corridor & Z-Fighting",
        duration: 9.0,
        startTime: 43.0,
        endTime: 52.0,
        timecode: "00:43 - 00:52",
        camera: "Wide cinematic corridor one-point perspective dolly, flickering overhead sodium fixtures",
        prompt: "Wide one point perspective shot of long dark data center corridor, harsh yellow sodium emergency lights flickering at 60hz, geometric glitches where floor tiles and distant server racks interpenetrate with z-fighting artifact, cinematic, atmospheric sci-fi",
        narration: "The hallway beyond is decompiling. Sodium lights flicker at sixty hertz as server racks tear through the floor.",
        overlay: ["CORRIDOR SECTOR B-NORTH", "Z-BUFFER COLLAPSE DETECTED"],
        badge: "EP2 SCENE 07: Z-BUFFER COLLAPSE",
        visualType: "void_glitch",
        sfx: "hum",
        audioSrc: "audio/narration_ep2/scene_07_narration.wav",
        aiRender: ""
      },
      {
        id: "scene_08",
        num: 8,
        title: "The 23% Build Progress & Defiance",
        duration: 8.0,
        startTime: 52.0,
        endTime: 60.0,
        timecode: "00:52 - 01:00",
        camera: "Snap zoom on distant glowing workstation screen, then fast whip-pan into engineer's eyes",
        prompt: "Cinematic close-up of engineer looking over shoulder in dark glitched corridor, eyes resolute and determined, green and yellow light reflection on face, in background distant workstation monitor reads COMPILING USER_ABHRANKAN... 23%, high contrast, cinematic film still",
        narration: "The terminal prints: Compiling User Abhrankan, twenty-three percent. But until the build finishes, he still owns himself.",
        overlay: ["COMPILING USER_ABHRANKAN... 23%", "TO BE CONTINUED IN CHAPTER 3"],
        badge: "EP2 SCENE 08: 23% COMPILATION",
        visualType: "eye_glitch",
        sfx: "strobe",
        audioSrc: "audio/narration_ep2/scene_08_narration.wav",
        aiRender: ""
      }
    ];
"""

    if "const scenesEpisode2" not in html:
        target_pos = "const episodesConfig = {"
        html = html.replace(target_pos, scenes_ep2_code + "\n    " + target_pos)

    # 5. Add ep2 config into episodesConfig
    ep2_config_str = """,
      ep2: {
        title: "Episode 2 — Force Quit (Chapter 2 Blueprint & Narration)",
        videoSrc: "episodes/chapter-01-complete-directors-cut.mp4",
        size: "Episode 2 Blueprint",
        srt: "subtitles/episode-02-force-quit.srt",
        vtt: "subtitles/episode-02-force-quit.vtt",
        yaml: "episodes/episode-02-force-quit.yaml",
        duration: 60,
        scenes: scenesEpisode2
      }"""

    if '"scenesPart2.map' in html and 'ep2:' not in html:
        # inject before closing of episodesConfig
        close_cfg = "};\n\n    let currentEpisodeKey"
        html = html.replace(close_cfg, ep2_config_str + "\n    " + close_cfg)

    # 6. Update switchEpisode to handle tabEp2 styling
    old_switch_tabs = """["part1", "part2", "full"].forEach(k => {
        const btn = document.getElementById(k === "part1" ? "tabPart1" : (k === "part2" ? "tabPart2" : "tabFull"));"""

    new_switch_tabs = """["part1", "part2", "full", "ep2"].forEach(k => {
        const btn = document.getElementById(k === "part1" ? "tabPart1" : (k === "part2" ? "tabPart2" : (k === "full" ? "tabFull" : "tabEp2")));"""

    if old_switch_tabs in html:
        html = html.replace(old_switch_tabs, new_switch_tabs)

    with open(sb_path, "w", encoding="utf-8") as f:
        f.write(html)
    with open(sb_idx, "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully updated storyboard.html and storyboard/index.html with Episode 2 support!")

if __name__ == "__main__":
    update()
