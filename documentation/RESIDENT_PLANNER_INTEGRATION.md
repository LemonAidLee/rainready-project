# Resident Door ↔ Planner View: How Reports Become Pins

**Written for:** the teammate building the resident door (features 5 and 6) and the team leader. **As of:** 21 October
2026. **Concept:** feature 5 says a report "appears as a pin in the planner view". This note says how that can work
when the resident app tracks real locations anywhere, and the planner view shows only one simulated township.
**Related:** [WEBSITE.md](WEBSITE.md) (the planner view), [../research/RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md)
(who a report goes to).

## 1. The key fact: the planner model is on real coordinates

The 3D township is simulated, but it is **georeferenced**. Its ponds, drains, main ditch, council line and the three
flood streets are placed from OpenStreetMap at their real positions. Only the town fabric (most houses) is invented.
So a real GPS point lands on the right street in the model.

| Item | Value |
|---|---|
| Model origin | **3.0900 N, 101.4360 E** (centre of the mapped extent) |
| Mapped extent | **3.0845–3.0955 N, 101.4250–101.4470 E** (about 2.45 × 1.22 km) |
| Lat/lon → model metres | `x = (lon − 101.436) × 111158` (east) · `y = (lat − 3.09) × 110572` (north) |
| Already used by | The planner view's cursor readout (`website/src/ui/Shell.tsx`), which does the reverse |

At this scale the flat conversion is accurate to well under a metre, far finer than a phone's GPS (typically 5–20 m).

## 2. Three cases for a report's location

| Where the report is | What the planner view does |
|---|---|
| **Inside the mapped extent** | A pin at its position, attached to the nearest mapped drain or street, with its **zone** (Z01–Z09) and the **owner** from the responsibility record |
| **Just outside** (the upstream side in Setia Alam, or neighbouring Klang estates) | Not dropped. A marker at the model's edge pointing towards it, with a count ("3 reports north of the model"). Upstream reports matter most: they are the cross-boundary evidence |
| **Far away** (another town) | Listed in a "reports outside this catchment" panel only. The planner view is one catchment; another township would get its own model |

This answers the mismatch: the resident door can work anywhere, and the planner view shows what falls in its
catchment, plus what flows into it.

**Built (21 Oct 2026):** the site's landing page is a Malaysia map that already draws reports in this format
(`website/public/data/reports_example.json`, EXAMPLE records) next to JPS Selangor's real flood records, and zooming
into Bandar Bukit Raja opens the planner view. Replacing the example file with the resident door's file or feed is the
join ([WEBSITE.md](WEBSITE.md) section 8).

**Built (21 Oct 2026, later the same day):** the resident door is the teammate's **Waterline** system, ported into the
site (`website/src/resident/`, [WEBSITE.md](WEBSITE.md) section 13). It keeps its own report record (issue, description,
location text, `locationCoordinates`, status, updates, photo); `toShared()` in `resident/store.ts` converts it to the
format below for the Malaysia map. Status mapping: Reported → `new`, Checked by association → `verified`, Sent to
[holder] → `forwarded`, Cleared → `resolved`. Reports are browser-local (option A in section 5, without a file); a
backend would give option B with no change to the readers.

## 3. What the two parts exchange: one report record

The resident door owns the reports. The planner view only **reads** them. A shared format lets both be built
separately and joined at the end.

```json
{
  "id": "r-000123",
  "created_at": "2026-11-02T18:40:00+08:00",
  "lat": 3.0921, "lon": 101.4338, "accuracy_m": 12,
  "type": "blocked_drain",
  "status": "verified",
  "verified_by": "residents_association",
  "forwarded_to": { "channel": "iClean Selangor", "url": "…" },
  "note": "Drain grating blocked with leaves",
  "example": true
}
```

| Field | Values | Notes |
|---|---|---|
| `type` | `blocked_drain`, `flooded_street`, `other` | Matches the concept's two report types |
| `status` | `new` → `verified` → `forwarded` → `resolved` | The "visible status" in feature 5 |
| `verified_by` | `residents_association`, or empty | The association checks before a report counts |
| `forwarded_to` | channel name and link | RainReady forwards to the existing channel (iClean Selangor, Sispaa); it never runs its own hotline |
| `example` | `true` for any sample data | The planner view marks these EXAMPLE, as the mock-ups do now |

Fields the planner view **adds itself** on reading: model x/y, zone, nearest asset, owner and confidence.

## 4. Real-time location: what crosses over, and what does not

The resident app tracks location live; the planner view **must not**.

| Stays on the phone | Crosses to the planner view |
|---|---|
| The live location track | **One point per report**, at the moment of reporting |
| The move-now plan's "nearest higher ground" (worked out on the phone) | — |
| Name, phone number, photos of people | Nothing that identifies the resident |

Reasons: a planner needs *where the drain is*, not *where the person is*. Showing live positions of residents
would be a privacy risk, and it is not needed for any feature. Malaysia's Personal Data Protection Act 2010 may
apply to location data held by a commercial service [verify scope]. Plan for consent on first use, and keep only
what the report needs.

**Feature 6 (move-now plan)** needs data in the other direction: the planner model can supply the "example"
higher-ground spots and the zone each street is in, as a small file the resident door reads.

## 5. How to join them for the competition

| Option | How | When it fits |
|---|---|---|
| **A. Shared sample file** | The resident door writes reports in the format above; a copy sits in the website's `public/data/reports.json`. Pins appear from it, marked EXAMPLE | The demo and the video. Works even if the resident app is not online on the day |
| **B. Live feed** | The resident door's backend serves the same records at a URL the planner view reads every ~30 s (cross-origin allowed) | If the backend is hosted and stable by then. The video's "pin appears" moment would be real |

Both use the same format, so going from A to B changes only where the file comes from.

## 6. Decisions for the team leader and the resident-door teammate

1. Agree the report format in section 3 (or the teammate's version of it). **This is the only hard dependency.**
2. Option A, B, or A now and B later.
3. Whether the planner view shows pins as **points** or **counts per zone**. Counts are safer for privacy and
   readable at overview zoom; points are needed to show the nearest drain.
4. Who supplies the sample reports for the video, and that each is marked as an example.

**Open:** the resident survey on reporting channel preference has no responses yet ([TBD], concept section 7).
