# collision-policy.md

How skill-creator handles a name collision on the path it's about to write.

## Rule

Refuse by default. Return to the CEO with the existing path + last-modified timestamp.

## Exceptions

| Case                                                  | Action                                    |
| ----------------------------------------------------- | ----------------------------------------- |
| Same file, `metadata.version` bump requested by user  | Edit in place, bump minor or patch.       |
| User says "replace the old agent"                     | Require CEO to stage a `_archive/<name>-<ts>.md` copy first, then overwrite. |
| File exists but is empty or malformed frontmatter     | Treat as collision; refuse. CEO repairs.  |
| Different kind (`skills/foo/` vs `agents/<council>/foo.md`) | Allowed — no collision.             |

## Return format on collision

```
file: <path that already exists>
kind: collision
existingVersion: <metadata.version from frontmatter or "unknown">
note: "refused — CEO must archive or bump version"
```

## Never

- Silently overwrite.
- Write a `.bak` or `.old` file; archive goes under `_archive/` with timestamp suffix.
- Merge two agents' personas into one file.
