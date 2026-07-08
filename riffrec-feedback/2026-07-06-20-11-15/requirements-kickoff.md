---
date: 2026-07-06
topic: 2026-07-06-20-11-15
---

# 2026 07 06 20 11 15

## Problem Frame

A product feedback source for `unknown` produced evidence of product friction. The raw source has been converted into transcript, selected moments when video is available, screenshots when frames can be extracted, and candidate findings so the team can decide what product behavior should change before planning implementation.

Source materials for brainstorm:
- Source materials manifest: `riffrec-feedback/2026-07-06-20-11-15/source-materials.md`
- Analysis: `riffrec-feedback/2026-07-06-20-11-15/analysis.md`
- Problem analysis: `riffrec-feedback/2026-07-06-20-11-15/problem-analysis.md`
- Review prompt with transcript and frames: `riffrec-feedback/2026-07-06-20-11-15/review-prompt.md`

---

## Actors

- A1. User: Operates the product in the recorded session and verbalizes friction.
- A2. Product surface: The UI and backend behavior visible in the recording.
- A3. Brainstorm agent: Uses the evidence bundle to confirm, correct, and group requirements before planning.

---

## Key Flows

- F1. Evidence-backed feedback triage
  - **Trigger:** A feedback zip, video, audio file, or meeting notes file is available.
  - **Actors:** A1, A2, A3
  - **Steps:** Extract or copy the source, transcribe media or read notes, select high-signal moments when video exists, inspect screenshots when available, confirm problems, and write requirements with supporting evidence.
  - **Outcome:** Confirmed product problems are represented as requirements with transcript support and screenshot support when visual evidence exists.
  - **Covered by:** R1, R2, R3

---

## Requirements

**Evidence handling**
- R1. Each confirmed product problem must cite supporting transcript, notes, or moment evidence from the source, including timestamp and screenshot when video is available.
- R2. Transcript claims must be tied to the closest visible interaction or explicitly marked as untimed verbal context.

**Product requirements from this session**
- R3. Resolve or intentionally scope the issue described by F1: No obvious failure detected automatically.

---

## Acceptance Examples

- AE1. **Covers R1, R2.** Given a feedback source with voice, video, or notes, when the analysis is complete, each promoted issue includes source evidence rather than prose-only claims.
- AE2. **Covers R3.** Given the user reports that a button is weird or unclickable, when requirements are finalized, the requirement identifies the specific control and the expected available/unavailable behavior.

---

## Success Criteria

- A human reviewer can understand what went wrong without rewatching the entire recording.
- `ce-brainstorm` can confirm requirements from linked source evidence before any planning begins.

---

## Scope Boundaries

- The analyzer output is evidence and requirements kickoff material, not final implementation design.
- Automatically detected findings remain candidates until screenshots are inspected.
- Development-only noise, such as profiler requests, should not become product requirements unless it affects the user experience.

---

## Key Decisions

- Evidence first: Requirements should cite moments and screenshots before moving to planning.
- Brainstorm before plan: Use `ce-brainstorm` to refine product behavior when the recording reveals ambiguity.

---

## Dependencies / Assumptions

- Source session URL: `unknown`.
- Source materials manifest: `riffrec-feedback/2026-07-06-20-11-15/source-materials.md`.
- Candidate findings: F1.
- Screenshot evidence: M1: `riffrec-feedback/2026-07-06-20-11-15/frames/m1-6.85s-representative-video-frame.png`; M2: `riffrec-feedback/2026-07-06-20-11-15/frames/m2-20.56s-representative-video-frame.png`; M3: `riffrec-feedback/2026-07-06-20-11-15/frames/m3-34.27s-representative-video-frame.png`; M4: `riffrec-feedback/2026-07-06-20-11-15/frames/m4-47.97s-representative-video-frame.png`; M5: `riffrec-feedback/2026-07-06-20-11-15/frames/m5-61.68s-representative-video-frame.png`.

---

## Outstanding Questions

### Resolve Before Planning

- Which candidate findings are real product problems after screenshot review?
- For each promoted finding, what should the user experience be instead?

### Deferred to Planning

- [Technical] Which code paths own the confirmed product behavior?
- [Technical] What regression tests should lock the behavior once fixed?

---

## Next Steps

-> Resume `/ce-brainstorm` to confirm candidate findings and replace generic R-items with product-specific requirements.
