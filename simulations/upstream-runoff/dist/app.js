const $ = (id) => document.getElementById(id);

const controls = {
  impervious: $('impervious'), rainfall: $('rainfall'), duration: $('duration'),
  drainSpeed: $('drainSpeed'), capacity: $('capacity')
};

const presets = {
  natural: { impervious: 20, rainfall: 55, duration: 1.5, drainSpeed: 20, capacity: 8, title: 'Natural hillside' },
  developed: { impervious: 75, rainfall: 55, duration: 1.5, drainSpeed: 82, capacity: 8, title: 'Developed upstream' },
  extreme: { impervious: 92, rainfall: 105, duration: 2.5, drainSpeed: 95, capacity: 8, title: 'Intense storm + hard surfaces' }
};

let state = { ...presets.natural };
let result = null;
let baseline = null;
let animating = false;
let animationStart = 0;
let simProgress = 0;
let rafId = 0;

const landscape = $('landscape');
const hydrograph = $('hydrograph');
const lctx = landscape.getContext('2d');
const hctx = hydrograph.getContext('2d');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

function runoffCoefficient(impervious) {
  const fraction = impervious / 100;
  return 0.15 * (1 - fraction) + 0.90 * fraction;
}

function simulate(input) {
  const dtMinutes = 3;
  const dtSeconds = dtMinutes * 60;
  const totalHours = input.duration + 6;
  const steps = Math.ceil(totalHours * 60 / dtMinutes);
  const coefficient = runoffCoefficient(input.impervious);
  const rainInflow = input.rainfall * 0.2777778 * coefficient;
  const tauHours = 2.6 - 2.25 * (input.drainSpeed / 100) - 0.55 * (input.impervious / 100);
  const tauSeconds = Math.max(0.25, tauHours) * 3600;
  const alpha = 1 - Math.exp(-dtSeconds / tauSeconds);
  let routedFlow = 0;
  let downstreamStorage = 0;
  let peakStorage = 0;
  let peak = 0;
  let peakTime = 0;
  const points = [];

  for (let i = 0; i <= steps; i++) {
    const hours = i * dtMinutes / 60;
    const generated = hours <= input.duration ? rainInflow : 0;
    routedFlow += (generated - routedFlow) * alpha;
    peak = Math.max(peak, routedFlow);
    if (routedFlow === peak) peakTime = hours;
    downstreamStorage = Math.max(0, downstreamStorage + (routedFlow - input.capacity) * dtSeconds);
    peakStorage = Math.max(peakStorage, downstreamStorage);
    points.push({ hours, flow: routedFlow, storage: downstreamStorage });
  }

  const rainfallVolume = input.rainfall * input.duration * 1000;
  const runoffVolume = rainfallVolume * coefficient;
  const infiltrationShare = Math.round((1 - coefficient) * 100);
  return { points, coefficient, runoffVolume, infiltrationShare, peak, peakTime, peakStorage, totalHours };
}

function formatVolume(value) {
  if (value >= 1e6) return `${(value / 1e6).toFixed(2)} million m³`;
  return `${Math.round(value).toLocaleString()} m³`;
}

function updateStateFromControls() {
  state = {
    impervious: +controls.impervious.value,
    rainfall: +controls.rainfall.value,
    duration: +controls.duration.value,
    drainSpeed: +controls.drainSpeed.value,
    capacity: +controls.capacity.value,
    title: 'Custom scenario'
  };
  document.querySelectorAll('.preset').forEach(button => button.classList.remove('active'));
  recalculate();
}

function updateRangeFill(input) {
  const percent = ((+input.value - +input.min) / (+input.max - +input.min)) * 100;
  input.style.setProperty('--fill', `${percent}%`);
}

function syncControls() {
  Object.keys(controls).forEach(key => {
    controls[key].value = state[key];
    updateRangeFill(controls[key]);
  });
  $('imperviousValue').textContent = `${state.impervious}%`;
  $('rainfallValue').textContent = `${state.rainfall} mm/h`;
  $('durationValue').textContent = `${state.duration} h`;
  $('capacityValue').textContent = `${state.capacity} m³/s`;
  $('drainSpeedValue').textContent = state.drainSpeed < 34 ? 'Slow' : state.drainSpeed < 68 ? 'Moderate' : 'Fast';
  $('scenarioTitle').textContent = state.title;
}

