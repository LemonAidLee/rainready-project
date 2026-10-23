# Research

RainReady research findings, one file per question. The questions come from the Google Sheet's
[Research List](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit).
**Where two files disagree, [TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md) wins** (21 Oct 2026).

## Index

| Track | File | Answers |
|---|---|---|
| All | [TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md) | How every [TBD] and [verify] was settled, or replaced by a stated assumption. **Read first** |
| Architecture | [AR1_study_area_selection.md](AR1_study_area_selection.md) | Which part of BBR the simulated township is based on |
| Architecture | [AR1_site_model.md](AR1_site_model.md) + [AR1_site_model/](AR1_site_model/) | What is modelled, what is measured and what is assumed; the GIS layers, terrain and imagery checks |
| Hydrology | [HY_screening_inputs.md](HY_screening_inputs.md) | The simulator's inputs, sourced from MSMA 2 and public data; result and sensitivity |
| Hydrology | [HY_ASSUMPTIONS_CHECK.md](HY_ASSUMPTIONS_CHECK.md) | A check of the two assumptions the result rests on |
| Hydrology | [FASTFLOOD_CROSSCHECK.md](FASTFLOOD_CROSSCHECK.md) | An independent cross-check of the screening model with FastFlood |
| Team leader | [RESPONSIBILITY_RECORD.md](RESPONSIBILITY_RECORD.md) | What the official rules say about who maintains ponds and drains |
| Team leader | [AFTER_THE_FLOOD.md](AFTER_THE_FLOOD.md) | Who does what when a township floods (source for the website's "After the water") |
| Team leader | [THREE_CHALLENGES_REVIEW.md](THREE_CHALLENGES_REVIEW.md) | Three challenges to the pitch: built towns, who pays for losses, more towns than BBR |
| Team leader | [SCALING_PLATFORM.md](SCALING_PLATFORM.md) | What ties the product to BBR, ideas for making it planner software for any township, and appendix slide text |

## Format for new files

Use the same shape every time, so findings can go straight into the judge appendix without being rewritten:

```
# <ID> — <the question>

**Owner:** · **Date:** · **Confidence:** H / M / L

## Answer in five lines
## Evidence          (every claim with its source and its own confidence label)
## Assumptions       (anything we had to assume, and what would change if it is wrong)
## Limits            (what this does not tell us)
## One figure        (a chart, map or diagram, if the finding has one)
```

Rules: never invent a number, a quote or a source. Mark unconfirmed items **[verify]** and blanks **[TBD]**.
Keep the wording neutral about the developer, the councils and the residents.

## Archive

[archive/](archive/) is kept for the record and isn't part of the current project. Nothing is deleted. See
[archive/README.md](archive/README.md).
