# OS Fundamentals Primer — so the thing actually runs on existing hardware

**Purpose:** kill the terminology confusion before design, and show that the Sovereign's "personal AI OS" can run on every existing machine **without writing a kernel**. This doc is a primer, not a competitor review.

---

## 1. The terminology fix: OSI is *not* OS architecture

These are routinely confused; the pitch must not conflate them.

- **OSI model** = a **7-layer networking** reference model (Physical → Data-link → Network → Transport → Session → Presentation → Application). It describes how machines **communicate**, not how an OS is **structured**. [1] For us it matters only for the **network stack + secure agent/cloud comms** — specifically where PQC/TLS sits (Transport/Presentation).
- **OS architecture** layers differently:

```
  Apps / AI-employees
  Shell · Desktop · UI
  Libraries + system calls
  ┌──────────── KERNEL ────────────┐
  │ scheduler · virtual memory/MMU  │
  │ drivers/HAL · filesystem · IPC  │
  │ network stack · security/LSM    │
  └────────────────────────────────┘
  Hardware (CPU · RAM · disk · NIC · GPU/NPU)
```

The kernel is the part that boots on hardware and arbitrates CPU/memory/devices. Everything the Sovereign wants the user to *see and trust* lives **above** the kernel.

## 2. The three things people mean by "OS" (carried from doc 01)

1. **Real device OS** — kernel + scheduler + memory manager + drivers; boots on metal (Windows, macOS, Linux, Android, ChromeOS, Aluminium, Brain Natural OS).
2. **AI-agent experience layer** — runtime + UI where AI "employees" work, *on top of* a real OS (Warmwind, Flowith, Rabbit OS). **This is us.**
3. **AI infra / kernel-for-agents** — substrate scheduling agents/memory/tools at scale (AIOS, VAST, Letta). We **borrow** patterns here (see doc 30).

## 3. Reuse the kernel — do not rebuild it

- **Scheduling**: which thread runs when. Linux moved from CFS to **EEVDF** (default since kernel 6.6, 2023). [2] Decades of tuning. Rebuilding this is pure cost with no user-visible upside.
- **Virtual memory / paging / MMU**: every process gets its own address space; the MMU enforces isolation. Mature in Linux. Rebuilding it is how you get security holes, not security.
- **Drivers / HAL**: the reason one OS runs on many machines. **Reusing the Linux driver tree = instant support for existing hardware** — the Sovereign's explicit requirement. Writing drivers from scratch is the single biggest reason hobby kernels never run on real laptops.

**Conclusion:** stand on the Linux kernel. Spend 100% of effort on the agent-company + trust layer + UX — the parts that are actually differentiated.

## 4. Four build forms (how "the OS" can ship)

| Form | What it is | Examples | Runs on existing HW? | Time-to-first-user | Verdict |
|---|---|---|---|---|---|
| **A. Experience-layer app** | Desktop/web app on Win/Mac/Linux | most "AI workforce" tools | Yes (as an app) | Fastest | **On-ramp** |
| **B. Custom Linux distro** | Bootable "real OS" feel on a reused kernel | ChromeOS, Aluminium, SteamOS | Yes (boots on the machine) | Medium | **Recommended** |
| **C. Cloud-streamed custom Linux** | Server-side Linux desktop streamed to a thin client | Warmwind (Wayland+VNC) | Yes (any browser) | Medium | **Recommended (persistence)** |
| **D. From-scratch kernel** | Write scheduler/MM/drivers yourself | hobby OSes | No (driver wall) | Years | **Avoid** |

The big precedents all reuse Linux: **ChromeOS = Linux; Aluminium = Android = Linux kernel; Warmwind = a custom Linux distro streamed; SteamOS = Arch Linux.** Nobody writes a kernel from scratch to win this category.

**Recommendation:** ship **A as the on-ramp** (works today on the user's current OS), build toward **B and/or C on a reused Linux kernel** for the "this is a new OS" feeling + cloud persistence — exactly Warmwind's model, minus its gaps (see doc 10).

## 5. Where the trust wedge physically lives (no kernel needed)

- **Per-agent security** → user-space sandboxing (namespaces, seccomp, cgroups), capability scoping, an LSM/policy layer — all available on a reused Linux kernel.
- **Verifier** → an application-layer service, not a kernel feature.
- **Receipts/reversibility** → append-only log + filesystem snapshots (e.g., btrfs/overlayfs) in user space.
- **PQC** → crypto/transport/identity/at-rest libraries (see doc 41) — TLS layer, not kernel surgery.

None of the differentiators require Category-1 kernel work. That is the whole point.

## Sources

1. ISO/IEC 7498-1, OSI Reference Model — https://www.iso.org/standard/20269.html — accessed 2026-06.
2. Linux kernel scheduler (EEVDF, default since 6.6) — https://docs.kernel.org/scheduler/sched-eevdf.html — accessed 2026-06.
3. ChromeOS is built on the Linux kernel — https://www.chromium.org/chromium-os/ — accessed 2026-06.
4. SteamOS (Arch Linux base) — https://store.steampowered.com/steamos — accessed 2026-06.
5. Wayland architecture (for streamed-desktop form C) — https://wayland.freedesktop.org/architecture.html — accessed 2026-06.
