/**
 * Parity check: network.ts must match network.py (the reference) number for number and key for key.
 *
 *   node --experimental-strip-types check_network.ts          (from simulations/platform)
 *
 * Cases: every site's inputs.json in sites/, edge cases, a branched network, and 200 randomly perturbed copies of
 * each (every numeric value scaled by 0.2-3). Relative tolerance 1e-9. Exits 1 on any mismatch. Needs `python`.
 */
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { run, type Inputs } from "./network.ts";

const HERE = dirname(fileURLToPath(import.meta.url));
const tmp = mkdtempSync(join(tmpdir(), "rr-network-"));

function python(cases: Inputs[]): unknown[] {
  const f = join(tmp, "cases.json");
  writeFileSync(f, JSON.stringify(cases));
  const code = "import json, sys; sys.path.insert(0, sys.argv[1]); import network; " +
    "print(json.dumps([network.run(c) for c in json.load(open(sys.argv[2], encoding='utf-8'))]))";
  return JSON.parse(execFileSync("python", ["-c", code, HERE, f], { encoding: "utf-8", maxBuffer: 1 << 29 }));
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
function scale(node: any, rnd: () => number) {
  if (node && typeof node === "object") {
    if (typeof node.value === "number") node.value *= 0.2 + 2.8 * rnd();
    for (const v of Object.values(node)) scale(v, rnd);
  }
}
let seed = 20261022;
const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2 ** 31) / 2 ** 31);

const bases: [string, Inputs][] = readdirSync(join(HERE, "sites"))
  .filter((s) => existsSync(join(HERE, "sites", s, "inputs.json")))
  .map((s) => [s, JSON.parse(readFileSync(join(HERE, "sites", s, "inputs.json"), "utf-8"))]);

// a branched network: BBR's trunk drain split in two in series, a second pond releasing straight to the outfall
const bbr = bases.find(([s]) => s === "bbr")![1];
const branched = clone(bbr);
branched.drains.upper = { ...clone(bbr.drains.trunk_drain), drains_to: "trunk_drain", council: "Shah Alam" };
branched.zones.Z01.drains_to = "upper";
branched.external_inflows.EXT_A.drains_to = "upper";
branched.ponds.pond_B.drains_to = "outfall";
bases.push(["branched", branched]);

const cases: [string, Inputs][] = [];
for (const [name, base] of bases) {
  cases.push([name, clone(base)]);
  const edge = (what: string, f: (c: Inputs) => void) => { const c = clone(base); f(c); cases.push([`${name}: ${what}`, c]); };
  edge("no allowed release", (c) => { c.method.c_predevelopment.value = 0; });
  edge("every drain 40 % blocked", (c) => { for (const d of Object.values<any>(c.drains)) d.blockage = { value: 0.4 }; });
  edge("blockage over the cap", (c) => { for (const d of Object.values<any>(c.drains)) d.blockage = { value: 1.5 }; });
  edge("storm held at 1 h", (c) => { c.storm.design_duration_h = { value: 1 }; });
  edge("storm held at a duration not listed", (c) => { c.storm.design_duration_h = { value: 4 }; });
  edge("capacities removed", (c) => { for (const p of Object.values<any>(c.ponds)) p.capacity_m3 = { value: null }; });
  edge("capacities entered", (c) => { for (const p of Object.values<any>(c.ponds)) p.capacity_m3 = { value: 50000 }; });
  edge("no councils", (c) => { for (const k of ["zones", "external_inflows", "drains", "ponds"]) for (const n of Object.values<any>(c[k] ?? {})) delete n.council; });
  edge("what-if ponds overflow", (c) => { for (const w of Object.values<any>(c.what_if_ponds ?? {})) w.capacity_m3 = { value: 10 }; });
  for (let k = 0; k < 200; k++) { const c = clone(base); scale(c, rnd); cases.push([`${name}: random #${k}`, c]); }
}

const py = python(cases.map(([, c]) => c));
let bad = 0;
cases.forEach(([name, c], j) => {
  const out: string[] = [];
  diff(py[j], JSON.parse(JSON.stringify(run(c))), name, out);
  if (out.length) { bad++; if (bad < 6) console.log(`MISMATCH in ${name}:\n  ` + out.slice(0, 8).join("\n  ")); }
});
console.log(bad ? `${bad} of ${cases.length} cases differ` : `parity OK: ${cases.length} cases (${bases.map(([s]) => s).join(", ")}), every output field matches`);
process.exit(bad ? 1 : 0);
