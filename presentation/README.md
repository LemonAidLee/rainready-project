# RainReady presentation (HTML)

**The story deck for the 5-minute video** (v3, 22 Oct 2026). Not the submitted pitch deck. 13 slides, 1920 × 1080,
in a **paper-collage explainer style** (Vox-like): one long sheet of paper that the camera pans across, taped
black-and-white prints, newspaper clippings with torn edges, a yellow highlighter on key words, red hand-drawn
circles, arrows and strike-throughs, black label boxes, sticky notes. Type: Libre Franklin (headlines) and Source
Serif 4 (clippings, body). How to record it and where the demo goes: [../documentation/VIDEO_GUIDE.md](../documentation/VIDEO_GUIDE.md).

**History.** v1 (21 Oct): 14-slide deck in the website's dark style, [archive/index_v1_2026-10-21.html](archive/index_v1_2026-10-21.html).
v2 (22 Oct, team leader): reworked into a documentary-style story modelled on the team leader's earlier CoreX pitch (a
news-style cold open, the evidence, a persona, Aiman, the demo hand-off, then what's new, who it helps, feasibility,
the pilot and next steps, the value and the close), still dark, [archive/index_v2_dark_2026-10-22.html](archive/index_v2_dark_2026-10-22.html).
v3 (22 Oct, team leader): same content and timing, restyled as a paper-collage explainer.

**Open:** serve the folder (`python -m http.server` here, then http://127.0.0.1:8000); fonts load from Google Fonts,
so stay online. Keep `assets/` next to it.

| Key | Action |
|---|---|
| → · Space · PageDown · click | If the slide's beats are still playing, show them all; otherwise next slide |
| ← · PageUp | Previous slide |
| R | Replay the current slide's beats (for a retake) |
| Home / End | First / last slide |
| F | Full screen (record at 1920 × 1080) |
| N | Voice-over script for the slide |
| number, then Enter | Jump to a slide; the address also takes `#7` |

**Beats.** Each slide plays a timed sequence when it arrives: pieces slap down onto the paper with a small bounce,
words pop in, the highlighter sweeps over key words, red lines draw themselves, and earlier points fade to grey when
the next arrives. In the markup, `data-at="s"` reveals an element s seconds in; `data-dim` / `data-lit` dim and
restore it; `data-fx` picks the entrance (`slap`, `pop`, `rise`, `left`, `right`, `fade`, `words`); `<mark data-at>`
is the highlighter; `.draw` paths draw on. Slide-specific moments: the print flooding against a ruler (1), the
annotated drain-crossing map (5), red string pinning the clippings together (6), the browser print that hands over
to the demo (7, cut to the recording), strike-throughs on "Today" (8), the red circle around 28 (12). Every beat time
is scaled by `--tempo` (0.8) in the CSS.

**Backdrop.** A faint topographic map (contour rings, a winding river, survey grid) is drawn once by script across the
whole sheet and pans at 45 % of the camera speed, so every slide change has depth (parallax). Each slide adds one torn
paper patch or halftone shape behind its key piece (`.patch`, `.patch.kraft`, `.dots.droplet`, `.dots.disc`). The map is
decorative only: it is not BBR terrain and carries no data.

**Persona.** Aiman is an **illustrative persona** built from public reports, labelled as such on the slide. The quote
is written by us, not said by a real person; the three points beneath it are sourced.

Every figure on the slides is from [../research/TBD_VERIFY_RESOLUTION.md](../research/TBD_VERIFY_RESOLUTION.md),
[../research/HY_screening_inputs.md](../research/HY_screening_inputs.md) or the website's results; the screenshots in
`assets/` are from the website on 21 Oct 2026. Team names are not on the slides yet **[TBD — team]**.

## Photo credits and licences (assets/photos)

Downloaded from Wikimedia Commons on 21 Oct 2026; licences checked on each file page. Shown with credit on the slide.

| File | What | Author | Licence |
|---|---|---|---|
| `klang_aerial_2021.jpg` | Aerial view of a flooded area in Klang, 21 Dec 2021 | AiMediaMY | CC BY 3.0 |
| `shahalam_s24_street_2021.jpg` | Knee-deep water, Section 24, Shah Alam, 19 Dec 2021 (not BBR) | Muhammad Zaim | CC BY-SA 4.0 |
| `shahalam_s24_park_2021.jpg` | Flooded park, Section 24, Shah Alam, 19 Dec 2021 (spare, not used) | Muhammad Zaim | CC BY-SA 4.0 |

No openly licensed photo of a flood **in Bandar Bukit Raja itself** was found. News photos of BBR floods (Sinar Harian,
FMT, The Star) are copyrighted: use them only with the outlet's permission. Better still, ask the residents'
associations for their own photos with written consent.

## Data on the problem slides

| Figure | Source |
|---|---|
| 363 / 273 / 258 / 247 mm in 24 h (Sentul, Sg. Bonus, Jinjang, Gombak), 17–18 Dec 2021; KL annual 2,400 mm | Environment and Water Ministry, via [FMT, 19 Dec 2021](https://freemalaysiatoday.com/category/nation/2021/12/19/one-months-rainfall-in-one-day-a-once-in-a-century-event) |
| RM6.1 bn losses in 2021; living quarters RM1.6 bn; vehicles RM1.0 bn | [DOSM, Special Report on Impact of Floods 2021, 28 Jan 2022](https://www.dosm.gov.my/portal-main/release-content/special-report-on-impact-of-floods-in-malaysia-2021) |
| Worst flood Dec 2021, water reached 3 m (residents); latest flash flood 24 Apr 2024, about a foot; 583 residents, 48 associations; "four shallow ponds"; water from Setia Alam | [FMT, 24 May 2024](https://freemalaysiatoday.com/category/nation/2024/05/24/developers-local-councils-need-to-hash-out-flood-issues-say-bandar-bukit-raja-folk) |
| Phase 1, especially Jalan Makyong, "badly hit" after over two hours of rain | [The Star, 5 Jun 2023](https://thestar.com.my/news/nation/2023/06/05/dramatic-day-in-klang-due-to-floods) |
| Jalan Makyong floods at least three times a year | [Sinar Harian, 25 May 2024](https://www.sinarharian.com.my/ampArticle/666626) |
| JPS ponding records at BBR, 2023 and 2024 | JPS Selangor GIS (see ../research/TBD_VERIFY_RESOLUTION.md) |

The KL gauges are in the Klang Valley, not in Klang district; the slide says "Klang Valley". The national loss figure
is context only, not the main argument (house rule).

**v2 (22 Oct 2026):** the story deck uses the Klang aerial photo only (slide 1); the Section 24 photo, the national
loss figures and the Brief and resident screenshots are no longer shown, because the demo shows the product. The
"2 years running" figure on slide 3 is the JPS ponding record above. The note below refers to v1's slide numbers.

**21 Oct 2026 (v1):** slide 8 now shows `assets/brief_record.jpg` (the Brief's seven-line responsibility record, captured from
the website's local build) instead of `brief_crop.jpg`, which showed an older Brief (kept, unused). Slide 8's record line
and slide 13's pilot measure ("0 of 7 lines confirmed today, 7 of 7 by month 12") follow
[../research/RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md).
