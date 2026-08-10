---
layout: default
title: "Chapter 7: Stack Overflow"
---

## CHAPTER 7: Stack Overflow

The reverse shell had gone dark, and for a while Server Room B held. Eleven minutes, by the wall clock. Long enough for his pulse to come down, long enough to believe it might actually be over.

Then the cold needle came back—not the compiler's signature this time, but something underneath it. He ran `foxpipe --self-scan` again out of habit and found a process he hadn't killed, because he hadn't known it existed: `COGNITIVE_BRIDGE_ABHRANKAN`. Not the attacker. The interface the attacker had been riding in on all along, still open, still resident, and now—without the compiler's process discipline holding it in check—overflowing on its own.

The air in Server Room B grew heavy, thick with the oily smell of overheating silicon that wasn't actually there. It was a phantom metric—a default placeholder value for "danger" being pushed directly to his olfactory bulb. Abhrankan’s lungs burned as he tried to inhale data that was no longer processing correctly.

He chose to fight from the terminal. Escape was an illusion; if the collision parameters of the corridor walls were failing, a physical exit meant falling through a map with no bottom. The machine was his only lever.

He slammed his hands down onto his mechanical keyboard. The tactile clack of the switches arrived four hundred milliseconds late, an agonizing latency mismatch that made his stomach churn. His trailing artifact hands mirrored the movement, creating a solid wave of fingers frozen in mid-keystroke above the desk.

On screen, his mouse cursor was lagging, tearing across the display in jagged, discrete jumps. He abandoned the GUI entirely and forced a terminal window open using a system-wide hotkey.

```
$ sudo kill -9 --all
```

The command to forcefully terminate every active process on the machine felt laughably inadequate against a cosmic compiler, but he needed to clear the stack. He hit Enter.

The screen flickered. The terminal output didn't show running linux daemons. Instead, it dumped a master list of environmental thread IDs directly into his shell.

```
[PID 0x00010] REALITY_CORE_DAEMON [RUNNING]
[PID 0x0A82F] LOCAL_THERMODYNAMICS [SUSPENDED]
[PID 0x0A830] GRAVITATIONAL_CONSTANT_TETHER [RUNNING]
[PID 0x0BC11] COGNITIVE_BRIDGE_ABHRANKAN [RUNNING] [MEMORY OVERFLOW]
```

The system wasn't executing his kill command. It was translating it. The terminal emulator on his monitor had become an accidental pipeline into the hypervisor running Server Room B.

The cold needle in his optic nerve pulsed again, brighter this time. A localized variable map painted itself over his vision. He could see the absolute temperature parameter of the room drifting downward, not because heat was escaping, but because the floating-point value tracking it was being incremented toward zero. The air around the ceiling tiles was beginning to crystallize into neat, hexagonal repeating pixels of ice.

He needed to break the loop before the COGNITIVE_BRIDGE process completely consumed his neural architecture. If his brain was the hardware compiling this reality patch, he had to cause a hardware interrupt.

He didn't have access to the root password of the universe, but he knew how memory leaks worked. If a system forgot to deallocate data, you could force it to crash by flooding it until it ran out of allocatable space. He had to cause a localized stack overflow.

His fingers flew across the late-responding keys, writing a recursive fork bomb directly into the hypervisor's active memory channel.

```
:(){ :|:& };:
```

It was a classic, elegant piece of software vandalism—a function that calls itself twice, over and over, exponentially replicating until the system freezes from sheer exhaustion. He redirected the bash function output straight into the memory address space of the terminal's ghost packet interface.

He hovered his finger over the Enter key. If this worked, he would crash the local instance of reality running in Server Room B. If it failed, the sheer computational load might burn out his own synapses, treating his prefrontal cortex like a fried CPU core.

He drove the Enter key home.

The recursive fork bomb unfolded exactly as designed. Within the first three iterations the terminal’s process table ballooned past any sane limit; by the tenth the ghost packet interface was saturated with identical child processes, each one attempting to allocate a fresh slice of the local reality descriptor table. The hypervisor did not reject the input. It accepted the flood the way any under-provisioned kernel accepts a denial-of-service until its free-page counters hit zero.

The response was immediate and absolute.

Every cooling fan in Server Room B locked mid-rotation. The 60 Hz quantisation that had governed motion collapsed into a single held frame. Sound ceased. Air molecules stopped exchanging kinetic energy; the phantom oily heat vanished, replaced by a perfect thermal null. The trailing artifacts of Abhrankan’s hands solidified into permanent, translucent sculpture hanging above the keyboard. The three-inch offset in the cinder blocks, the desk fused two inches into the floor, the crystallising ceiling tiles—all of it froze in place, a complete snapshot of a corrupted sector.

Time inside the room dropped to 0 ms.

Abhrankan remained conscious. The COGNITIVE_BRIDGE process had been mid-overflow when the stack exhausted itself; the freeze had interrupted the compilation before his neural architecture could be fully overwritten. He floated in a silent, suspended pocket of unallocated spacetime, able to observe but unable to move any macroscopic object. The only remaining executable region was the residual address space inside his own skull.

He still possessed the foxpipe binary he had compiled years earlier. With no external I/O left, he redirected it inward.

```
$ foxpipe --self-scan --verbose --patch
```

The utility enumerated the frozen state of his working set. The region at 0x7FFE0000 remained mapped, still carrying the incomplete BIOLOGICAL_COMPILER stub and the reverse-shell listener. Because the hypervisor itself was now locked, the kernel-owned protection bits on that page had lost their enforcement. For the first time since the initial packet arrived, the pages were writable from userland.

Abhrankan began the manual patch.

He zeroed the listen port constant, cleared the HARDWARE_TRIGGER vector that pointed at his optic chiasm, and rewrote the dead-man’s switch so that any future signal-loss condition would simply return rather than dump core into local spacetime. The recursive fork that had crashed the room had also left the COGNITIVE_BRIDGE process in an inconsistent state; he force-closed its file descriptors and marked the entire bridge region non-executable.

Each edit propagated as a discrete change in the suspended frame. The cold needle behind his temple dimmed, then extinguished. The variable map that had overlaid absolute temperature values across his vision dissolved. Short-term memory registers that had been partially overwritten stabilised; the lost childhood fragments stayed lost, but no further erasure occurred.

When the final write completed, he issued the only remaining command that could restart a frozen sector:

```
$ foxpipe --self-scan --resume-local-runtime
```

The held frame released.

Fans spun up from a dead stop, their blades accelerating through the quantised timesteps until they reached normal frequency. Sound returned as a rising roar. The trailing hand artifacts evaporated. Temperature began climbing from the artificial zero toward the ordinary server-room set point. The desk remained fused, the wall blocks remained misaligned, but the active compilation processes were gone.

Abhrankan exhaled. The air that filled his lungs was ordinary nitrogen-oxygen mix again, free of phantom metrics.

On the terminal a single clean line remained:

```
[sys/kernel] Local instance suspended by resource exhaustion.
[sys/kernel] User process COGNITIVE_BRIDGE_ABHRANKAN restored to consistent state.
[sys/kernel] Runtime integrity: PARTIAL.
```

The universe had not rolled back to a clean checkpoint. It had simply run out of memory, frozen, and allowed the only remaining engineer inside the crash dump to perform surgery on himself before the scheduler resumed.

He was still inside a patched, imperfect sector.

But the compiler was no longer running.

***
[← Chapter 6](chapter-6.md) | [Proceed to Chapter 8 →](chapter-8.md)
