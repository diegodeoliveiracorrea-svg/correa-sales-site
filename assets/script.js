/* Correa Sales — global interactions */

// Mobile drawer
(function () {
  const toggle = document.querySelector('.menu-toggle');
  const drawer = document.querySelector('.mobile-drawer');
  const close = document.querySelector('.drawer-close');
  if (!toggle || !drawer) return;
  const open = () => { drawer.classList.add('open'); document.body.style.overflow = 'hidden'; };
  const shut = () => { drawer.classList.remove('open'); document.body.style.overflow = ''; };
  toggle.addEventListener('click', open);
  close && close.addEventListener('click', shut);
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', shut));
})();

// FAQ accordion
(function () {
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    const a = item.querySelector('.faq-a');
    if (!q || !a) return;
    q.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      // close siblings
      item.parentElement.querySelectorAll('.faq-item.open').forEach(i => {
        if (i !== item) {
          i.classList.remove('open');
          i.querySelector('.faq-a').style.maxHeight = '0';
        }
      });
      if (isOpen) {
        item.classList.remove('open');
        a.style.maxHeight = '0';
      } else {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });
})();

// Reveal on scroll — safe by default.
// The CSS only hides `.reveal` when <html> has the `js-reveal` class,
// which we only add if we can guarantee we'll reveal things back.
(function () {
  const init = () => {
    const els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    const revealAll = () => els.forEach(el => el.classList.add('in'));

    // Reduced motion → skip animation entirely, leave content visible.
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return; // never add js-reveal → content stays visible per CSS default
    }

    // If IO is unavailable, don't gate anything — leave content visible.
    if (!('IntersectionObserver' in window)) return;

    // Activate the animation system: now CSS will hide .reveal until .in
    document.documentElement.classList.add('js-reveal');

    // Reveal above-the-fold immediately so first paint isn't empty
    // if IO's initial callback is unreliable in this environment.
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const toReveal = [];
    els.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.95) toReveal.push(el);
    });
    // Force layout then flip on next frame so the transition still plays.
    requestAnimationFrame(() => {
      requestAnimationFrame(() => toReveal.forEach(el => el.classList.add('in')));
    });

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -8% 0px' });
    els.forEach(el => io.observe(el));

    // Final safety net — if for any reason IO doesn't fire, reveal all
    // remaining elements after 2s so no visitor ever sees blank content.
    setTimeout(revealAll, 2000);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// Contact form (simulated submission)
(function () {
  const form = document.querySelector('#contact-form');
  if (!form) return;
  const status = form.querySelector('.form-status');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Enviando...';
    setTimeout(() => {
      form.reset();
      btn.disabled = false;
      btn.textContent = 'Enviar mensagem';
      if (status) {
        status.textContent = '✓ Recebemos sua mensagem. Nossa equipe entrará em contato em até 1 dia útil.';
        status.classList.add('show');
        setTimeout(() => status.classList.remove('show'), 6000);
      }
    }, 900);
  });

  // Pre-fill service from ?servico= query param
  const params = new URLSearchParams(window.location.search);
  const service = params.get('servico');
  const select = form.querySelector('select[name="servico"]');
  if (service && select) {
    for (const opt of select.options) {
      if (opt.value === service) { select.value = service; break; }
    }
  }
})();

// Newsletter form (simulated)
(function () {
  document.querySelectorAll('.newsletter form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input');
      const btn = form.querySelector('button');
      const original = btn.textContent;
      btn.textContent = '✓ Inscrito';
      input.value = '';
      setTimeout(() => { btn.textContent = original; }, 2400);
    });
  });
})();
