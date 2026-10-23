# HydroShield → RainReady: Integration and Enhanced Problem Statement

**Written for:** the team (Eujin, the track leads, the team leader). **Status:** proposal for the team to accept or change; nothing here has been adopted yet.
**Source of HydroShield:** Eujin's sections in the Google Doc "SDP Documentation" (read 20 Oct 2026).
**Rules that apply:** [README.md](../README.md) house rules. Risk bands, never depths. Advisory, never forecast. Neutral wording.

---

## 1. The idea in one paragraph

HydroShield and RainReady describe the same gap from two sides. HydroShield asks *"how does a developer show that its
side did its job?"* RainReady asks *"how do all parties see the same water?"* The strongest version is RainReady's
neutral shared picture with HydroShield's two sharpest ideas built in: **an account of inflow versus capacity** (Shield)
and **a cross-boundary check before building** (Sandbox). Both survive if they show flows and capacity and leave the
verdict to the reader.

---

## 2. What we take, reword or drop

| HydroShield element | Decision | Why | RainReady form |
|---|---|---|---|
| Tagline "Property boundaries stop at the fence. Water doesn't." | **Take**, lightly reworded | Says the cross-boundary idea in one line | "Property lines stop at the fence. Water doesn't." |
| "Good Developer Trap" (developer blamed for water from outside) | **Reword** | Real insight, but written as defence of one party. Our evidence: residents say councils and developers shift blame, and causes are contested | "The party whose name is on the township is often the one blamed, whichever side the water came from" |
| Shield: measure outside water entering | **Take** | Answers the central dispute | **Boundary inflow account**: a range for upstream versus internal contribution, with assumptions shown |
| Shield: "proves compliance", Compliant/Breached | **Drop the verdict** | We have no pond depths, drain network or pump rates, so we cannot prove compliance. A verdict would also read as taking a side | Show **required storage versus stated capacity**, and the gap |
| "1-Click Audit Report" | **Take, reword** | A one-page output is useful to every party | **Shared Capacity Brief**: neutral, with sources, assumptions and confidence labels. Addressed to developer and councils alike |
| Sandbox: test earthworks before breaking ground | **Take** | The strongest forward-looking idea. Fits our pond what-if | **Before-you-build check** inside the what-if: "how does this change affect storage need downstream and upstream?" |
| "Upstream councils must co-fund" | **Drop** | Assigns blame and prescribes a settlement | "Shows who contributes what, so parties can agree shares" |
| Homepage: two cards, two buttons, trust bar | **Take the layout** | Good 30-second structure | Cards show *inflow versus capacity*, not innocent versus guilty |
| "+65% over baseline", "100% MSMA 2 compliant", "absorbing 100% rain", "award-winning", "RM50 million" | **Drop** | No source we have read supports any of them | Use only figures in [BBR_PUBLIC_DOCUMENT_SURVEY.md](../supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md) |
| "125 acres" / "50-acre" wetland | **Replace** | Our booklet figure is 130 acres of ponds, a design value | "Designed to hold 16,000 / 34,000 / 50,000 m³" |
| Water-level slider | **Keep the interaction, change the output** | Judges remember it | The slider changes how full each pond or zone is. Show fill as a **band**, not metres |
| Hourly fill-and-recede timeline | **Take** | Shows *when* capacity runs short | A scenario curve of inflow versus storage, labelled "scenario, not forecast" |
| Naming Gamuda, EcoWorld, IJM | **Reword** | Unsourced, and naming competitors adds risk | "Any master developer or council on a shared catchment" |
| "Powered for Sime Darby Property" | **Drop** | Reads as endorsement we do not have | Competition entry, not SDP product |

---

## 3. Enhanced problem statement (proposed v2)

> **Water crosses property lines and council boundaries. The plans, the maintenance records and the blame do not.
> Residents of flood-prone townships, the developers who built them and the councils that maintain them each see only
> their own part of one river system, so storage and drain upgrades are argued over after each flood instead of agreed
> before it.**

**The three moments where the gap shows up**

| Moment | What goes wrong today | Evidence |
|---|---|---|
| **Before building** | Drainage design is done parcel by parcel. Review is per development (JPS Selangor: 100-year ARI retention per application). We found no public cross-boundary check of what a change upstream does downstream (searched 20 Oct 2026; see [RAINREADY_CONCEPT_V2.md](../RAINREADY_CONCEPT_V2.md) section 10) | Residents link flooding to upstream development (FMT, 2024); causes contested (Deck Appendix A) |
| **During a storm** | Warnings are district-wide. A street cannot see what the warning means for it | MET and JPS warnings are by district (Deck Slide 6) |
| **After a flood** | Nobody can show who contributed what, or who owns the asset. Blame moves between parties | 583 residents and 48 associations; "councils and developers shift blame" (FMT); over 300 unmanned ponds, about 55 taken over (Bernama) |

**Who feels it**

