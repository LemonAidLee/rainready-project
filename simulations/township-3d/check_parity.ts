/**
 * Parity check: screening.ts must match screening.py (the reference) number for number.
 *
 *   node --experimental-strip-types check_parity.ts          (from simulations/township-3d)
 *
 * Runs both on inputs.json, on edge cases and on 200 randomly perturbed copies of inputs.json (every numeric value
 * scaled by 0.2-3, with and without entered pond capacities), and compares every output field (relative tolerance
 * 1e-9) and the key order. Exits 1 on any mismatch. Needs `python` on the PATH.
 */
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { run, type Inputs } from "./screening.ts";

const HERE = dirname(fileURLToPath(import.meta.url));
const base: Inputs = JSON.parse(readFileSync(join(HERE, "inputs.json"), "utf-8"));
const drawn: Record<string, number> = Object.fromEntries(
  JSON.parse(readFileSync(join(HERE, "data", "zones.json"), "utf-8")).zones.map((z: any) => [z.id, z.area_ha]));
const tmp = mkdtempSync(join(tmpdir(), "rr-parity-"));

function python(cases: Inputs[]): unknown[] {
  const f = join(tmp, "cases.json");
  writeFileSync(f, JSON.stringify(cases));
  const code = "import json, sys; sys.path.insert(0, sys.argv[1]); import screening; " +
    "print(json.dumps([screening.run(c) for c in json.load(open(sys.argv[2], encoding='utf-8'))]))";
  return JSON.parse(execFileSync("python", ["-c", code, HERE, f], { encoding: "utf-8", maxBuffer: 1 << 28 }));
}

function diff(a: unknown, b: unknown, path: string, out: string[]) {
  if (typeof a === "number" && typeof b === "number") {
    if (Math.abs(a - b) > 1e-9 * Math.max(1, Math.abs(a), Math.abs(b))) out.push(`${path}: py ${a} vs ts ${b}`);
  } else if (a && b && typeof a === "object" && typeof b === "object") {
    const ka = Object.keys(a as object), kb = Object.keys(b as object);
    if (ka.join() !== kb.join()) out.push(`${path}: keys py [${ka}] vs ts [${kb}]`);
    for (const k of ka) diff((a as any)[k], (b as any)[k], `${path}.${k}`, out);
  } else if (a !== b) out.push(`${path}: py ${JSON.stringify(a)} vs ts ${JSON.stringify(b)}`);
}

const clone = (x: Inputs): Inputs => JSON.parse(JSON.stringify(x));
function scale(node: any, rnd: () => number) {           // multiply every numeric input value by 0.2-3
  if (node && typeof node === "object") {
    if (typeof node.value === "number") node.value *= 0.2 + 2.8 * rnd();
    for (const v of Object.values(node)) scale(v, rnd);
  }
}
let seed = 20261021;
const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2 ** 31) / 2 ** 31);

const cases: [string, Inputs][] = [["inputs.json", clone(base)]];
const edge = (name: string, f: (c: Inputs) => void) => { const c = clone(base); f(c); cases.push([name, c]); };
const sec = (c: Inputs) => c.trunk_drain.section;
edge("trunk drain tiny", (c) => { sec(c).top_width_m.value = 0.5; sec(c).bottom_width_m.value = 0.3; });
edge("trunk drain huge", (c) => { sec(c).top_width_m.value = 200; sec(c).depth_m.value = 10; });
edge("no allowed release (C_pre 0)", (c) => { c.method.c_predevelopment.value = 0; });
edge("capacities entered", (c) => { c.ponds.pond_A.capacity_m3.value = 100000; c.ponds.pond_B.capacity_m3.value = 90000; });
edge("what-if pond overflows", (c) => { c.what_if_pond.capacity_m3.value = 10; });
edge("what-if pond huge outlet", (c) => { c.what_if_pond.outlet_m3_s.value = 1e4; });
edge("what-if pond no capacity", (c) => { c.what_if_pond.capacity_m3.value = null; });
edge("trunk drain 30 % blocked", (c) => { c.trunk_drain.blockage.value = 0.3; });
edge("trunk drain blockage over the cap", (c) => { c.trunk_drain.blockage.value = 1.5; });
edge("no blockage input (older inputs)", (c) => { delete c.trunk_drain.blockage; });
edge("storm held at 1 h", (c) => { c.storm.design_duration_h.value = 1; });
edge("storm held at 24 h, drain blocked", (c) => { c.storm.design_duration_h.value = 24; c.trunk_drain.blockage.value = 0.3; });
edge("storm held at a duration not listed", (c) => { c.storm.design_duration_h.value = 4; });
edge("10-year ARI", (c) => { c.storm.ari_years.value = 10; });
edge("a placeholder left (illustrative)", (c) => { c.storm.tc_hours.status = "placeholder"; });
for (let k = 0; k < 200; k++) {
  const c = clone(base);
  if (k % 2) { c.ponds.pond_A.capacity_m3.value = 150000; c.ponds.pond_B.capacity_m3.value = 80000; }
  if (k % 3 === 0) c.trunk_drain.blockage.value = 0.4;   // scaled below to 0.08-1.2, so the cap is exercised too
  scale(c, rnd);
  cases.push([`random #${k}`, c]);
}

const py = python(cases.map(([, c]) => c));
let bad = 0;
cases.forEach(([name, c], j) => {
  const out: string[] = [];
  const ts = run(c, drawn);
  diff(py[j], JSON.parse(JSON.stringify(ts)), name, out);   // JSON round trip, as Python's json writes it
  if (out.length) { bad++; console.log(`MISMATCH in ${name}:\n  ` + out.slice(0, 8).join("\n  ")); }
});
console.log(bad ? `${bad} of ${cases.length} cases differ` : `parity OK: ${cases.length} cases, every output field matches`);
process.exit(bad ? 1 : 0);
