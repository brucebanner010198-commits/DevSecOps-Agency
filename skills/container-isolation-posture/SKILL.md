---
name: container-isolation-posture
description: Design-guidance skill for sandboxing agent execution. Use when designing or reviewing any system that runs LLM-driven agents against host resources — whether the host is a laptop, a CI runner, a Docker/container runtime, or a VM. Codifies the nine-rule posture (external allowlist, fail-closed, block-by-default patterns, symlink resolution, container-path validation, read-only project root, session isolation, IPC authorization, credential vault) so reviewers, architects, and specialists (mcp-defense, mcp-author, injection-defense, secrets-vault, sandbox, sdlc-patterns, red-team) have a shared checklist. Pairs with `sandbox` (the execution skill) and `mcp-defense` (the consumer-side skill).
version: 0.3.6
lineage: Design patterns distilled from MIT-licensed qwibitai/nanoclaw@v1.2.53 — docs/SECURITY.md and src/mount-security.ts, © 2026 Gavriel. Generalized to design guidance (no TypeScript code ported). See LICENSES/MIT-nanoclaw.txt.
---

# container-isolation-posture — a nine-rule checklist for agent sandboxes

Every system that runs an LLM-driven agent against real host resources (a laptop, a CI runner, a container, a VM) needs a sandbox. This skill codifies what "sandbox" means in nine concrete rules so designers, reviewers, and red-teamers share the same picture. Apply it when you are:

- Writing a spec for a new agent-execution surface.
- Reviewing an existing MCP server or agent host for injection / exfiltration exposure.
- Answering "is this safe to ship?" on a new runtime integration.
- Closing a finding from `red-team`, `injection-defense`, or `oss-forensics`.

This is **design guidance**, not executable code. The goal is a posture that any implementation in any language can hold up against.

## The trust model (fill this in first)

For every new surface, name the entities and their trust level explicitly. The nanoclaw posture uses four buckets — reuse them:

| Entity              | Trust level | Rationale                                                     |
| ------------------- | ----------- | ------------------------------------------------------------- |
| Main / admin chat   | Trusted     | Private self-chat; admin ergonomics; credentials never leave. |
| Other chats/groups  | Untrusted   | Other humans; potentially adversarial.                        |
| Agent container     | Sandboxed   | Isolated by mount + process + network policy.                 |
| Incoming messages   | User input  | Prompt-injection surface; treat as attacker-controlled.       |

If your design can't fill this table in one sitting, you don't have a sandbox — you have an execution environment.

## The nine rules

### 1. Primary boundary is the container / VM, not the application

Rely on OS-level isolation for the hard boundary:

- **Process isolation** — agent process cannot `ptrace` or signal host processes.
- **Filesystem isolation** — only explicitly mounted directories are visible; everything else doesn't exist from the agent's view.
- **Non-root execution** — run as a dedicated unprivileged user (uid ≥ 1000), never as root.
- **Ephemeral containers** — `--rm` / fresh instance per invocation. No stateful drift across calls.

Application-level permission checks inside the agent are a *defense in depth* layer, not the boundary. If your threat model depends on the agent choosing to obey a rule, the boundary is in the wrong place.

### 2. Mount allowlist lives outside the sandbox

The allowlist of what can be mounted in, and at what mode (ro/rw), **must not be reachable from the sandbox**. Requirements:

- Stored outside project root (e.g. `~/.config/<app>/mount-allowlist.json`).
- Never mounted into the container.
- Loaded at host-process startup; cached in memory for the process lifetime.
- Changes require host-process restart *or* an explicit SIGHUP-style reload — not a mutation from inside the agent.

If the agent can rewrite its own policy, it isn't a policy.

### 3. Fail closed, not open

When the allowlist is missing, malformed, or unreadable: **block all additional mounts**. Log loud, return `allowed: false`. The default must be "no extra filesystem surface."

Same rule for sender allowlists, credential policies, and tool grants. Any config read that returns `{}` because the file is missing should block, not permit.

(Sender-side note: nanoclaw's `sender-allowlist.ts` defaults to `{ allow: '*', mode: 'trigger' }` — that's fail-open on the sender side, which is a conscious tradeoff for a personal assistant. If you inherit this pattern for anything multi-tenant, flip it.)

### 4. Block-by-default patterns for sensitive paths

Even if an allowlist permits a root, reject paths that match any of:

```
.ssh   .gnupg   .gpg   .aws   .azure   .gcloud   .kube   .docker
credentials   .env   .netrc   .npmrc   .pypirc
id_rsa   id_ed25519   private_key   .secret
```

Match against both any path component and the full path string. Mount-time block, not read-time.

Additionally:

- Shadow `.env` with `/dev/null` in any mount that includes the project root.
- Never mount the channel-auth store (session cookies, Slack/Discord tokens).
- Credentials matching the blocked patterns are blocked regardless of allowlist entries — the deny-list is the final word.

### 5. Symlink resolution before policy check

Attackers control symlinks. A path like `~/projects/foo/.cache/redirect` can `realpath` to `~/.ssh`. Resolve every path with `realpathSync` (or equivalent) **before** checking it against the allowlist or block-list. Never policy-check the supplied path; always check the real path.