- **Residents:** repeated flooding, at least three times a year by their account (Sinar Harian).
- **Developers:** carry the public and reputational pressure for the township, whichever side the water came from.
  SDP's managing director called it "quite urgent" and "a top priority" (The Edge, **year to verify**). *(Confidence M:
  inferred from the quotes and the dispute, not measured.)*
- **Councils and agencies:** funded programmes exist on both sides (Shah Alam RM150m, Klang 17 urgent projects, the
  Taman Mutiara pond, the August 2026 joint strategy) but run separately.

**What is missing is not effort. It is one shared picture across the boundary.**

---

## 4. Enhanced solution (proposed v2)

**Plan before. Warn during. Account after. One shared picture.**

| Moment | RainReady feature | What HydroShield adds |
|---|---|---|
| **Before** | Catchment view · **Retention-pond what-if** | **Before-you-build check** (Sandbox): test a pond change or earthworks and see the storage gap move, upstream and downstream |
| **During** | **Street-level advisories** on official warnings | Nothing. Stays as is, advisory only |
| **After** | **Responsibility record** | **Boundary inflow account and Shared Capacity Brief** (Shield): required storage versus stated capacity, upstream and internal shares as ranges, owners and confidence labels |

The four existing features stay. HydroShield contributes the **before-you-build check**, the **inflow account** and the
**one-page brief**, and sharpens the demo.

### 4.1 Shared Capacity Brief, contents

1. The scenario: design storm, assumptions, date.
2. Required storage versus stated capacity, with each capacity figure labelled **sourced**, **assumed** or **[TBD]**.
3. Inflow shares as a **range** (for example "between X% and Y% enters from the upstream catchment under these assumptions"),
   with a confidence label. No single exact percentage.
4. Who maintains each asset involved, with confidence.
5. Risk bands for streets, linked to the official warning pages.
6. What would change the answer (the assumption ledger entries that matter most).

It states no compliance verdict and no fault.

### 4.2 Demo story for judges (30 seconds)

1. Two cards for BBR: **"Capacity (designed)"** and **"Inflow entering across the boundary (scenario)"**.
2. Move the rainfall slider. The ponds and low-lying zones change band.
3. Switch on a "change upstream" scenario. The gap grows. Add a pond. The gap shrinks.
4. Open the one-page brief.

### 4.3 AI layer: what from Eujin's list fits

| Eujin's idea | Fit | Note |
|---|---|---|
| Land-cover to runoff-coefficient extractor | **Possible** | Supports the "change upstream" scenario. Output is an estimate with a confidence label. Needs a validation check. Frontend and AI track to confirm |
| RAG over MSMA 2 and local plans with clause citations | **Possible** | Supports the responsibility record and the before-you-build check. Must cite the clause and link the source; "Section 4.2 / 3–5% OSD" in Eujin's example is invented and must not be used |
| Surrogate model for instant 2D flood spread | **Hold** | Only if outputs are bands. Anything that outputs depths conflicts with our rule |
| Rejected gimmicks (chatbot, AI-made flow, AI-made terrain) | **Agree** | Already in our guardrails |

---

## 5. What this changes in the pitch deck

| Slide | Change |
|---|---|
| 2 | Add the three-moment framing. Keep the evidence table as is |
| 4 | Show the feature table in 4 above. Add "before-you-build check" to the pond what-if |
| 5 | Add the Shared Capacity Brief as a fifth screen or as the output of Screen 2 |
| 6 | New differentiator: "one shared account of inflow and capacity that every party can read" |
| 7 | Add metric: share of brief assumptions that are sourced rather than assumed |
| Appendix | Add the brief's template and its limitations |

These are edits to propose, not made yet. [FLOOD_PITCH_DECK.md](../supporting/FLOOD_PITCH_DECK.md) is unchanged.

---

## 6. Open decisions for the team

1. **Primary user.** This merge supports **developer first, councils as co-users, residents as beneficiaries**. Confirm
   (also open decision 2 in [PROJECT_STATUS.md](../PROJECT_STATUS.md)).
2. **Name.** HydroShield as a name tilts towards defence. RainReady stays neutral. Keep RainReady, or use Eujin's
   tagline only.
3. **Lead features.** Candidates: the pond what-if with the before-you-build check, and the inflow account with the brief.
4. **Eujin's section ownership.** Decide who owns the Sandbox idea in the tracker (hydrology: inflow logic; frontend:
   brief and demo).

## 7. Verify before use

- Whether any public cross-boundary drainage design review exists in Selangor (underpins "before building" row).
- Any figure Eujin quoted that we want to keep. Each needs a source first. None is currently cleared.
- Whether MBDK or MBSA publishes a retention requirement we can cite.
- Whether a range for upstream share can be defended with the data we have (no catchment boundary yet; see
  [PROJECT_STATUS.md](../PROJECT_STATUS.md) section 9). If it cannot, the brief shows storage gap only and says why.
