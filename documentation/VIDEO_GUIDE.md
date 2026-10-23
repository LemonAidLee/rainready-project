# Video guide (5 minutes)

How to make the required 5-minute video from the **story deck** ([../presentation/](../presentation/README.md), v3 of
22 Oct 2026, paper-collage style) and the website's **guided demo** (https://rainready-wheat.vercel.app/#/demo). Written for the team
leader. v1 of this guide (21 Oct) was for the old 14-slide presentation, now archived in `presentation/archive/`.

## 1. The shape

The structure follows the team leader's earlier CoreX pitch: hook the viewer with a real event, show the evidence,
meet the person with the problem, hand over to the live demo, then come back to the slides for innovation, users,
feasibility, the pilot, the value and the close.

```
 slides 1–7 (story, ~1:33)  →  guided demo (~1:39)  →  slides 8–13 (the case, ~1:34)
```

Every slide plays **timed beats** when it opens (all beat times are scaled by `--tempo` in the deck's CSS, now 0.8; lower it to speed everything up): pieces slap onto the paper, words pop in, a yellow highlighter marks the key words, and
earlier points dim. Let each slide's beats finish before moving on (→ finishes them early; **R** replays them).

## 2. Outline (target 4:46; timecodes as in VIDEO_SCRIPT.md)

| Time | # | Slide | On screen | Judging criterion |
|---|---|---|---|---|
| 0:00–0:15 | 1 | **Cold open** | Klang, Dec 2021, in rain. "One month's rain fell in a single day." Water rises against a ruler to "3.0 m, as residents describe it" | Impact |
| 0:15–0:20 | 2 | **Title** | RainReady. *Property lines stop at the fence. Water doesn't.* | — |
| 0:20–0:39 | 3 | **It keeps happening** | 3× a year · 2 years of JPS ponding records · 583 residents; then the MD's "top priority" quote | Impact, Strategic fit |
| 0:39–0:59 | 4 | **Meet Aiman** | Illustrative persona, a drainage engineer at a developer, and the question they can't answer today | Impact |
| 0:59–1:15 | 5 | **The crossing** | Paper map: rain on Setia Alam → one drain crosses the council line → shared drain → ponds A and B fill | Innovation (the insight) |
| 1:15–1:30 | 6 | **The gap** | Five real programmes as clippings; a red string pins them together. "A shared picture is." | Innovation |
| 1:30–1:33 | 7 | **Meet RainReady** | The prototype print, its address typing in: **cross-fade to the demo** | — |
| 1:33–3:12 | — | **Guided demo** | Demo steps 2–10, 12, 14–15 (table below) | Feasibility, Innovation |
| 3:12–3:32 | 8 | **What's new** | Today vs with RainReady, five rows struck through; "We claim the combination" | Innovation |
| 3:32–3:39 | 9 | **Who it helps** | "Now Aiman can show everyone their part": SDP, both councils, JPS, residents | Impact, Strategic fit |
| 3:39–4:10 | 10 | **Can it work** | Already working vs honest limits, each limit with what closes it; "Decision support under uncertainty, not prediction" | Feasibility, Evidence |
| 4:10–4:26 | 11 | **Pilot and next** | 12-month timeline, four next steps, our ask | Feasibility, Commercial |
| 4:26–4:33 | 12 | **The value** | 28 townships | Commercial value |
| 4:33–4:46 | 13 | **Close** | Three lines, tagline, link | — |

### Demo steps to show

| Demo step | Title | Keep? | Time |
|---|---|---|---|
| 1 | Flooding is a national problem (map) | Skip | – |
| 2 | One shared picture | Keep, short | 0:06 |
| 3 | Property lines stop at the fence | Keep, short (slide 5 set it up) | 0:06 |
| 4 | Where residents say it floods, and where JPS recorded it | Keep | 0:06 |
| 5 | A 100-year design storm | Keep | 0:10 |
| 6 | Today: how much the ponds must hold | Keep | 0:07 |
| 7 | The next parcels upstream | Keep | 0:05 |
| 8 | The shared drain carries more | Keep | 0:08 |
| 9 | A fix on the table: a new pond | Keep | 0:10 |
| 10 | The biggest unknown: the drain's size | Keep | 0:11 |
| 11 | Keep it working | Skip | – |
| 12 | The findings, on one page (Brief) | Keep | 0:08 |
| 13 | Checked against the ground | Skip (slide 10 says it) | – |
| 14 | The resident door | Keep | 0:11 |
| 15 | Reports land on the shared picture | Keep | 0:11 |
| 16 | Close | Skip | – |
| | **Total** | | **~1:39** |

If the video runs long, cut demo step 7 first, then shorten step 3.

## 3. Voice-over script

The full outline, shooting script (screen and voice-over, scene by scene, with timecodes) and a read-through script
for the recording are in **[VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)**, which is the master copy. The deck's voice-over panel
(**N**) holds the same slide lines.

## 4. Before you record

- **Same numbers everywhere.** Check the demo captions against the script (steps 6, 8, 9).
- **Screen.** Display at 1920 × 1080, scaling 100 %, browser zoom 100 %. Turn on Do Not Disturb, and hide the
  bookmarks bar.
- **Warm up.** Open the live site and the deck once before recording, so the 3D model, fonts and photo are cached.
- **Deck.** In `presentation/`, run `python -m http.server`, open http://127.0.0.1:8000, press **F** for full
  screen. Keep the voice-over panel (**N**) **off** while recording.

## 5. Recording

Record **pictures and voice separately**. It is much easier to fix one sentence than a whole take.

1. **Voice first.** Read the script in section 3 in a quiet room (phone recorder or Audacity, 15–20 cm from the mic),
   one file per slide. Re-read any line you stumble on.
2. **Slides.** Screen recorder: **OBS Studio** (Display Capture, 1920 × 1080, 30 fps, MP4) or **Win + Alt + R**
   (Xbox Game Bar). On each slide, **wait for the beats to finish** and hold 2 seconds before pressing →. Don't press →
   during the beats: it skips them. If a slide goes wrong, press **R** to replay it and keep recording; cut the bad
   part later. Record slides 1–7 as one clip and 8–13 as another.
3. **Slide 7 is the hand-off.** Let the address finish typing, hold a second, then stop. In the editor, cut (or
   cross-fade over ~0.5 s) from the framed screenshot straight to the demo clip.
4. **Demo.** Open **https://rainready-wheat.vercel.app/#/demo?clean** in full screen (F11). `clean` hides the controls
   and cursor but keeps the caption and status label, which must stay on screen. Press **→** at your own pace: let each
   camera move finish and hold 2–3 seconds. Step quickly through the skipped steps (1, 11, 13); cut them later.

## 6. Editing

- **Editor:** Clipchamp (built into Windows 11) is enough; CapCut or DaVinci Resolve also work.
- Lay the **voice down first**, then fit the clips to it. The beats are timed close to the script, so most slides
  need only trimming. Where a clip is slower than the voice, speed it up (up to ~1.5× looks fine) rather than cutting
  in the middle of an animation.
- **Slide 1 has no voice for its first second.** Optionally add soft rain sound under it (royalty-free only).
- **Subtitles burned in.** Judges may watch muted. Use auto-captions, then **fix every number and name** by hand
  (Makyong, Setia Alam, MSMA, JPS, Aiman).
- **Credits.** The Klang aerial photo (slide 1) is CC BY 3.0; its credit is on the slide, so keep it visible.
- Export **1080p MP4**, **under 5:00**. Check the length in the exported file, not in the editor.

## 7. Hand-in

- Upload to YouTube as **Unlisted**, or to Google Drive with **"Anyone with the link can view"**.
- **Test the link in a private window**, signed out: the rules require a video that opens without asking for
  permission.
- Put the link in the submission form.

## 8. House rules to keep

- **No predicted flood depths.** The 3 m on slide 1 is the residents' account of 2021, and the slide says so. In the
  demo, say "storage falls short", never "the water will be X metres".
- **Neutral tone.** Say "a difference, not blame". Slide 4's "residents say councils and developers shift the blame"
  is attributed to residents (FMT); don't add to it.
- **Aiman is illustrative.** Never present the persona or the quote as a real person.
- **Advisory, not forecast** for the resident door: it always "builds on official warnings".
