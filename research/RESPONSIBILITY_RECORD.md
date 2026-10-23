# Responsibility Record: What We Have, and How "Who Maintains It?" Is Decided

**Written for:** the team leader and the teammate building the resident door (features 5–6). **As of:** 21 October
2026 (revised the same day with the Selangor State Assembly answers). **Concept:** feature 7 in
[RAINREADY_CONCEPT_V2.md](../documentation/RAINREADY_CONCEPT_V2.md) section 4. It feeds the Brief (feature 4), the
planner's cards and the routing of resident reports (feature 5). **Wins over:** the first version of this note and
[TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md) item 16 (which rested on one newspaper report).

House rule: the record says **who maintains** an asset under the published rules, never who is to blame. Each line
has a confidence, and each party can confirm or correct its own line.

## 1. The finding in three lines

1. Selangor has **written rules** for who maintains drains, rivers and retention ponds (state cabinet decisions,
   stated in the State Assembly). Every line of the record now rests on one of them.
2. **Ponds A and B, the two biggest assets, have no settled maintainer on public record.** Three official rules point
   to three different holders, and the deciding fact (have they been handed over?) is not public.
3. **None of the seven lines has been confirmed by the party itself.** That is the gap the record exists to close: the
   pilot's measure is how many lines each party confirms.

## 2. The rules (official sources)

All from the Selangor State Assembly's published questions and answers (`dewan.selangor.gov.my`, read 21 Oct 2026).

| # | Rule | Source | Conf. |
|---|---|---|---|
| R1 | MSMA retention ponds are **owned by the state** (built on state land) and **maintained by the local council (PBT)**; JPS is responsible only for rivers and flood-mitigation works | 2014 session 2, Q8 "Penyelenggaraan Kolam Takungan Saliran Mesra Alam", citing the **Cabinet decision of 6 June 1996**, ministry minutes of 23 May 2011 and a State Treasury letter of 8 Sep 2005 | H (the rule) |
| R2 | **The developer maintains retention ponds not yet handed over.** Developer ponds are gazetted only after the whole development is complete. Handover needs as-built plans and survey before the CCC. 547 ponds awaited gazetting in 2020: 296 held by JPS or councils, 247 by developers | 2020 session 3, Q284 "Serahan Kolam Takungan Oleh Pemaju Kepada JPS" | H (the rule) |
| R3 | Main drains linked to rivers (including unowned ones) → **JPS Selangor**. Secondary and tertiary drains linked to main drains → **the local council**. Drains in JKR road reserves → **JKR**, except main drains linked to rivers. Farm drains → JPS. Handover to the agencies expected in 2027 | 2025 session 3, Q229 "Saliran, Parit dan Sungai yang Tidak Bertuan", citing state cabinet decision **MMKN 17/2025 of 4 June 2025** | H (the rule) |
| R4 | Tributaries (anak sungai) → **JPS**. For a monsoon drain, the signboard on site says whether the council or JPS maintains it | 2022 session 1, Q27 "Penyenggaraan Sungai dan Longkang" | H (the rule) |
| R5 | Councils clean residential and monsoon drains twice a month (2015 SOP); in many councils the cleaning is done by contractors such as KDEB Waste Management | 2015 session 2, Q182 "Penyelenggaraan Longkang"; 2024 session 3, Q137; [Malaysiakini 2022](https://malaysiakini.com/news/637120) | M |
| R6 | Which council: MBDK on the Klang side, MBSA on the Shah Alam side | OSM council boundary (used in the model) | H for the line as mapped |

What JPS's own pond register says about ponds A and B (`AppHydro/Kolam_Fasa_JPS`, layer `kolam_fasa_1`, read 21 Oct
2026): K02 (12 acres, lot 63232, "kawasan kolam") and K03 (14 acres, lots 62804 and 46963, "kawasan kolam takungan"),
surveyed 2 Sep 2011 by JPS staff. **The land-title field (HAKMILIK) is blank for both.** The register lists the ponds;
it does not say who maintains them.

## 3. The record (seven lines)

