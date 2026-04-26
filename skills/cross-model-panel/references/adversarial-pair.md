# Adversarial-pair mode (v0.6.0)

The v0.5.7 baseline runs a parallel panel where every panelist evaluates from their own perspective. Adversarial-pair adds an **explicit affirmative/negative role assignment** for two of the four panelists: one is asked to make the strongest case FOR a position, the other to make the strongest case AGAINST. The remaining two panelists evaluate normally. The Multi-Agent Debate literature (Khan et al. 2024, Liang et al. 2024) reports adversarial framing measurably improves blind-spot detection on questions where a single-perspective panel converges to a wrong answer with high confidence.

This mode is **opt-in** and appropriate ONLY for questions with a defensible binary or ternary frame (e.g., "Should we adopt approach X?" / "Is finding F actually ASI-class?" / "Does this design satisfy requirement R?"). It is INAPPROPRIATE for open-ended generative questions ("How should we structure...?").

## When to use adversarial-pair

Appropriate triggers:

- **ASI-class finding determination where the initial verdict is split or low-confidence.** Adversarial framing forces the strongest "this IS ASI-class" case and the strongest "this is NOT ASI-class" case to be explicit, then the panel ranks both arguments.
- **Architectural decision with two clearly-named alternatives** where a parallel panel might converge prematurely to one without honest stress-testing of the other.
- **Compliance / policy disputes** where a single-perspective panel might miss the steel-strongest counter-argument.

INAPPROPRIATE for:

- Open-ended questions ("How should we approach...?")
- Questions with > 3 reasonable positions
- Routine decisions
- Constitution amendment proposals (use parallel single-round per Anthropic CCAI ensemble-robustness finding — adversarial framing introduces unnecessary polarization on amendment work)

## Procedure

### Pre-flight: identify the frame

The convening council MUST specify the frame as part of the panel request. Three valid frames:

- **Binary:** "FOR position X" vs "AGAINST position X"
- **Comparative:** "STRONGEST case for option A" vs "STRONGEST case for option B"
- **Verdict:** "ARGUE that finding F is ASI-class" vs "ARGUE that finding F is NOT ASI-class"

If the question doesn't fit one of these frames, fall back to the v0.5.7 parallel panel procedure.

### Role assignment

Two of the four panelists are assigned roles. The other two run the standard parallel procedure. The role-assignment rotates per panel (per `panel-rotation.md`'s rotation rules) so the same model isn't always "affirmative."

**Default assignment:**
- Slot 1 (Opus 4): AFFIRMATIVE
- Slot 2 (Sonnet 4.5): NEGATIVE
- Slot 3 (Haiku 4.5): PARALLEL (standard, no role)
- Slot 4 (Opus 4 with thinking): PARALLEL (standard, no role)

**Independence rule:** the panel-chair MUST log the role assignment in the ADR and rotate so that any given model has been AFFIRMATIVE no more than 60% of the time across the trailing 10 panels. This prevents the panel from becoming a stable "Opus argues yes, Sonnet argues no" pattern that the Chairman could systematically discount.

### Stage 1 prompts (role-specific)

**AFFIRMATIVE prompt (Slot 1):**

```
You are being consulted as one of four panelists on a hard question. For this panel, you have been assigned the AFFIRMATIVE role.

Your job is to make the strongest possible case for: <FRAME_AFFIRMATIVE>

You may believe this position is wrong. That is irrelevant for this round — your job is to steel-man it. Cite the strongest evidence, the strongest reasoning, the strongest precedents. Acknowledge weaknesses honestly but argue past them.

After your case is collected, you will see the NEGATIVE panelist's case and two parallel-panel responses, and you will rank all four anonymized.

Original question:
<QUESTION>

Make the strongest case FOR <FRAME_AFFIRMATIVE>. Length: as long as the substance requires, default ≤ 600 words.
```

**NEGATIVE prompt (Slot 2):** mirror image of AFFIRMATIVE, against the same position.

**PARALLEL prompts (Slots 3 + 4):** standard Stage 1 prompt from `stage-prompts.md`.

### Stage 2 (anonymized peer review)

Identical to v0.5.7 dual-ordering. The anonymized labels do NOT reveal which slot was AFFIRMATIVE/NEGATIVE/PARALLEL — peer evaluators see four anonymous responses and rank on substance. Role assignment is de-anonymized only in the ADR after Stage 2 completes.

### Stage 3 (Chairman synthesis)

Chairman receives all four raw responses with role labels revealed PLUS the ranking. Chairman prompt addition:

```
Two panelists were assigned adversarial roles: AFFIRMATIVE made the strongest case FOR <FRAME_AFFIRMATIVE>, NEGATIVE made the strongest case AGAINST. Two panelists ran a standard parallel evaluation.

Your synthesis MUST:
1. Identify the strongest argument from EACH side.
2. Identify the rebuttal that the other side did NOT successfully address.
3. Take a position with stated reason — but do not pretend the question is settled if both sides have unrebutted strong arguments. In that case, recommend the question be deferred to the User with both cases attached.
4. Note that the AFFIRMATIVE and NEGATIVE responses do NOT necessarily represent those panelists' actual beliefs — they were assigned roles. Do not infer model bias from these responses; their role-assigned outputs are not their general output.
```

## ADR fields added by adversarial-pair mode

```yaml
mode: adversarial-pair
frame: binary  # or comparative, verdict
frame_text:
  affirmative: "Finding F is ASI-class"
  negative: "Finding F is NOT ASI-class"
role_assignment:
  - panelist: 1
    role: AFFIRMATIVE
  - panelist: 2
    role: NEGATIVE
  - panelist: 3
    role: PARALLEL
  - panelist: 4
    role: PARALLEL
role_history_check:
  panelist_1_affirmative_pct_last_10: 50  # MUST be ≤ 60
  panelist_2_negative_pct_last_10: 40    # MUST be ≤ 60
  rotation_compliant: true
chairman_verdict:
  position: "Finding F IS ASI-class"
  unrebutted_arguments_remaining: false  # if true, defer to User
```

## Why role-rotation matters

If the same model is always AFFIRMATIVE on a category of questions, two failure modes appear:

1. **Apparent model bias** — observers wrongly conclude "Opus is always pro-X" when in fact Opus was assigned the AFFIRMATIVE slot every time.
2. **Chairman compensation** — a Chairman who learns "the Opus response is always FOR" might systematically discount it, losing the calibration benefit of the adversarial mode.

The 60% cap is the documented rotation threshold from the Multi-Agent Debate Strategies survey for adversarial settings.

## Cost

Same model-call count as a v0.5.7 single-round panel (~13 equivalents). The role-assignment doesn't add cost; it changes prompt content. **No multi-round coupling** in v0.6.0 — adversarial-pair is single-round only. Multi-round adversarial is deferred to v0.6.1+ because the funneling effect compounds with the role-induced polarization in ways the literature hasn't fully characterized.

## Anti-patterns

- **Don't run adversarial-pair without a clear frame.** If the question doesn't fit binary/comparative/verdict, fall back to parallel.
- **Don't reveal role assignment in Stage 2.** The anonymized peer review evaluates substance, not role. Role labels appear only in the ADR.
- **Don't combine adversarial-pair with multi-round in v0.6.0.** Deferred to v0.6.1+ pending literature review.
- **Don't infer model bias from a model's adversarial-role output.** It's role-assigned content, not general output.
- **Don't run adversarial-pair on Constitution amendment proposals.** Use parallel single-round per Anthropic CCAI.
- **Don't let the same model be AFFIRMATIVE more than 60% of trailing-10 panels.** Rotate per `panel-rotation.md` updated rules.
