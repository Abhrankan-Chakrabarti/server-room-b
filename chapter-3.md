---
layout: default
title: "Chapter 3: Link Stage"
---

## CHAPTER 3: Link Stage

The SRE corridor didn’t end; it looped.

Abhrankan passed the fire extinguisher station three times, each iteration rendering at a lower level of detail. By the third loop, the instructional text on the canister had degenerated into a blocky, low-resolution placeholder texture. The system was running out of video memory. It was aggressively culling assets to keep his local rendering loop afloat while the background compilation choked his cognitive processing.

```
COMPILING USER_ABHRANKAN... 41%
```

The text didn't print on the walls anymore. It burned directly into his blind spot, moving when his eyes moved.

He didn't look for an exit sign. If the topology of the building had been remapped to a circular buffer, standard navigation was a dead end. He needed a terminal that hadn't been demoted to Userland. He needed to find the core network switch room—the physical point of ingress where the raw fiber lines entered the building from the outside world. If he could intercept the raw bitstream before it reached the local bus, he could drop the connection at the hardware layer.

He slid through a door labeled MAIN DISTRIBUTION FRAME (MDF).

The room was freezing. The ambient cooling here was still operational, but the air felt thin, unrendered, like breathing an empty array. In the center of the room stood the core Cisco backbone switch, its status lights flashing in an erratic, unquantized rhythm.

It was still running on bare metal. The compiler hadn't hooked its microcode yet.

Abhrankan dropped to his knees in front of the console rack. His hands were getting harder to control; the latency had jumped to over 150 milliseconds. His fingers felt heavy, like blocks of uninitialized memory. He grabbed the serial console cable, jammed it into his laptop’s USB port, and opened a raw serial interface.

```
$ screen /dev/ttyUSB0 115200
```

The console screen flashed green. A clean, pristine command prompt appeared. No logs. No entity warnings. Just pure, unadulterated hardware control.

```
MDF-CORE-SW01>
```

Behind him, the door to the MDF room vanished. The wall became a smooth, featureless grey plane. The compiler was sealing the active sector to prevent memory leakage.

```
COMPILING USER_ABHRANKAN... 67%
```

His vision began to drop channels. The color depth snapped from 32-bit true color to 8-bit VGA. The room lost its gradient shadows, flattening into harsh, jagged blocks of primary colors. He could feel his short-term memory fragments starting to overwrite each other. He forgot his childhood phone number. He forgot the name of his first pet. The compiler was clearing his storage registers to make room for its own payload libraries.

He began typing, his fingers striking the keys in rhythmic, mechanical bursts. He didn't write code; he wrote network access control lists (ACLs).

```
MDF-CORE-SW01> enable
MDF-CORE-SW01# configure terminal
MDF-CORE-SW01(config)# ip access-list extended BLOCK_COMPILER
MDF-CORE-SW01(config-ext-nacl)# deny udp any any eq 8080
MDF-CORE-SW01(config-ext-nacl)# deny ip host 0.0.0.0 any
```

A sudden spasm wracked his upper body. His left arm locked completely straight, the muscles rigid as the compiler attempted to load an external driver into his nervous system. His vision flashed pure white.

```
COMPILING USER_ABHRANKAN... 89%
```

He could see the structure of the binary now. It wasn't alien code. It was an elegant, terrifyingly optimized algorithm designed to loop infinitely, parsing the matter of the universe and stripping out everything that wasn't mathematically essential. It was a garbage-collector for existence.

With his right hand, his only remaining responsive limb, he reached for the keyboard to apply the access list to the external interface.

```
MDF-CORE-SW01(config-ext-nacl)# interface GigabitEthernet0/1
MDF-CORE-SW01(config-if)# ip access-group BLOCK_COMPILER in
```

He hit Enter.

The screen frozen. The cursor stayed solid. The entire room went completely, horrifyingly silent. The 60 Hz stutter of the fans stopped. Time dropped to 0 ms.

For a timeless frame, Abhrankan hung in the void between states. The link stage had collided with the firewall rules at the exact same microsecond.

Then, the console printed a final line:

```
%ACL-I-APPLIED: Extended IP access list BLOCK_COMPILER applied to interface Gi0/1.
[sys/kernel] Connection reset by peer.
```

The white text in his vision shattered into millions of green pixels and fell away like digital rain. The color depth instantly snapped back to true color. The air filled with the sharp, warm scent of ozone, and the industrial roar of three hundred fans returned at their normal, unquantized pitch.

Abhrankan collapsed against the server rack, gasping for air, his hands completely clear of trailing artifacts. He looked at the laptop screen. The serial session was dead.

He had dropped the packet.

But as he stood up and looked toward the wall where the door used to be, he noticed the doorway had returned—yet the cinder blocks around it were still permanently misaligned by exactly three inches. The bug in the wall remained.

The connection was closed, but the universe hadn't reloaded its last clean save.

***
[← Chapter 2](chapter-2.md) | [Proceed to Chapter 4 →](chapter-4.md)