function recalculate() {
  result = simulate(state);
  baseline = simulate({ ...state, impervious: 20, drainSpeed: 20 });
  syncControls();
  updateMetrics();
  resizeAndDraw();
}

function updateMetrics() {
  $('infiltrationMetric').textContent = `${result.infiltrationShare}%`;
  $('runoffMetric').textContent = formatVolume(result.runoffVolume);
  $('peakMetric').textContent = `${result.peak.toFixed(1)} m³/s`;
  $('floodMetric').textContent = formatVolume(result.peakStorage);

  const ratio = result.peak / state.capacity;
  const badge = $('riskBadge');
  badge.className = 'risk-badge ' + (result.peakStorage > 1 ? 'flooding' : ratio > .8 ? 'watch' : 'safe');
  badge.querySelector('span').textContent = result.peakStorage > 1 ? 'Drain overwhelmed' : ratio > .8 ? 'Near capacity' : 'Within capacity';

  if (result.peakStorage > 1) {
    $('explanationTitle').textContent = 'The water arrives faster than the township can release it.';
    $('explanationBody').textContent = `Peak inflow is ${result.peak.toFixed(1)} m³/s, above the ${state.capacity} m³/s drain limit. The excess temporarily ponds downstream; harder surfaces and faster channels make the peak taller and earlier.`;
  } else if (ratio > .8) {
    $('explanationTitle').textContent = 'The downstream system has almost no spare capacity.';
    $('explanationBody').textContent = `Peak flow reaches ${Math.round(ratio * 100)}% of drain capacity. A slightly heavier or longer storm could push this scenario into flooding.`;
  } else {
    $('explanationTitle').textContent = 'The landscape is absorbing and delaying much of the storm.';
    $('explanationBody').textContent = `About ${result.infiltrationShare}% of rainfall does not become immediate surface runoff. The remaining flow is spread over time, keeping the peak below the downstream drain limit.`;
  }
}

function fitCanvas(canvas, ctx) {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const width = Math.max(1, Math.round(rect.width * dpr));
  const height = Math.max(1, Math.round(rect.height * dpr));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width; canvas.height = height;
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { width: rect.width, height: rect.height };
}