Corollary: if `realpathSync` fails (path doesn't exist), reject. Don't guess.

### 6. Container-path validation rejects injection

The container-side path (`-v host:container`) is an attack surface because Docker / container-runtime CLI parses its own syntax. Require the container path to:

- Be relative (never absolute — the runtime already prefixes a safe root like `/workspace/extra/`).
- Not contain `..` (path-traversal).
- Not contain `:` (Docker `-v` option-injection, e.g. `repo:rw` smuggling in a mode flag).
- Not be empty or whitespace-only.

Apply the same rules to any argv value that gets spliced into a shell-adjacent CLI. (See `webapp-testing` for the `shlex.split(posix=True)` + `shell=False` + per-server `--cwd` pattern already in force in the agency.)

### 7. Read-only project root; writable paths are listed explicitly

If the agent has access to the host application's source, mount the project root **read-only**. The handful of paths the agent legitimately needs to write — a store directory, the group folder, an IPC directory, a session's `.claude/` — get mounted separately in read-write mode, each narrow and named.

Rationale: otherwise the agent can edit its own host code (`src/`, `dist/`, `package.json`) and fully escape on the next host restart.

### 8. Per-tenant session isolation

Every group / tenant / channel gets isolated state:

- Per-group `.claude/` session directory → other groups cannot read this group's transcript, files-read list, or tool history.
- Per-group scratch / memory directory.
- Per-group credential scope (see rule 9).

Cross-tenant information disclosure via shared session state is a failure mode even if the outer container is tight.

### 9. Credentials never enter the sandbox

Real API credentials do not appear:

- In the agent container's environment.
- On stdin to the agent runner.
- In any mounted file.
- In `/proc/<pid>/environ` or `/proc/<pid>/stat`.

Instead, route outbound HTTPS through a gateway process on the host that matches requests by host + path and injects the real credential at egress. The nanoclaw reference implementation uses OneCLI Agent Vault; the same pattern works with any reverse-proxy vault (Vault agent, 1Password Connect, HashiCorp Boundary, AWS STS-assume-role proxy).

Per-tenant credential policies fall out naturally: each group gets its own agent identity, with rate limits, time-bound access, and approval flows as independent knobs.

## The privilege matrix (fill this in for your design)

Reviewers should ask for this table at the start of any agent-execution spec:

| Capability                  | Main / admin tier   | Untrusted tier       |
| --------------------------- | ------------------- | -------------------- |
| Project root access         | `/workspace/project` (**ro**) | None        |
| Writable store              | named dirs (rw)     | None                 |
| Group folder                | `/workspace/group` (rw) | `/workspace/group` (rw) |
| Global memory               | implicit            | `/workspace/global` (**ro**) |
| Additional mounts           | configurable        | ro unless allowlist permits rw |
| Network egress              | via vault, unrestricted scope | via vault, scoped policy |
| MCP tools                   | all                 | all (but vault-scoped creds gate reach) |

If "Untrusted tier" has strictly more capability than your threat model justifies, shrink it before shipping.

## Review checklist — paste into PRs

Copy this block verbatim into any PR that adds or changes an agent-execution surface:

```
## container-isolation-posture review

- [ ] Trust model named (main / other / container / input).
- [ ] Primary boundary is the container/VM, not app-level checks.
- [ ] Mount allowlist stored outside project root, not writable from agent.
- [ ] Config loaders fail closed (missing config = block).
- [ ] Block-by-default patterns enforced (.ssh, .env, .aws, credentials, …).
- [ ] All host paths resolved via realpath() before policy check.
- [ ] Container paths validated: no absolute, no `..`, no `:`, non-empty.
- [ ] Project root mounted read-only; writable paths listed explicitly.
- [ ] Per-tenant session / scratch / memory directories.
- [ ] Credentials routed through host-side vault; none in container env / stdin / files.
- [ ] Privilege matrix filled in and minimal.
```

A new surface that can't tick all ten boxes ships behind a flag or not at all.

## Pairs well with

- `sandbox` — the agency's existing execution skill. This skill defines the posture; `sandbox` implements a subset for shell commands.
- `mcp-defense` — consumer-side hardening for MCP tool calls. Same spirit, different layer.
- `mcp-author` / `mcp-authoring` — use this checklist when the MCP server runs any host-side process.
- `injection-defense` — prompt-injection surface lives at the trust-model boundary; this skill names the boundary so defense can focus.
- `secrets-vault` — implementing rule 9 in a specific vault ecosystem.
- `sdlc-patterns` — plan stage: "does this new surface need a container-isolation-posture review?" is a gate.

## What this skill never does

- Does not hand out a specific container runtime (Docker / containerd / Apple `container` / Podman / nerdctl) — language-agnostic.
- Does not specify a vault product — language-agnostic.
- Does not contain executable TypeScript / Python — the upstream `mount-security.ts` pattern is referenced but not ported, to keep this a design-guidance skill.
- Does not replace `red-team` reviews — it tees up what red-team looks for.

## License

Lineage: design patterns distilled from MIT-licensed source in `qwibitai/nanoclaw@v1.2.53` (`docs/SECURITY.md`, `src/mount-security.ts`). © 2026 Gavriel. No code ported; only the posture + checklist, rewritten for DevSecOps-Agency v0.3.6. See `LICENSES/MIT-nanoclaw.txt`.
