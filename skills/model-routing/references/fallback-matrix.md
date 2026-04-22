# fallback-matrix

Same-tier lateral fallbacks. Updated via ADR when a new vendor enters / exits the matrix.

## Opus tier (CEO only)

| Primary | Fallback 1 | Fallback 2 |
| --- | --- | --- |
| claude-opus-4.6 | claude-opus-4.5 | gpt-5-thinking (Opus-class) |

## Sonnet tier (Chiefs)

| Primary | Fallback 1 | Fallback 2 |
| --- | --- | --- |
| claude-sonnet-4.6 | claude-sonnet-4.5 | gpt-5 (Sonnet-class) |
| | | gemini-2.5-pro |

## Haiku tier (specialists)

| Primary | Fallback 1 | Fallback 2 |
| --- | --- | --- |
| claude-haiku-4.5 | claude-haiku-4 | gpt-5-mini (Haiku-class) |
| | | gemini-2.5-flash |

## Emergency upgrade rule

If Haiku tier has no working fallback, specialists may temporarily run on Sonnet for the duration of the override. This is an upgrade, not a downgrade, so it's permitted — but it still needs the opening + closing ADR like any other override.

## Forbidden moves

- Any downward tier crossing (Sonnet → Haiku, Opus → Sonnet).
- Any cross-family jump without a prior scout report.
- Any silent routing change that doesn't tag session logs.

## Updates

Adding / removing a vendor from this matrix is an ADR trigger. Pair with a fresh scout report on the incoming vendor.
