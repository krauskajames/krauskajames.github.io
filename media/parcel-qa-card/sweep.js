/* Parcel QA homepage card, in three beats:
   1. Draft: zoom in and draw one parcel from its legal description, course by course (COGO traverse),
      with the call read out in a caption bar, then close on the point of beginning.
   2. Place: zoom back out so the drafted parcel sits among the county's real parcels.
   3. Check: a scan line sweeps the block and the real QA findings light up, with a running count.
   Plays on hover (mouse) or once when scrolled into view (touch). Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('pqcard');
  if (!fig) return;
  const svg = fig.querySelector('svg');
  const scan = svg.querySelector('.scan');
  const trav = svg.querySelector('.trav');
  const courses = Array.from(trav.querySelectorAll('.tc')).map(g => {
    const path = g.querySelector('path');
    const m = path.getAttribute('d').match(/M([\d.-]+),([\d.-]+)L([\d.-]+),([\d.-]+)/).slice(1).map(Number);
    return { g, path, dd: g.querySelector('.dd'), dist: +g.dataset.dist, call: g.dataset.call, x: m[0], y: m[1] };
  });
  const narrow = trav.querySelector('.narrow');
  const finds = Array.from(svg.querySelectorAll('.f')).map(el => ({ el, x: +el.dataset.x, n: +(el.dataset.n || 0) }));
  const label = fig.querySelector('.pq-label');
  const cap = fig.querySelector('.pq-cap');
  const rest = label.textContent;
  const done = label.dataset.done;
  const FULL = [0, 0, 1000, 600];
  const ZOOM = trav.dataset.zoom.split(' ').map(Number);
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduceMotion) return;

  let run = 0;
  const ease = k => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);
  const setVB = a => svg.setAttribute('viewBox', a.map(v => v.toFixed(2)).join(' '));
  const lerp = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
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
    trav.classList.remove('closed');
    courses.forEach(c => { c.g.classList.remove('on', 'done'); c.path.style.strokeDashoffset = 1; c.dd.textContent = c.dist.toFixed(2); });
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
    cap.textContent = 'Beginning at the point of beginning (POB)';
    if (!await tween(1000, k => setVB(lerp(FULL, ZOOM, ease(k))), tok)) return;

    for (const c of courses) {                       // 1. draft, course by course
      cap.textContent = c.call;
      narrow.setAttribute('transform', `translate(${c.x},${c.y})`);
      c.g.classList.add('on');
      if (!await tween(800, k => {
        const e = ease(k);
        c.path.style.strokeDashoffset = 1 - e;
        c.dd.textContent = (c.dist * e).toFixed(2);
      }, tok)) return;
      c.g.classList.add('done');
      if (!await wait(200, tok)) return;
    }
    cap.textContent = trav.dataset.close;
    trav.classList.add('closed');
    if (!await wait(1400, tok)) return;

    fig.classList.remove('drafting');                // 2. place it among the county's parcels
    fig.classList.add('placed');
    if (!await tween(1000, k => setVB(lerp(ZOOM, FULL, ease(k))), tok)) return;

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
