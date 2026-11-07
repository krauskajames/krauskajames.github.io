/* Parcel QA homepage card, in four beats (the same story as the project page):
   1. Start: the point of commencement, a PLSS sixteenth corner in the Village of Cascade.
   2. Draft: James's Parcel 3 drawn from its recorded description, course by course (COGO traverse), with the
      call read out in a caption bar and a magnifier on the 6.55 ft jog; it closes on the point of beginning.
   3. Compare: the county's tax parcel is laid over the draft, with the corner offsets measured in ArcGIS Pro.
   4. Check: zoom out to the block; a scan line sweeps it and the real QA findings light up, with a running count.
   Plays on hover (mouse) or once when scrolled into view (touch). Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('pqcard');
  if (!fig) return;
  const svg = fig.querySelector('svg');
  const scan = svg.querySelector('.scan');
  const trav = svg.querySelector('.trav');
  const loupePaths = Array.from(trav.querySelectorAll('.lp'));
  const courses = Array.from(trav.querySelectorAll('.tc')).map(g => {
    const path = g.querySelector('path');
    const m = path.getAttribute('d').match(/M([\d.-]+),([\d.-]+)L([\d.-]+),([\d.-]+)/).slice(1).map(Number);
    return { g, path, i: +g.dataset.i, dd: g.querySelector('.dd'), dist: +g.dataset.dist, call: g.dataset.call,
             loupe: g.dataset.loupe === '1', lp: loupePaths.filter(p => +p.dataset.i === +g.dataset.i), x: m[0], y: m[1] };
  });
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
  let playing = false, finished = false, back = 0;
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
    fig.classList.remove('drafting', 'jog', 'compared', 'placed', 'scanning', 'swept');
    trav.classList.remove('closed');
    courses.forEach(c => { c.g.classList.remove('on', 'done'); c.path.style.strokeDashoffset = 1; if (c.dd) c.dd.textContent = c.dist.toFixed(2); });
    loupePaths.forEach(p => { p.style.strokeDashoffset = 1; });
    finds.forEach(f => f.el.classList.remove('on'));
    scan.removeAttribute('transform');
    setVB(FULL);
    cap.textContent = '';
    label.textContent = rest; label.style.opacity = '';
  }

  async function play() {
    clearTimeout(back);
    if (playing || finished) return;                 // a stray mouse exit/re-entry never restarts or snaps the card
    playing = true;
    const tok = ++run;
    reset();
    label.style.opacity = 0;
    fig.classList.add('drafting');                   // 1. start at the corner
    cap.textContent = 'Commencing at the NE corner of the SW¼ SE¼, Section 20, T14N R21E';
    if (!await tween(1100, k => setVB(lerp(FULL, ZOOM, ease(k))), tok)) return;
    if (!await wait(500, tok)) return;

    for (const c of courses) {                       // 2. draft, course by course
      cap.textContent = c.call;
      c.g.classList.add('on');
      if (c.loupe) { fig.classList.add('jog'); if (!await wait(500, tok)) return; }
      if (!await tween(c.loupe ? 1500 : 850, k => {
        const e = ease(k);
        c.path.style.strokeDashoffset = 1 - e;
        c.lp.forEach(p => { p.style.strokeDashoffset = 1 - e; });
        if (c.dd) c.dd.textContent = (c.dist * e).toFixed(2);
      }, tok)) return;
      c.g.classList.add('done');
      if (!await wait(c.loupe ? 700 : 200, tok)) return;
      if (c.i === 3) fig.classList.remove('jog');
    }
    cap.textContent = trav.dataset.close;
    trav.classList.add('closed');
    if (!await wait(1500, tok)) return;

    fig.classList.add('compared');                   // 3. lay the county's parcel over the draft
    cap.textContent = trav.dataset.compare;
    if (!await wait(2600, tok)) return;

    fig.classList.remove('drafting', 'compared');    // 4. zoom out and check the block
    fig.classList.add('placed');
    if (!await tween(1100, k => setVB(lerp(ZOOM, FULL, ease(k))), tok)) return;
    fig.classList.add('scanning', 'swept');
    let found = 0;
    swapLabel('Running 19 checks · 0 found');
    if (!await tween(3400, k => {
      const x = -40 + ease(k) * 1080;
      scan.setAttribute('transform', `translate(${x.toFixed(1)},0)`);
      for (const f of finds) if (x >= f.x && !f.el.classList.contains('on')) {
        f.el.classList.add('on'); found += f.n;
        label.textContent = `Running 19 checks · ${found} found`;
      }
    }, tok)) return;
    fig.classList.remove('scanning');
    swapLabel(done);
    playing = false; finished = true;
    if (!fig.matches(':hover')) settle(2500);
  }
  // Once started, the story plays to the end even if the pointer leaves; the card returns to rest
  // a moment after the pointer is gone, fading out rather than snapping.
  function settle(delay = 1200) {
    clearTimeout(back);
    if (playing) return;
    back = setTimeout(() => {
      fig.classList.add('resting');
      setTimeout(() => { run++; reset(); finished = false; fig.classList.remove('resting'); }, 350);
    }, typeof delay === 'number' ? delay : 1200);
  }

  if (finePointer) {
    fig.addEventListener('mouseenter', play);
    fig.addEventListener('mouseleave', settle);
  }
  else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { setTimeout(play, 300); io.disconnect(); } }), { threshold: 0.7 });
    io.observe(fig);
  }
})();
