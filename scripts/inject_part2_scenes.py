"""
Injects Part 1, Part 2, and Director's Cut scene data and switcher logic into storyboard.html.
"""

import os

def update():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sb_path = os.path.join(repo_dir, "storyboard.html")
    with open(sb_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Find definition of const scenes = [ ... ];
    start_tag = "    // --- Data Model for Server Room B: Episode 1 ---"
    end_tag = "    // --- State Variables ---"
    
    idx1 = html.find(start_tag)
    idx2 = html.find(end_tag)
    
    if idx1 == -1 or idx2 == -1:
        print("Could not find scenes tag boundary")
        return

    new_data_model = """    // --- Data Model for Server Room B: Chapter 1 (Part 1 & Part 2) ---
    const scenesPart1 = [
      {
        id: "scene_01",
        num: 1,
        title: "Server Room B Corridor",
        duration: 6,
        startTime: 0,
        endTime: 6,
        timecode: "00:00 - 00:06",
        camera: "Slow camera dolly forward, volumetric blue lighting, anamorphic bokeh",
        prompt: "Dark enterprise server room at night, rows of black server racks with blinking blue LEDs, cinematic sci-fi thriller, slow camera dolly forward, volumetric lighting, realistic hardware, suspenseful atmosphere, ultra realistic, vertical 9:16 mobile format.",
        narration: "3:14 AM. Server Room B.",
        overlay: ["03:14 AM"],
        badge: "SCENE 1: SERVER ROOM B",
        visualType: "servers",
        sfx: "hum",
        audioSrc: "audio/narration/scene_01_narration.wav",
        aiRender: "episodes/kling_renders/scene_01.mp4"
      },
      {
        id: "scene_02",
        num: 2,
        title: "Abhrankan at Consoles",
        duration: 8,
        startTime: 6,
        endTime: 14,
        timecode: "00:06 - 00:14",
        camera: "Low-angle medium shot, screen glow reflection, slow push-in",
        prompt: "Abhrankan, late 20s software engineer, sitting alone in front of multiple monitors, blue monitor glow, dark server room, realistic cinematic science fiction, vertical 9:16 format.",
        narration: "Abhrankan sits alone, tracking a mysterious memory leak.",
        overlay: ["MEMORY ALLOCATION ERROR DETECTED"],
        badge: "SCENE 2: MEMORY LEAK INVESTIGATION",
        visualType: "engineer",
        sfx: "typing",
        audioSrc: "audio/narration/scene_02_narration.wav",
        aiRender: "episodes/kling_renders/scene_02.mp4"
      },
      {
        id: "scene_03",
        num: 3,
        title: "Memory Statistics Dashboard",
        duration: 6,
        startTime: 14,
        endTime: 20,
        timecode: "00:14 - 00:20",
        camera: "Close-up locked-on terminal shot, rhythmic HUD update",
        prompt: "Computer terminal displaying memory statistics, numbers decreasing, technical monitoring dashboard, realistic interface, cinematic suspense, vertical 9:16 format.",
        narration: "Every minute, the system loses exactly sixty-four bytes.",
        overlay: ["-64 BYTES"],
        badge: "SCENE 3: TELEMETRY ANOMALY",
        visualType: "memory_dash",
        sfx: "pulse",
        audioSrc: "audio/narration/scene_03_narration.wav",
        aiRender: "episodes/kling_renders/scene_03.mp4"
      },
      {
        id: "scene_04",
        num: 4,
        title: "Packet Stream Scan",
        duration: 8,
        startTime: 20,
        endTime: 28,
        timecode: "00:20 - 00:28",
        camera: "Close-up monitor shot, rapid scrolling text, subtle rack focus",
        prompt: "Computer terminal streaming network packets, encrypted telemetry, rapid scrolling data, realistic cyber infrastructure, close-up monitor shot, vertical 9:16 format.",
        narration: "He launches a network scan. Everything looks normal.",
        overlay: [],
        badge: "SCENE 4: NETWORK SCAN STREAM",
        visualType: "packet_stream",
        sfx: "typing_fast",
        audioSrc: "audio/narration/scene_04_narration.wav",
        aiRender: "episodes/kling_renders/scene_04.mp4"
      },
      {
        id: "scene_05",
        num: 5,
        title: "Terminal Freeze",
        duration: 8,
        startTime: 28,
        endTime: 36,
        timecode: "00:28 - 00:36",
        camera: "Slow suspenseful zoom in on frozen blinking cursor, ambient darkness",
        prompt: "Terminal suddenly freezes, blinking cursor, dark room illuminated by monitor light, slow zoom in, sci-fi suspense, vertical 9:16 format.",
        narration: "Then the scrolling stops.",
        overlay: [],
        badge: "SCENE 5: SYSTEM HALT",
        visualType: "frozen_cursor",
        sfx: "silence",
        audioSrc: "audio/narration/scene_05_narration.wav",
        aiRender: "episodes/kling_renders/scene_05.mp4"
      },
      {
        id: "scene_06",
        num: 6,
        title: "The Ghost Source (0.0.0.0)",
        duration: 8,
        startTime: 36,
        endTime: 44,
        timecode: "00:36 - 00:44",
        camera: "Dramatic digital zoom toward screen, chromatic lens distortion",
        prompt: "Computer monitor displaying source address 0.0.0.0, subtle digital distortion, cinematic cyber thriller, dramatic zoom toward screen, vertical 9:16 format.",
        narration: "A single packet appears. Source address: zero point zero point zero point zero.",
        overlay: ["SOURCE: 0.0.0.0"],
        badge: "SCENE 6: NULL PACKET",
        visualType: "null_packet",
        sfx: "glitch",
        audioSrc: "audio/narration/scene_06_narration.wav",
        aiRender: "episodes/kling_renders/scene_06.mp4"
      },
      {
        id: "scene_07",
        num: 7,
        title: "Biological Compiler Awakening",
        duration: 10,
        startTime: 44,
        endTime: 54,
        timecode: "00:44 - 00:54",
        camera: "Dynamic zoom, chromatic aberration, symbols reassembling",
        prompt: "Hexadecimal code transforming into glowing warning text, symbols rearranging themselves, digital corruption, cinematic science fiction horror, vertical 9:16 format.",
        narration: "The packet begins rearranging itself into words.",
        overlay: ["CRITICAL SYSTEM FAULT", "BIOLOGICAL COMPILER ACTIVE", "TARGET IDENTIFIED: USER_ABHRANKAN"],
        badge: "SCENE 7: RECOMPILATION",
        visualType: "hex_recompile",
        sfx: "alarm",
        audioSrc: "audio/narration/scene_07_narration.wav",
        aiRender: "episodes/kling_renders/scene_07.mp4"
      },
      {
        id: "scene_08",
        num: 8,
        title: "Human Pupil Glitch Impact",
        duration: 6,
        startTime: 54,
        endTime: 60,
        timecode: "00:54 - 01:00",
        camera: "Extreme macro close-up of human eye, monitor reflection, violent glitch",
        prompt: "Extreme close-up of human eye illuminated by monitor light, digital glitch reflections, sudden distortion, realistic cinematic thriller, vertical 9:16 format.",
        narration: "Ah!",
        overlay: [],
        badge: "SCENE 8: REALITY OVERFLOW",
        visualType: "eye_glitch",
        sfx: "shriek",
        audioSrc: "audio/narration/scene_08_narration.wav",
        aiRender: "episodes/kling_renders/scene_08.mp4"
      }
    ];

    const scenesPart2 = [
      {
        id: "scene_09",
        num: 9,
        title: "The Acoustic Stutter (2ms Loop)",
        duration: 7.5,
        startTime: 0,
        endTime: 7.5,
        timecode: "00:00 - 00:07.5",
        camera: "Perspective server corridor, ominous camera float, amber sodium flicker",
        prompt: "Dark enterprise server room, rows of black server racks with cold blue and amber LEDs, cinematic science fiction horror, subtle flickering sodium light, tense silence, 9:16 vertical format.",
        narration: "The server hum has changed. Instead of a smooth mechanical drone, it now stutters like a broken audio file.",
        overlay: ["TIMESTEP: 2.00ms FIXED"],
        badge: "SCENE 9: ACOUSTIC STUTTER",
        visualType: "servers",
        sfx: "hum",
        audioSrc: "audio/narration_part2/scene_09_narration.wav",
        aiRender: "episodes/kling_renders/scene_09.mp4"
      },
      {
        id: "scene_10",
        num: 10,
        title: "Tactile Input Delay",
        duration: 7.0,
        startTime: 7.5,
        endTime: 14.5,
        timecode: "00:07.5 - 00:14.5",
        camera: "Low angle medium push, Abhrankan rising and freezing in shock",
        prompt: "Abhrankan, late 20s software engineer, standing up from workstation chair, reaching hand toward smartphone on desk, frozen in disbelief, eyes wide, 9:16 vertical format.",
        narration: "Abhrankan slowly rises from his chair. He reaches for his phone... and freezes.",
        overlay: ["INPUT LATENCY: +47ms"],
        badge: "SCENE 10: TACTILE DELAY",
        visualType: "engineer",
        sfx: "pulse",
        audioSrc: "audio/narration_part2/scene_10_narration.wav",
        aiRender: "episodes/kling_renders/scene_10.mp4"
      },
      {
        id: "scene_11",
        num: 11,
        title: "Geometric Hand Cascade",
        duration: 8.0,
        startTime: 14.5,
        endTime: 22.5,
        timecode: "00:14.5 - 00:22.5",
        camera: "Close-up macro lens, frozen solid duplicate knuckles in air",
        prompt: "Extreme close-up of a human hand moving across a desk leaving a physical cascading trail of translucent solid duplicate knuckles suspended in mid-air, like a frozen window dragging across a crashed desktop, 9:16 vertical format.",
        narration: "Behind his hand hangs a trail. Not motion blur, but solid frozen copies lingering in the air.",
        overlay: ["ARTIFACT ACCUMULATION"],
        badge: "SCENE 11: GEOMETRIC CASCADE",
        visualType: "hand_cascade",
        sfx: "glitch",
        audioSrc: "audio/narration_part2/scene_11_narration.wav",
        aiRender: "episodes/kling_renders/scene_11.mp4"
      },
      {
        id: "scene_12",
        num: 12,
        title: "Keypad Log Overflow",
        duration: 7.0,
        startTime: 22.5,
        endTime: 29.5,
        timecode: "00:22.5 - 00:29.5",
        camera: "Close-up of heavy steel security door digital keypad, streaming system logs",
        prompt: "Close-up of high-security facility door digital keypad, glowing monochrome LCD cycling rapid system logs, industrial heavy metal texture, biometric scanner, 9:16 vertical format.",
        narration: "The security keypad isn't asking for a passcode anymore. It races through endless system messages.",
        overlay: ["LOG STREAM: SECTOR 4"],
        badge: "SCENE 12: KEYPAD OVERFLOW",
        visualType: "packet_stream",
        sfx: "typing_fast",
        audioSrc: "audio/narration_part2/scene_12_narration.wav",
        aiRender: "episodes/kling_renders/scene_12.mp4"
      },
      {
        id: "scene_13",
        num: 13,
        title: "The Void & Collision Mesh Unload",
        duration: 8.5,
        startTime: 29.5,
        endTime: 38.0,
        timecode: "00:29.5 - 00:38.0",
        camera: "Dramatic camera push on cinder block wall vanishing into infinite void",
        prompt: "Concrete cinder block wall under digital keypad flickering, a rectangular section completely vanishing into a flat infinite pitch black void, then snapping back misaligned and clipping into the floor, 9:16 vertical format.",
        narration: "The wall flickers, vanishing into an infinite black void. The universe wasn't being haunted. It was being uninstalled.",
        overlay: ["COLLISION MESH UNLOADED"],
        badge: "SCENE 13: THE VOID",
        visualType: "void_mesh",
        sfx: "sub_drop",
        audioSrc: "audio/narration_part2/scene_13_narration.wav",
        aiRender: "episodes/kling_renders/scene_13.mp4"
      },
      {
        id: "scene_14",
        num: 14,
        title: "Violent Monitor Strobe",
        duration: 7.5,
        startTime: 38.0,
        endTime: 45.5,
        timecode: "00:38.0 - 00:45.5",
        camera: "Violent camera shake, blinding white/blue strobe light flashing across room",
        prompt: "Abhrankan shielding his face with his forearm in terror inside the dark server room, workstation monitors violently flashing blinding white and electric blue strobe bursts, 9:16 vertical format.",
        narration: "A deep rumble shakes the room. His workstation monitor flashes violently, casting a blinding strobe pattern.",
        overlay: ["SECTOR 4 DECOMPILING"],
        badge: "SCENE 14: MONITOR STROBE",
        visualType: "strobe_flash",
        sfx: "alarm",
        audioSrc: "audio/narration_part2/scene_14_narration.wav",
        aiRender: "episodes/kling_renders/scene_14.mp4"
      },
      {
        id: "scene_15",
        num: 15,
        title: "Biological Host Detected",
        duration: 8.0,
        startTime: 45.5,
        endTime: 53.5,
        timecode: "00:45.5 - 00:53.5",
        camera: "Macro terminal shot, biological compilation progress and EEG spikes",
        prompt: "Extreme close-up macro view of computer monitor displaying Linux terminal, sharp glowing crimson-red text reading BIOLOGICAL HOST DETECTED, COMPILATION SOURCE: USER_ABHRANKAN, EEG brainwave telemetry spiking, 9:16 vertical format.",
        narration: "The terminal is compiling a new process. And the hardware it's using to build it... is Abhrankan's own brain.",
        overlay: ["BIOLOGICAL HOST: USER_ABHRANKAN"],
        badge: "SCENE 15: BIOLOGICAL HOST",
        visualType: "hex_recompile",
        sfx: "alarm",
        audioSrc: "audio/narration_part2/scene_15_narration.wav",
        aiRender: "episodes/kling_renders/scene_15.mp4"
      },
      {
        id: "scene_16",
        num: 16,
        title: "Cut to Black & Credits",
        duration: 6.5,
        startTime: 53.5,
        endTime: 60.0,
        timecode: "00:53.5 - 01:00.0",
        camera: "Blinding whiteout optical flare expanding to full screen, cut to black title card",
        prompt: "Blinding whiteout lens flare erupting from central monitor inside dark server room, rays of pure white light washing out room, streaks of anamorphic blue flare, cutting to black, 9:16 vertical format.",
        narration: "TO BE CONTINUED. Story by Abhrankan Chakrabarti.",
        overlay: ["STORY BY ABHRANKAN CHAKRABARTI"],
        badge: "SCENE 16: TO BE CONTINUED",
        visualType: "eye_glitch",
        sfx: "shriek",
        audioSrc: "audio/narration_part2/scene_16_narration.wav",
        aiRender: "episodes/kling_renders/scene_16.mp4"
      }
    ];

    const episodesConfig = {
      part1: {
        title: "Episode 1 — Part 1: The Packet",
        videoSrc: "episodes/episode-01-the-packet.mp4",
        size: "17.6 MB",
        srt: "subtitles/episode-01.srt",
        vtt: "subtitles/episode-01.vtt",
        yaml: "episodes/episode-01-the-packet.yaml",
        duration: 60,
        scenes: scenesPart1
      },
      part2: {
        title: "Episode 1 — Part 2: Reality Uninstall",
        videoSrc: "episodes/episode-01-part-02.mp4",
        size: "19.7 MB",
        srt: "subtitles/episode-01-part-02.srt",
        vtt: "subtitles/episode-01-part-02.vtt",
        yaml: "episodes/episode-01-part-02.yaml",
        duration: 60,
        scenes: scenesPart2
      },
      full: {
        title: "Chapter 1 — Complete Director's Cut (120s)",
        videoSrc: "episodes/chapter-01-complete-directors-cut.mp4",
        size: "37.3 MB",
        srt: "subtitles/episode-01.srt",
        vtt: "subtitles/episode-01.vtt",
        yaml: "episodes/episode-01-part-02.yaml",
        duration: 120,
        scenes: scenesPart1.concat(scenesPart2.map(s => ({
          ...s,
          startTime: s.startTime + 60,
          endTime: s.endTime + 60,
          timecode: `${Math.floor((s.startTime+60)/60).toString().padStart(2,'0')}:${Math.floor((s.startTime+60)%60).toString().padStart(2,'0')} - ${Math.floor((s.endTime+60)/60).toString().padStart(2,'0')}:${Math.floor((s.endTime+60)%60).toString().padStart(2,'0')}`
        })))
      }
    };

    let currentEpisodeKey = "part1";
    let scenes = episodesConfig.part1.scenes;
"""

    html = html[:idx1] + new_data_model + "\n" + html[idx2:]
    
    # Add switchEpisode function before renderSceneCards
    insert_before = "    // --- Render Scene Cards in Right Panel ---"
    ins_idx = html.find(insert_before)
    if ins_idx != -1:
        switcher_func = """    // --- Episode Switching Dispatcher ---
    window.switchEpisode = function(epKey) {
      if (!episodesConfig[epKey]) return;
      currentEpisodeKey = epKey;
      const ep = episodesConfig[epKey];
      scenes = ep.scenes;
      
      // Update UI Header & Badges
      const hTitle = document.getElementById("headerEpisodeTitle");
      if (hTitle) hTitle.textContent = ep.title;
      const actLabel = document.getElementById("activeAssetLabel");
      if (actLabel) actLabel.textContent = `${epKey.toUpperCase()} (${ep.size})`;
      const dlLink = document.getElementById("downloadActiveMp4");
      if (dlLink) {
        dlLink.href = ep.videoSrc;
        const szBadge = document.getElementById("activeVideoSizeBadge");
        if (szBadge) szBadge.textContent = ep.size;
      }
      const srtLink = document.getElementById("specSrtLink");
      if (srtLink) srtLink.href = ep.srt;
      const vttLink = document.getElementById("specVttLink");
      if (vttLink) vttLink.href = ep.vtt;
      const yamlLink = document.getElementById("specYamlLink");
      if (yamlLink) yamlLink.href = ep.yaml;

      // Update Tabs styling
      ["part1", "part2", "full"].forEach(k => {
        const btn = document.getElementById(k === "part1" ? "tabPart1" : (k === "part2" ? "tabPart2" : "tabFull"));
        if (!btn) return;
        if (k === epKey) {
          btn.className = "px-3 py-1 rounded-lg font-semibold transition-all bg-sky-600 text-white shadow-sm";
        } else {
          btn.className = "px-3 py-1 rounded-lg font-semibold transition-all text-slate-400 hover:text-slate-200";
        }
      });

      // Update Scrubber Max
      scrubber.max = ep.duration;
      const maxTimeSpan = scrubber.nextElementSibling;
      if (maxTimeSpan) maxTimeSpan.textContent = ep.duration >= 120 ? "02:00" : "01:00";

      // Re-source Video Player
      productionVideoPlayer.pause();
      productionVideoPlayer.src = ep.videoSrc;
      productionVideoPlayer.currentTime = 0;
      currentTime = 0;
      currentSceneIndex = 0;
      lastSpokenScene = -1;
      updateSceneState(0);
      renderSceneCards();
      pause();
      showToast(`Switched to: ${ep.title}`);
    };

"""
        html = html[:ins_idx] + switcher_func + html[ins_idx:]

    with open(sb_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Injected Part 1, Part 2 & Director's Cut data into storyboard.html!")

if __name__ == "__main__":
    update()
