/* MKE Airport homepage card: the radar sweep is CSS only. It turns on hover with a mouse;
   on touch screens it runs while the card is in view. Static with reduced motion. */
(function () {
  'use strict';
  const fig = document.getElementById('rcard');
  if (!fig || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (matchMedia('(hover: hover) and (pointer: fine)').matches || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(es => es.forEach(e => fig.classList.toggle('run', e.isIntersecting)), { threshold: 0.5 }).observe(fig);
})();
