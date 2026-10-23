# Upstream Runoff Simulation

A buildless interactive teaching tool showing how upstream impervious development can increase runoff volume, accelerate peak discharge, and overwhelm a constrained downstream drain.

## Run locally

From this directory:

```powershell
python -m http.server 4173 --directory dist
```

Then open `http://127.0.0.1:4173`.

## Model assumptions

- Catchment area: 1 km².
- Pervious runoff coefficient: 0.15.
- Impervious runoff coefficient: 0.90.
- The weighted coefficient determines total generated runoff.
- A conceptual linear reservoir routes the upstream runoff. Imperviousness and engineered drainage reduce the routing delay.
- Downstream ponding accumulates whenever incoming flow is higher than the selected drain capacity.

This is a conceptual educational model. It is not suitable for engineering design, flood-map production, or safety decisions without local rainfall, soil, topography, drainage geometry, and model calibration.