function drawLandscape(progress = 0) {
  const { width: w, height: h } = fitCanvas(landscape, lctx);
  const ctx = lctx;
  ctx.clearRect(0, 0, w, h);

  const sky = ctx.createLinearGradient(0, 0, 0, h);
  sky.addColorStop(0, '#13262e'); sky.addColorStop(1, '#0a171a');
  ctx.fillStyle = sky; ctx.fillRect(0, 0, w, h);

  const rainActive = animating || progress > 0;
  if (rainActive) {
    ctx.strokeStyle = `rgba(120, 192, 221, ${0.18 + state.rainfall / 600})`;
    ctx.lineWidth = 1;
    const density = Math.floor(25 + state.rainfall / 2);
    for (let i = 0; i < density; i++) {
      const x = ((i * 83 + progress * 430) % (w + 50)) - 25;
      const y = ((i * 47 + progress * 900) % (h * .73));
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 4, y + 11); ctx.stroke();
    }
  }

  const groundY = h * .70;
  ctx.beginPath();
  ctx.moveTo(0, h * .42);
  ctx.bezierCurveTo(w * .18, h * .35, w * .32, h * .50, w * .48, h * .58);
  ctx.bezierCurveTo(w * .64, h * .68, w * .76, groundY, w, groundY);
  ctx.lineTo(w, h); ctx.lineTo(0, h); ctx.closePath();
  const earth = ctx.createLinearGradient(0, h * .38, 0, h);
  earth.addColorStop(0, '#31533d'); earth.addColorStop(.25, '#294134'); earth.addColorStop(1, '#17251f');
  ctx.fillStyle = earth; ctx.fill();

  const impervious = state.impervious / 100;
  const roadStart = w * (0.08 + (1 - impervious) * .25);
  ctx.beginPath(); ctx.moveTo(roadStart, h * .43); ctx.lineTo(w * .66, groundY); ctx.lineTo(w * .73, groundY); ctx.lineTo(roadStart + 25, h * .43); ctx.closePath();
  ctx.fillStyle = '#3b4547'; ctx.fill();
  ctx.strokeStyle = '#788183'; ctx.setLineDash([10, 12]); ctx.beginPath(); ctx.moveTo(roadStart + 13, h * .44); ctx.lineTo(w * .695, groundY); ctx.stroke(); ctx.setLineDash([]);

  const buildings = Math.round(1 + impervious * 8);
  for (let i = 0; i < buildings; i++) {
    const t = i / Math.max(1, buildings - 1);
    const x = 35 + t * w * .48;
    const surfaceY = h * .42 + Math.pow(t, 1.35) * h * .16;
    const bw = 24 + (i % 3) * 7;
    const bh = 25 + (i % 4) * 9;
    ctx.fillStyle = i % 2 ? '#7b7d74' : '#8d887d'; ctx.fillRect(x, surfaceY - bh, bw, bh);
    ctx.fillStyle = '#242f31';
    for (let wy = surfaceY - bh + 7; wy < surfaceY - 5; wy += 9) for (let wx = x + 6; wx < x + bw - 4; wx += 10) ctx.fillRect(wx, wy, 4, 4);
  }

  const treeCount = Math.max(1, Math.round(10 * (1 - impervious)));
  for (let i = 0; i < treeCount; i++) {
    const x = 20 + ((i * 71) % Math.max(60, w * .5));
    const t = x / (w * .52);
    const y = h * .41 + Math.pow(t, 1.35) * h * .17;
    ctx.fillStyle = '#574b36'; ctx.fillRect(x, y - 17, 3, 18);
    ctx.fillStyle = '#67a874'; ctx.beginPath(); ctx.arc(x + 1, y - 20, 9, 0, Math.PI * 2); ctx.fill();
  }

  const riverY = groundY + 11;
  ctx.fillStyle = '#172c37'; ctx.fillRect(w * .52, riverY, w * .48, 21);
  const activeIndex = Math.min(result.points.length - 1, Math.floor(progress * (result.points.length - 1)));
  const active = result.points[activeIndex] || result.points[0];
  const capacityRatio = active.flow / state.capacity;
  ctx.fillStyle = capacityRatio > 1 ? 'rgba(70,144,225,.82)' : 'rgba(54,112,160,.66)';
  ctx.fillRect(w * .52, riverY + 15 - Math.min(14, capacityRatio * 10), w * .48, 8 + Math.min(14, capacityRatio * 10));

  const floodFraction = Math.min(1, active.storage / Math.max(1, result.peakStorage));
  if (active.storage > 1) {
    ctx.fillStyle = `rgba(55, 135, 220, ${.22 + floodFraction * .42})`;
    ctx.fillRect(w * .66, groundY - floodFraction * 28, w * .34, 28 + floodFraction * 28);
  }

  for (let i = 0; i < 5; i++) {
    const x = w * (.72 + i * .055), y = groundY - 30 - (i % 2) * 5;
    ctx.fillStyle = '#b7a687'; ctx.fillRect(x, y, 32, 30);
    ctx.fillStyle = '#6a5047'; ctx.beginPath(); ctx.moveTo(x - 3, y); ctx.lineTo(x + 16, y - 13); ctx.lineTo(x + 35, y); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#223033'; ctx.fillRect(x + 11, y + 13, 8, 17);
  }

  if (rainActive) {
    const flowDots = Math.round(7 + state.impervious / 5);
    for (let i = 0; i < flowDots; i++) {
      const p = (progress * 2.1 + i / flowDots) % 1;
      const x = w * (.1 + p * .6);
      const y = h * (.43 + Math.pow(p, 1.25) * .27) - 3;
      ctx.fillStyle = '#68ccff'; ctx.beginPath(); ctx.arc(x, y, 2.2 + state.impervious / 100, 0, Math.PI * 2); ctx.fill();
    }
  }
}

