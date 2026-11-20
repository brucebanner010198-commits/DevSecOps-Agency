#!/usr/bin/env python3
"""Lint and repair YAML frontmatter in agent and skill files.

Claude Code drops every frontmatter field except the name when the YAML
fails to parse, so a broken file silently loses its `tools:` allowlist and
`model:` tier. The usual cause is a plain `description:` scalar that holds
`: ` or runs over several lines (for example `<example>` blocks).

    python scripts/frontmatter.py check   # exit 1 if any file fails to parse
    python scripts/frontmatter.py fix     # rewrite failing descriptions

`fix` touches only files that fail to parse. It turns the description into a
literal block scalar (`description: |-`) holding the same text, line for
line, and leaves every other byte of the file alone. It then re-parses the
file and checks that the parsed description equals the original text; if
not, the file is left unchanged and reported.

Needs PyYAML.
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Top-level frontmatter keys in use. A line starting with one of these, outside
# an <example> block, ends the description. Lines such as `user:` or
# `Context:` inside examples are part of the description, not keys.
KEYS = (
    "name", "description", "model", "color", "tools", "metadata", "version",
    "license", "lineage", "author", "category", "triggers", "toolsets",
    "compatibility", "disable-model-invocation", "effort", "maxTurns",
    "skills", "memory", "permissionMode", "isolation", "hooks", "background",
    "disallowedTools", "mcpServers", "initialPrompt", "activation", "access",
    "workers",
)
KEY_RE = re.compile(r"^(%s):" % "|".join(re.escape(k) for k in KEYS))


def targets() -> list[Path]:
    files = glob.glob(str(ROOT / "agents" / "**" / "*.md"), recursive=True)
    files += glob.glob(str(ROOT / "skills" / "**" / "SKILL.md"), recursive=True)
    return sorted(Path(f) for f in files if Path(f).name != "AGENTS.md")


ANY_KEY_RE = re.compile(r"^[A-Za-z_][\w-]*:(\s|$)")


def split(text: str) -> tuple[str, str, str] | None:
    """Return (frontmatter, closing-delimiter-and-body, newline) or None.

    The closing delimiter must be a whole line `---`, not a prefix such as
    `----- example`.
    """
    nl = "\r\n" if text.startswith("---\r\n") else "\n"
    opener = "---" + nl
    if not text.startswith(opener):
        return None
    m = re.compile(re.escape(nl) + r"---(?=" + re.escape(nl) + r"|$)").search(text, len(opener) - len(nl))
    if m is None:
        return None
    return text[len(opener):m.start()], text[m.start():], nl


def load(fm: str):
    """Parse frontmatter; return (mapping, None) or (None, error)."""
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as exc:
        return None, str(exc).splitlines()[0]
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    if "description" in data and not isinstance(data["description"], str):
        return None, "description is not a string"
    return data, None


def parses(fm: str) -> str | None:
    return load(fm)[1]


def example_state(line: str, in_example: bool) -> bool:
    """Track <example> nesting through a line, in the order tags appear."""
    for tag in re.findall(r"</?example>", line):
        in_example = tag == "<example>"
    return in_example


def description_span(lines: list[str]) -> tuple[int, int] | None:
    """Index of the description line and one past its last line."""
    starts = [i for i, l in enumerate(lines) if l.startswith("description:")]
    if len(starts) != 1:
        return None
    start = starts[0]
    in_example = example_state(lines[start], False)
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if not in_example and KEY_RE.match(line):
            break
        in_example = example_state(line, in_example)
        end += 1
    if in_example:
        return None  # unclosed <example>: cannot tell where the description ends
    return start, end


def repair(fm: str, nl: str) -> tuple[str, str] | str:
    """Return (new frontmatter, original description text), or a refusal reason.

    Refuses anything it cannot rewrite with certainty; a refused file is left
    untouched and reported.
    """
    lines = fm.split(nl)
    span = description_span(lines)
    if span is None:
        return "description missing, duplicated, or has an unclosed <example>"
    start, end = span
    first = lines[start][len("description:"):].lstrip(" ")
    if not first.strip():
        return "description value starts on a later line"
    if first[:1] in "\"'>|&*!%@`#{[":
        return "description is not a plain scalar"
    body = lines[start + 1:end]
    # Separator blank lines before the next key stay outside the block, as-is.
    n_trailing = 0
    while n_trailing < len(body) and body[len(body) - 1 - n_trailing] == "":
        n_trailing += 1
    body = body[:len(body) - n_trailing]
    # ` #` outside an example could be an intended YAML comment; inside an
    # example it is quoted prose (e.g. a markdown heading).
    in_example = example_state(lines[start], False)
    if " #" in first.split("<example>")[0]:
        return "' #' outside <example> (ambiguous comment)"
    for line in body:
        if line[:1] in (" ", "\t"):
            return "indented continuation line (would be folded by YAML)"
        if line.startswith("#"):
            return "comment line inside description"
        if not in_example and ANY_KEY_RE.match(line):
            return "key-like line outside <example> inside description: " + line.split(":")[0]
        if not in_example and " #" in line:
            return "' #' outside <example> (ambiguous comment)"
        in_example = example_state(line, in_example)
    raw = [first] + body
    block = ["description: |-"] + [("  " + l) if l else "" for l in raw]
    rest = lines[:start] + lines[end - n_trailing:]
    new = lines[:start] + block + lines[end - n_trailing:]

    # Independent checks: the frontmatter without the description must parse,
    # the fixed frontmatter must parse to exactly that plus the description,
    # and no key may appear twice.
    others, err = load(nl.join(rest)) if any(l.strip() for l in rest) else ({}, None)
    if err is not None:
        return "frontmatter without the description does not parse: " + err
    keys = [l.split(":", 1)[0] for l in rest if ANY_KEY_RE.match(l)]
    if len(keys) != len(set(keys)):
        return "duplicate top-level key"
    fixed, err = load(nl.join(new))
    if err is not None:
        return "still fails: " + err
    original = "\n".join(raw)
    if fixed.get("description") != original:
        return "parsed description differs from original text"
    if {k: v for k, v in fixed.items() if k != "description"} != others:
        return "other keys changed"
    return nl.join(new), original


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "check"
    if mode not in ("check", "fix"):
        print(__doc__)
        return 2
    failed, fixed, refused = [], [], []
    for path in targets():
        text = path.read_bytes().decode("utf-8")
        parts = split(text)
        rel = path.relative_to(ROOT).as_posix()
        if parts is None:
            failed.append((rel, "starts with a UTF-8 BOM" if text.startswith("﻿") else "no frontmatter"))
            continue
        fm, rest, nl = parts
        err = parses(fm)
        if err is None:
            continue
        if mode == "check":
            failed.append((rel, err))
            continue
        result = repair(fm, nl)
        if isinstance(result, str):
            refused.append((rel, result))
            continue
        new_fm, _ = result
        path.write_bytes(("---" + nl + new_fm + rest).encode("utf-8"))
        fixed.append((rel, sorted(load(new_fm)[0])))
    for rel, err in failed:
        print(f"FAIL  {rel}: {err}")
    for rel, keys in fixed:
        print(f"FIXED {rel}: keys={','.join(keys)}")
    for rel, err in refused:
        print(f"SKIP  {rel}: {err}")
    total = len(targets())
    print(f"{total} files; {len(failed)} failing; {len(fixed)} fixed; {len(refused)} refused")
    return 1 if failed or refused else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
