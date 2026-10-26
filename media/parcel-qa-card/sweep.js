/* Parcel QA homepage card: a scan line sweeps one real Sheboygan block and the QA findings there
   light up as it passes (nested CSM lot, slivers, an address linked to the wrong road segment, and a
   street name spelled two ways). Plays on hover (mouse) or once when scrolled into view (touch).
   Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('pqcard');
  if (!fig) return;
  const svg = fig.querySelector('svg');
  const scan = svg.querySelector('.scan');
  const finds = Array.from(svg.querySelectorAll('.f')).map(el => ({ el, x: +el.dataset.x }));
  const label = fig.querySelector('.pq-label');
  const rest = label.textContent;
  const done = label.dataset.done;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduceMotion) return;

  const SWEEP = 3600, W = 1000;
  let raf = 0, t0 = 0, playing = false;

  function swapLabel(text) {
    label.style.opacity = 0;
    setTimeout(() => { label.textContent = text; label.style.opacity = ''; }, 180);
  }
  function frame(t) {
    if (!t0) t0 = t;
    const k = Math.min(1, (t - t0) / SWEEP);
    const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    const x = -40 + e * (W + 80);
    scan.setAttribute('transform', `translate(${x.toFixed(1)},0)`);
    for (const f of finds) if (x >= f.x && !f.el.classList.contains('on')) f.el.classList.add('on');
    if (k < 1) raf = requestAnimationFrame(frame);
    else { fig.classList.remove('scanning'); swapLabel(done); }
  }
  function play() {
    if (playing) return;
    playing = true; t0 = 0;
    fig.classList.add('scanning', 'swept');
    swapLabel('Running 19 checks…');
    raf = requestAnimationFrame(frame);
  }
  function settle() {
    cancelAnimationFrame(raf);
    playing = false;
    fig.classList.remove('scanning', 'swept');
    finds.forEach(f => f.el.classList.remove('on'));
    swapLabel(rest);
  }
  if (finePointer) { fig.addEventListener('mouseenter', play); fig.addEventListener('mouseleave', settle); }
  else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { setTimeout(play, 300); io.disconnect(); } }), { threshold: 0.7 });
    io.observe(fig);
  }
})();