| Asset | Mapped as | Who maintains it, by the rules | Rule | Conf. | Confirmed by the party |
|---|---|---|---|---|---|
| **Pond A** | OSM 399570465; JPS K02 | **Not settled.** Sime Darby Property while not handed over (R2); MBDK once handed over, with the state as owner (R1). JPS lists it | R1, R2 | L | No |
| **Pond B** | OSM 359496461; JPS K03 | **Not settled**, as pond A | R1, R2 | L | No |
| **Shared trunk drain** | OSM ditch chain, council corner to the main ditch | **MBDK**: a secondary drain linked to a main drain, Klang side | R3, R6 | M | No |
| **Main ditch** | OSM way 888406336 | **JPS Selangor**: a main drain linked to a river | R3 | M | No |
| **Council-line crossing drain** | OSM drain at 3.09294 N, 101.44433 E | **MBSA** above the line, **MBDK** below it | R3, R6 | M | No |
| **Street drains** (what residents report) | Many; not mapped one by one | **The council of the side they are on** (MBDK or MBSA), cleaned by its contractor; **JKR** if inside a JKR road reserve | R3, R5 | M | No |
| **Sungai Keramat** | River reach south of zone Z03 | **JPS Selangor** (rivers and tributaries) | R1, R4 | M | No |

"M" means: an official rule applies and our reading of which class the asset falls in is reasonable, but the party has
not confirmed it. "L" means the deciding fact is not public.

**Changes from the first version:** ponds A and B moved from "JPS Selangor, M" to "not settled, L" (the register lists
them but R1 and R2 give maintenance to the council or the developer); the three drains moved from L to M (the rule is
now the state cabinet's, not a newspaper's paraphrase); street drains and Sungai Keramat added.

## 4. The decision logic: "who maintains this, and how sure are we?"

A cascade: the **first step that applies wins**, and it sets the confidence. The same logic answers the resident
door's question, "where should this report go?".

| Step | Question about the asset | If yes | Conf. |
|---|---|---|---|
| 1 | Has the party itself **confirmed** its line? | That party | **H** |
| 2 | Is it a **retention pond not yet handed over** by its developer? | The developer (R2) | M if the handover status is documented; otherwise **not settled** (L) |
| 3 | Is it a **retention pond that has been handed over**? | The council maintains, the state owns (R1) | M |
| 4 | Is it a **river or tributary**? | JPS Selangor (R1, R4) | M |
| 5 | Is it a **main drain linked to a river**? | JPS Selangor (R3) | M |
| 6 | Is it inside a **JKR road reserve**? | JKR, unless it is a main drain (R3) | M |
| 7 | Is it a **secondary or tertiary drain** linked to a main drain? | The council of its side (R3, R6) | M |
| 8 | Is it a **monsoon drain** whose class is unclear? | Read the signboard on site (R4) | L until checked |
| 9 | Does it **cross the council line**? | Split at the line (R6) | M |
| 10 | None of these | **"Not known: ask"**, shown as a gap, never guessed | — |

### Worked examples

- **Pond A** → step 2 applies, but the handover status is not public → **not settled** (L). One letter from JPS, MBDK or
  Sime Darby Property settles it, and the line moves to step 1 (H).
- **Shared trunk drain** → steps 2–6 do not apply → step 7: a secondary drain linked to the main ditch, Klang side →
  MBDK (M).
- **A resident reports a blocked street drain on Jalan Makyong** → step 7 → MBDK, cleaned by its contractor (M). The
  report goes to that party's **existing channel** (iClean Selangor or Sispaa), with a link. If the drain is in a JKR
  road reserve, step 6 sends it to JKR.

## 5. Where it shows

| Where | What |
|---|---|
| Brief | The seven-line table, with rule, confidence and "confirmed by the party" |
| Planner view | Zone and pond cards: who maintains the pond or drain the zone feeds, and its street drains |
| Pitch | "Even the two biggest assets have no settled maintainer on public record"; pilot measure: lines confirmed by the party (0 of 7 today) |
| Resident door (feature 5) | Routing of reports by the cascade above |

## 6. Open

- [TBD] Handover status of ponds A and B (JPS, MBDK or Sime Darby Property; one letter settles it).
- [verify] The trunk drain's class (secondary vs main) and whether any stretch lies in a JKR road reserve: the signboard
  or the council's drain inventory would settle it.
- [verify] Which contractor cleans MBDK's drains today (KDEB Waste Management is reported for several councils).
