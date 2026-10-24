/* Winnebago County homepage card: a flat single-color map that tilts to an oblique view, then
   raises and sinks each municipality by four measures in turn (a prism map), and settles flat again.
   Plays on hover (mouse) or once when scrolled into view (touch). Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('wcard');
  if (!fig) return;
  const canvas = fig.querySelector('canvas');
  const label = fig.querySelector('.pc-label');
  const ctx = canvas.getContext('2d');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

  const LAYERS = [
    { name: 'Population change since 2020', h: (v) => sgn(v) * Math.min(1.25, Math.sqrt(Math.abs(v) / 0.06)) },
    { name: 'Projected change, 2020–2050', h: (v) => sgn(v) * Math.min(1.25, Math.sqrt(Math.abs(v) / 0.16)) },
    { name: 'Residents 65 and older', h: (v) => (v - 0.08) / 0.24 },
    { name: 'Median household income', h: (v) => (v - 40000) / 94000 },
  ];
  const STATIC = { name: 'Winnebago County · population change since 2020', c: (v) => Math.max(0, Math.min(1, v / 0.04)) ** 0.75 };
  function sgn(v) { return v < 0 ? -1 : 1; }

  let D = null, pieces = [], lakes = [], outline = [];
  let W = 0, H = 0, dpr = 1, scale = 1, off = [[0, 0], [0, 0]];
  const TILT = 56 * Math.PI / 180, ROT = 38 * Math.PI / 180, ZMAX = 5.2;   // km of height at h = 1

  // ---------- colors
  function hex(c) { c = c.trim(); if (c[0] === '#') { if (c.length === 4) c = '#' + c[1] + c[1] + c[2] + c[2] + c[3] + c[3]; return [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)); } const m = c.match(/\d+/g); return m ? m.slice(0, 3).map(Number) : [0, 0, 0]; }
  let P = {};
  function palette() {
    const cs = getComputedStyle(fig);
    const v = (n) => hex(cs.getPropertyValue(n));
    P = { gLo: v('--pc-green-lo'), gHi: v('--pc-green-hi'), rLo: v('--pc-red-lo'), rHi: v('--pc-red-hi'), lake: v('--pc-lake'), edge: v('--pc-edge'), ink: v('--ink') };
  }
  const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
  const rgb = (c, k = 1) => `rgb(${Math.round(c[0] * k)},${Math.round(c[1] * k)},${Math.round(c[2] * k)})`;

  // ---------- states: each is { tilt, h: [], c: [] } (c = signed color position: + green, - red)
  function stateStatic(tilt) { return { tilt, h: D.munis.map(() => 0), c: D.munis.map(m => STATIC.c(m.v[0])), red: D.munis.map(() => 0), lab: -1 }; }
  function stateLayer(i) {
    const L = LAYERS[i];
    const hs = D.munis.map(m => L.h(m.v[i]));
    const max = Math.max(...hs.map(Math.abs));
    return { tilt: 1, h: hs, c: hs.map(h => Math.min(1, Math.abs(h) / max) ** 0.8), red: hs.map(h => h < 0 ? 1 : 0), lab: i };
  }
  function lerpState(a, b, t) {
    return { tilt: a.tilt + (b.tilt - a.tilt) * t, h: a.h.map((x, i) => x + (b.h[i] - x) * t), c: a.c.map((x, i) => x + (b.c[i] - x) * t), red: a.red.map((x, i) => x + (b.red[i] - x) * t), lab: t < 0.5 ? a.lab : b.lab };
  }
  const ease = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  // ---------- projection
  function view(tilt) {
    const a = ROT * tilt, ti = TILT * tilt;
    const ca = Math.cos(a), sa = Math.sin(a), ct = Math.cos(ti), st = Math.sin(ti);
    const ox = off[0][0] + (off[1][0] - off[0][0]) * tilt, oy = off[0][1] + (off[1][1] - off[0][1]) * tilt;
    return { ca, sa, ct, st, ox, oy };
  }
  function proj(V, x, y, z) {
    const xr = x * V.ca - y * V.sa, yr = x * V.sa + y * V.ca;
    return [W / 2 + (xr - V.ox) * scale, H * 0.46 - (yr * V.ct + z * V.st - V.oy) * scale, yr];
  }

  function prepare() {
    pieces = [];
    D.munis.forEach((m, mi) => m.parts.forEach((rings) => pieces.push({ mi, rings })));
    lakes = D.lakes; outline = D.outline;
  }

  function fit() {
    const r = fig.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    // scale so both the flat and the tilted view fit
    let s = Infinity;
    for (const t of [0, 1]) {
      const a = ROT * t, ti = TILT * t;
      const V = { ca: Math.cos(a), sa: Math.sin(a), ct: Math.cos(ti), st: Math.sin(ti) };
      let minx = Infinity, maxx = -Infinity, miny = Infinity, maxy = -Infinity;
      outline.forEach(pt => pt[0].forEach(([x, y]) => { const xr = x * V.ca - y * V.sa, yr = x * V.sa + y * V.ca; minx = Math.min(minx, xr); maxx = Math.max(maxx, xr); miny = Math.min(miny, yr * V.ct); maxy = Math.max(maxy, yr * V.ct + (t ? ZMAX * 0.9 * V.st : 0)); }));
      if (t) { miny -= ZMAX * 0.35 * V.st; }
      off[t] = [(minx + maxx) / 2, (miny + maxy) / 2];
      const pad = t ? 0.9 : 0.8;
      s = Math.min(s, (W * pad) / (maxx - minx), (H * pad) / (maxy - miny));
    }
    scale = s;
  }

  function ringPath(V, ring, z) { ring.forEach(([x, y], i) => { const p = proj(V, x, y, z); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }); ctx.closePath(); }

  function colorFor(S, mi) {
    const t = S.c[mi], r = S.red[mi];
    const g = mix(P.gLo, P.gHi, t), rd = mix(P.rLo, P.rHi, t);
    return mix(g, rd, r);
  }

  function draw(S) {
    if (!D) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const V = view(S.tilt);
    const light = [-0.45, -0.75];   // light from the viewer's lower left (in rotated plane coords)
    ctx.lineJoin = 'round';

    // lakes on the plane
    ctx.fillStyle = rgb(P.lake);
    ctx.beginPath(); lakes.forEach(pt => pt.forEach(r => ringPath(V, r, 0))); ctx.fill('evenodd');

    // order: farthest nearest-point first
    const items = pieces.map(pc => {
      let near = Infinity;
      pc.rings[0].forEach(([x, y]) => { near = Math.min(near, x * V.sa + y * V.ca); });
      return { pc, near, z: S.h[pc.mi] * ZMAX };
    });
    items.sort((a, b) => b.near - a.near);

    const wallsOf = (pc, z, wantFront) => {
      const out = [];
      pc.rings.forEach(r => {
        for (let i = 0; i < r.length; i++) {
          const [x1, y1] = r[i], [x2, y2] = r[(i + 1) % r.length];
          const nx = (y2 - y1), ny = -(x2 - x1);       // outward normal (exterior CCW, holes CW)
          const nyr = nx * V.sa + ny * V.ca, nxr = nx * V.ca - ny * V.sa;
          const front = nyr < 0;
          if (front !== wantFront) continue;
          const len = Math.hypot(nxr, nyr) || 1;
          const sh = 0.62 + 0.3 * Math.max(0, (nxr * light[0] + nyr * light[1]) / len);
          out.push({ x1, y1, x2, y2, sh, d: ((y1 + y2) / 2) * V.ca + ((x1 + x2) / 2) * V.sa });
        }
      });
      return out.sort((a, b) => b.d - a.d);
    };
    const quad = (w, z0, z1) => { const a = proj(V, w.x1, w.y1, z0), b = proj(V, w.x2, w.y2, z0), c = proj(V, w.x2, w.y2, z1), d = proj(V, w.x1, w.y1, z1); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.lineTo(c[0], c[1]); ctx.lineTo(d[0], d[1]); ctx.closePath(); ctx.fill(); ctx.stroke(); };

    // 1. sunken municipalities: a pit cut into the invisible plane, clipped to the outline at z = 0
    items.filter(it => it.z < -0.01).forEach(it => {
      const col = colorFor(S, it.pc.mi);
      ctx.save();
      ctx.beginPath(); it.pc.rings.forEach(r => ringPath(V, r, 0)); ctx.clip('evenodd');
      ctx.lineWidth = 0.5;
      wallsOf(it.pc, it.z, false).forEach(w => { ctx.fillStyle = rgb(col, 0.68 + 0.18 * w.sh); ctx.strokeStyle = ctx.fillStyle; quad(w, it.z, 0); });
      ctx.fillStyle = rgb(col); ctx.beginPath(); it.pc.rings.forEach(r => ringPath(V, r, it.z)); ctx.fill('evenodd');
      ctx.restore();
      ctx.strokeStyle = rgb(P.edge); ctx.lineWidth = 0.7; ctx.beginPath(); it.pc.rings.forEach(r => ringPath(V, r, 0)); ctx.stroke();
    });

    // county outline on the plane
    ctx.strokeStyle = rgb(P.ink); ctx.globalAlpha = 0.55; ctx.lineWidth = 1;
    ctx.beginPath(); outline.forEach(pt => ringPath(V, pt[0], 0)); ctx.stroke(); ctx.globalAlpha = 1;

    // 2. flat and raised municipalities
    items.filter(it => it.z >= -0.01).forEach(it => {
      const col = colorFor(S, it.pc.mi), z = Math.max(0, it.z);
      if (z > 0.02) {
        ctx.lineWidth = 0.5;
        wallsOf(it.pc, z, true).forEach(w => { ctx.fillStyle = rgb(col, w.sh); ctx.strokeStyle = ctx.fillStyle; quad(w, 0, z); });
      }
      ctx.fillStyle = rgb(col);
      ctx.beginPath(); it.pc.rings.forEach(r => ringPath(V, r, z)); ctx.fill('evenodd');
      ctx.strokeStyle = rgb(P.edge); ctx.lineWidth = 0.7; ctx.stroke();
    });

  }

  // ---------- timeline
  let keys = null, anim = null, cur = null;
  function buildKeys() {
    const S0 = stateStatic(0), S1 = stateStatic(1);
    const L = LAYERS.map((_, i) => stateLayer(i));
    keys = [[0, S0], [800, S1], [1650, L[0]], [3050, L[0]], [3900, L[1]], [5300, L[1]], [6150, L[2]], [7550, L[2]], [8400, L[3]], [9800, L[3]], [10650, S1], [11450, S0]];
  }
  function stateAt(t) {
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i][0]) { const [t0, a] = keys[i - 1], [t1, b] = keys[i]; return lerpState(a, b, ease((t - t0) / (t1 - t0))); }
    }
    return keys[keys.length - 1][1];
  }
  function setLabel(i) {
    const txt = i < 0 ? STATIC.name : LAYERS[i].name + (i < 2 ? ' · decline sinks' : '');
    if (label.dataset.i === String(i)) return;
    label.dataset.i = String(i);
    label.style.opacity = 0;
    setTimeout(() => { label.textContent = txt; label.style.opacity = 1; }, 180);
  }
  function frame(now) {
    if (!anim) return;
    const t = now - anim.start;
    let S;
    if (anim.mode === 'play') {
      S = stateAt(t);
      if (t >= keys[keys.length - 1][0]) { anim = null; }
    } else {
      const k = Math.min(1, t / 750); S = lerpState(anim.from, keys[0][1], ease(k));
      if (k >= 1) anim = null;
    }
    cur = S; draw(S); setLabel(S.lab);
    if (anim) requestAnimationFrame(frame);
  }
  function play() { if (!D || (anim && anim.mode === 'play')) return; anim = { mode: 'play', start: performance.now() }; requestAnimationFrame(frame); }
  function settle() { if (!anim || anim.mode !== 'play') return; anim = { mode: 'settle', start: performance.now(), from: cur }; requestAnimationFrame(frame); }

  function redraw() { if (!D) return; fit(); draw(cur || keys[0][1]); }

  function load() {
    fetch('media/winnebago-card/card.json').then(r => r.json()).then(d => {
      D = d; prepare(); palette(); buildKeys(); fit(); cur = keys[0][1]; draw(cur);
      fig.classList.add('ready'); label.textContent = STATIC.name; label.dataset.i = '-1';
      if (reduceMotion) return;
      if (finePointer) { fig.addEventListener('mouseenter', play); fig.addEventListener('mouseleave', settle); }
      else if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { setTimeout(play, 300); io.disconnect(); } }), { threshold: 0.7 });
        io.observe(fig);
      }
    }).catch(() => {});
  }
  if ('IntersectionObserver' in window) {
    const lio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { load(); lio.disconnect(); } }), { rootMargin: '400px' });
    lio.observe(fig);
  } else load();

  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(redraw, 120); });
  const scheme = () => { palette(); redraw(); };
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', scheme);
  new MutationObserver(scheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  window.__wcard = { play, stateAt: (t) => { const S = stateAt(t); draw(S); setLabel(S.lab); return S; } };   // for testing
})();
