"""Convert BBR's screening inputs (simulations/township-3d/inputs.json, one trunk drain, one what-if pond) into the
network format (network.py). Nothing is re-sourced: every value, status and source is carried over as it is.

The only additions are the sides of the council line for the trunk drain and the ponds, which inputs.json leaves
implicit: all three lie on the Klang side (TOWNSHIP_3D_AND_SIMULATOR.md 4.8; JPS pond list K02 and K03, Klang).

Run:  python bbr_to_network.py     -> writes sites/bbr/inputs.json (and network.py --check uses convert())
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "township-3d", "inputs.json")


def convert(bbr):
    net = json.loads(json.dumps(bbr))
    trunk = net.pop("trunk_drain")
    trunk.update(drains_to="outfall", council="Klang")
    net["drains"] = {"trunk_drain": trunk}
    for p in net["ponds"].values():
        p.update(drains_to="trunk_drain", council="Klang")
    wp = net.pop("what_if_pond")
    net["what_if_ponds"] = {"W1": wp}
    for sc in net["scenarios"].values():
        sc["what_if_ponds"] = ["W1"] if sc.pop("what_if_pond") else []
    net["_about"] = ("BBR's screening inputs in the network format, converted by bbr_to_network.py from "
                     "simulations/township-3d/inputs.json (the source; edit that, then re-run). " + bbr.get("_about", ""))
    return net


if __name__ == "__main__":
    out = os.path.join(HERE, "sites", "bbr", "inputs.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(convert(json.load(open(SRC, encoding="utf-8"))), open(out, "w", encoding="utf-8"), indent=1)
    print("wrote", out)