function drawHydrograph() {
  const { width: w, height: h } = fitCanvas(hydrograph, hctx);
  const ctx = hctx;
  ctx.clearRect(0, 0, w, h);
  const pad = { l: 42, r: 14, t: 14, b: 30 };
  const pw = w - pad.l - pad.r, ph = h - pad.t - pad.b;
  const maxFlow = Math.max(state.capacity * 1.22, result.peak * 1.18, baseline.peak * 1.18, 1);

  ctx.strokeStyle = 'rgba(230,245,242,.09)'; ctx.lineWidth = 1;
  ctx.fillStyle = '#64777b'; ctx.font = '10px system-ui';
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + ph * i / 4;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(w - pad.r, y); ctx.stroke();
    ctx.fillText(`${(maxFlow * (1 - i / 4)).toFixed(0)}`, 5, y + 3);
  }
  for (let i = 0; i <= 4; i++) {
    const x = pad.l + pw * i / 4;
    ctx.fillText(`${(result.totalHours * i / 4).toFixed(1)}h`, x - 9, h - 8);
  }

  const xFor = t => pad.l + (t / result.totalHours) * pw;
  const yFor = q => pad.t + ph - (q / maxFlow) * ph;

  const capacityY = yFor(state.capacity);
  ctx.strokeStyle = '#ff6b62'; ctx.lineWidth = 1.5; ctx.setLineDash([6, 5]);
  ctx.beginPath(); ctx.moveTo(pad.l, capacityY); ctx.lineTo(w - pad.r, capacityY); ctx.stroke(); ctx.setLineDash([]);

  function line(points, color, dashed = false, width = 2) {
    ctx.beginPath();
    points.forEach((p, i) => { const x = xFor(p.hours), y = yFor(p.flow); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
    ctx.strokeStyle = color; ctx.lineWidth = width; if (dashed) ctx.setLineDash([6, 5]); ctx.stroke(); ctx.setLineDash([]);
  }
  line(baseline.points, '#697d80', true, 1.5);

  const fill = ctx.createLinearGradient(0, pad.t, 0, h - pad.b);
  fill.addColorStop(0, 'rgba(76,141,255,.34)'); fill.addColorStop(1, 'rgba(76,141,255,0)');
  ctx.beginPath();
  result.points.forEach((p, i) => { const x = xFor(p.hours), y = yFor(p.flow); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
  ctx.lineTo(xFor(result.points.at(-1).hours), h - pad.b); ctx.lineTo(pad.l, h - pad.b); ctx.closePath(); ctx.fillStyle = fill; ctx.fill();
  line(result.points, '#54b7ff', false, 2.5);

  ctx.fillStyle = '#64777b'; ctx.save(); ctx.translate(11, h / 2 + 22); ctx.rotate(-Math.PI / 2); ctx.fillText('FLOW (m³/s)', 0, 0); ctx.restore();
}

function resizeAndDraw() {
  drawLandscape(simProgress);
  drawHydrograph();
}

function runStorm() {
  if (animating) {
    animating = false; cancelAnimationFrame(rafId); $('stormButton').classList.remove('running'); $('stormButton').innerHTML = '<span>▶</span> Run the storm';
    return;
  }
  animating = true; animationStart = performance.now();
  $('stormButton').classList.add('running'); $('stormButton').innerHTML = '<span>Ⅱ</span> Pause storm';
  const durationMs = reduceMotion ? 800 : 7000;
  function frame(now) {
    simProgress = Math.min(1, (now - animationStart) / durationMs);
    const shownHours = simProgress * result.totalHours;
    const hours = Math.floor(shownHours), minutes = Math.floor((shownHours - hours) * 60);
    $('timeReadout').textContent = `${hours}:${String(minutes).padStart(2, '0')}`;
    drawLandscape(simProgress);
    if (simProgress < 1 && animating) rafId = requestAnimationFrame(frame);
    else {
      animating = false; $('stormButton').classList.remove('running'); $('stormButton').innerHTML = '<span>↻</span> Replay storm';
    }
  }
  rafId = requestAnimationFrame(frame);
}

Object.values(controls).forEach(input => input.addEventListener('input', updateStateFromControls));
document.querySelectorAll('.preset').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.preset').forEach(b => b.classList.toggle('active', b === button));
  state = { ...presets[button.dataset.preset] };
  simProgress = 0; $('timeReadout').textContent = '0:00'; recalculate();
}));
$('resetButton').addEventListener('click', () => {
  state = { ...presets.natural }; simProgress = 0; $('timeReadout').textContent = '0:00';
  document.querySelectorAll('.preset').forEach(b => b.classList.toggle('active', b.dataset.preset === 'natural'));
  recalculate();
});
$('stormButton').addEventListener('click', runStorm);
addEventListener('resize', resizeAndDraw);

recalculate();
