/* Parcel QA homepage card, in three beats:
   1. Draft: pull back from the block and draw Sheboygan County from its boundary calls, leg by leg
      (west line, north line, the Lake Michigan shore, south line back to the point of beginning),
      then the town lines and names.
   2. Place: mark one block and zoom down into it, 70 km to 550 m.
   3. Check: a scan line sweeps the block and the real QA findings light up, with a running count.
   Plays on hover (mouse) or once when scrolled into view (touch). Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('pqcard');
  if (!fig) return;
  const svg = fig.querySelector('svg');
  const scan = svg.querySelector('.scan');
  const cty = svg.querySelector('.cty');
  const legs = Array.from(cty.querySelectorAll('.leg'));
  const munis = cty.querySelector('.munis');
  const finds = Array.from(svg.querySelectorAll('.f')).map(el => ({ el, x: +el.dataset.x, n: +(el.dataset.n || 0) }));
  const label = fig.querySelector('.pq-label');
  const cap = fig.querySelector('.pq-cap');
  const rest = label.textContent;
  const done = label.dataset.done;
  const FULL = [0, 0, 1000, 600];
  const COUNTY = cty.dataset.county.split(' ').map(Number);
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduceMotion) return;

  let run = 0;
  const ease = k => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);
  const setVB = a => svg.setAttribute('viewBox', a.map(v => v.toFixed(2)).join(' '));
  // Zoom between two views at a steady rate: width moves on a log scale, and the centre moves
  // in step with the width so the block stays under the eye the whole way down.
  function zoom(a, b, k) {
    const w = a[2] * Math.pow(b[2] / a[2], k);
    const f = (w - a[2]) / (b[2] - a[2]);
    const cx = a[0] + a[2] / 2 + (b[0] + b[2] / 2 - a[0] - a[2] / 2) * f;
    const cy = a[1] + a[3] / 2 + (b[1] + b[3] / 2 - a[1] - a[3] / 2) * f;
    const h = w * a[3] / a[2];
    return [cx - w / 2, cy - h / 2, w, h];
  }
  function tween(ms, fn, tok) {
    return new Promise(res => {
      let t0 = 0;
      const step = t => {
        if (tok !== run) return res(false);
        if (!t0) t0 = t;
        const k = Math.min(1, (t - t0) / ms);
        fn(k);
        k < 1 ? requestAnimationFrame(step) : res(true);
      };
      requestAnimationFrame(step);
    });
  }
  const wait = (ms, tok) => new Promise(res => setTimeout(() => res(tok === run), ms));
  function swapLabel(text) {
    label.style.opacity = 0;
    setTimeout(() => { label.textContent = text; label.style.opacity = ''; }, 160);
  }

  function reset() {
    fig.classList.remove('drafting', 'placed', 'scanning', 'swept');
    cty.classList.remove('closed', 'towns', 'marked');
    legs.forEach(l => { l.style.strokeDashoffset = 1; });
    munis.style.strokeDashoffset = 1;
    finds.forEach(f => f.el.classList.remove('on'));
    scan.removeAttribute('transform');
    setVB(FULL);
    cap.textContent = '';
    label.textContent = rest; label.style.opacity = '';
  }

  async function play() {
    const tok = ++run;
    reset();
    fig.classList.add('drafting');
    cap.textContent = 'Sheboygan County, from its boundary description';
    if (!await tween(1500, k => setVB(zoom(FULL, COUNTY, ease(k))), tok)) return;

    cap.textContent = 'Beginning at the southwest corner of the county (POB)';
    if (!await wait(700, tok)) return;
    for (const l of legs) {                          // 1. draft, leg by leg
      cap.textContent = l.dataset.call;
      const ms = l.dataset.call.includes('shore') ? 1500 : 950;
      if (!await tween(ms, k => { l.style.strokeDashoffset = 1 - ease(k); }, tok)) return;
      if (!await wait(250, tok)) return;
    }
    cty.classList.add('closed');
    cap.textContent = 'Closed. Then the 15 towns inside it';
    cty.classList.add('towns');
    if (!await tween(1100, k => { munis.style.strokeDashoffset = 1 - ease(k); }, tok)) return;
    if (!await wait(900, tok)) return;

    cty.classList.add('marked');                     // 2. find one block and zoom down to it
    cap.textContent = 'One block in the City of Sheboygan Falls, 550 m across';
    if (!await wait(1000, tok)) return;
    fig.classList.add('placed');
    if (!await tween(1700, k => setVB(zoom(COUNTY, FULL, ease(k))), tok)) return;
    fig.classList.remove('drafting');

    fig.classList.add('scanning', 'swept');          // 3. check the block
    let found = 0;
    swapLabel('Running 19 checks · 0 found');
    if (!await tween(3600, k => {
      const x = -40 + ease(k) * 1080;
      scan.setAttribute('transform', `translate(${x.toFixed(1)},0)`);
      for (const f of finds) if (x >= f.x && !f.el.classList.contains('on')) {
        f.el.classList.add('on'); found += f.n;
        label.textContent = `Running 19 checks · ${found} found`;
      }
    }, tok)) return;
    fig.classList.remove('scanning');
    swapLabel(done);
  }
  function settle() { run++; reset(); }

  if (finePointer) { fig.addEventListener('mouseenter', play); fig.addEventListener('mouseleave', settle); }
  else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { setTimeout(play, 300); io.disconnect(); } }), { threshold: 0.7 });
    io.observe(fig);
  }
})();
