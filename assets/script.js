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

// Contact form — envia a mensagem pelo WhatsApp do escritório
// (sem servidor: a mensagem chega de verdade, na conversa do cliente com o escritório)
(function () {
  const form = document.querySelector('#contact-form');
  if (!form) return;
  const status = form.querySelector('.form-status');
  const WA = '5521984660882';

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const v = (n) => (form.querySelector(`[name="${n}"]`)?.value || '').trim();
    const nome = v('nome'), email = v('email'), tel = v('telefone'), msg = v('mensagem');
    const tipo = v('tipo'), func = v('funcionarios'), preoc = v('preocupacao'), urg = v('urgencia');
    const select = form.querySelector('select[name="servico"]');
    const servico = select && select.value ? select.options[select.selectedIndex].text : '';
    const emailOk = !email || /^\S+@\S+\.\S+$/.test(email);

    if (!nome || tel.replace(/\D/g, '').length < 10 || !preoc || !emailOk) {
      status.textContent = !emailOk ? 'Confira o e-mail digitado ou deixe o campo em branco.' : 'Preencha nome, WhatsApp com DDD e o que mais preocupa hoje para continuar.';
      status.style.borderLeftColor = '#a2402f';
      status.style.color = '#a2402f';
      status.classList.add('show');
      return;
    }

    status.style.borderLeftColor = '';
    status.style.color = '';

    const texto = [
      'DIAGNÓSTICO',
      `Nome: ${nome}`,
      v('empresa') ? `Empresa: ${v('empresa')}` : null,
      `Preocupação: ${preoc}`,
      tipo ? `Tipo: ${tipo}` : null,
      func ? `Funcionários: ${func}` : null,
      urg ? `Urgência: ${urg}` : null,
      servico ? `Serviço: ${servico}` : null,
      email ? `E-mail: ${email}` : null,
      `WhatsApp: ${tel}`,
      msg ? '' : null,
      msg || null
    ].filter(l => l !== null).join('\n');

    const waUrl = `https://wa.me/${WA}?text=${encodeURIComponent(texto)}`;
    if (window.csConta) window.csConta('formulario', 'diagnóstico');

    // Abre direto na mesma aba (links wa.me funcionam bem assim e não caem em
    // bloqueio de pop-up). Se o navegador insistir, o aviso abaixo traz o número.
    const win = window.open(waUrl, '_blank', 'noopener');
    if (!win) window.location.href = waUrl;

    status.innerHTML = 'Abrimos o WhatsApp com sua mensagem pronta — é só tocar em enviar. Se não abrir, <a href="' + waUrl + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline">clique aqui</a> ou chame no (21) 98466-0882.';
    status.classList.add('show');
  });

  // Pre-fill service from ?servico= query param
  const params = new URLSearchParams(window.location.search);
  const service = params.get('servico');
  const select = form.querySelector('select[name="servico"]');
  if (service && select) {
    for (const opt of select.options) {
      if (opt.value === service) { select.value = service; const d = select.closest('details'); if (d) d.open = true; break; }
    }
  }
})();


// Medição anônima de contatos: conta cliques no WhatsApp e envios do formulário de diagnóstico.
// Não guarda nome, telefone, e-mail nem IP: só página, tipo de clique, texto do botão e origem da visita.
(function () {
  const API = 'https://zjktgygkiktjlgjuyglt.supabase.co/functions/v1/clique';
  let origem = '';
  try {
    const q = new URLSearchParams(location.search);
    const utm = q.get('utm_source');
    const ref = document.referrer ? new URL(document.referrer).hostname.replace(/^www\./, '') : '';
    origem = utm || (ref && ref !== location.hostname.replace(/^www\./, '') ? ref : '');
    if (origem) sessionStorage.setItem('cs_origem', origem); else origem = sessionStorage.getItem('cs_origem') || 'direto';
  } catch (e) { origem = origem || 'direto'; }
  window.csConta = function (alvo, rotulo) {
    try {
      const body = JSON.stringify({ alvo: alvo, pagina: location.pathname, rotulo: String(rotulo || '').trim().slice(0, 80), origem: origem });
      if (navigator.sendBeacon) navigator.sendBeacon(API, new Blob([body], { type: 'text/plain' }));
      else fetch(API, { method: 'POST', body: body, keepalive: true, mode: 'no-cors' });
    } catch (e) { /* medição nunca atrapalha o clique */ }
  };
  document.addEventListener('click', function (e) {
    const a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (a) window.csConta('whatsapp', a.getAttribute('aria-label') || a.textContent);
  }, true);
})();

// Anúncios (Google Ads e Meta): DESLIGADO enquanto os códigos abaixo estiverem vazios.
// Quando as contas existirem, preencha os códigos e atualize a política de privacidade.
// Cada clique no WhatsApp e cada formulário enviado passa a contar como conversão do anúncio.
(function () {
  const ADS = {
    googleAds: '',          // ex.: 'AW-123456789'
    googleConversao: '',    // ex.: 'AW-123456789/AbCdEfGhIjK'
    metaPixel: ''           // ex.: '123456789012345'
  };
  if (!ADS.googleAds && !ADS.metaPixel) return;
  if (ADS.googleAds) {
    const g = document.createElement('script');
    g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + ADS.googleAds;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date()); window.gtag('config', ADS.googleAds);
  }
  if (ADS.metaPixel) {
    (function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = true; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = true; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', ADS.metaPixel); window.fbq('track', 'PageView');
  }
  const conta = window.csConta;
  window.csConta = function (alvo, rotulo) {
    try {
      if (window.gtag && ADS.googleConversao) window.gtag('event', 'conversion', { send_to: ADS.googleConversao });
      if (window.fbq) window.fbq('track', alvo === 'formulario' ? 'Lead' : 'Contact');
    } catch (e) { /* medição nunca atrapalha o clique */ }
    if (conta) conta(alvo, rotulo);
  };
})();

// Faixa do Boletim Corrêa Sales (topo de todas as páginas).
// A CADA EDIÇÃO: atualize só este bloco (número, título, endereço e data da última atualização).
(function () {
  const BOLETIM = {
    edicao: 1,
    titulo: 'O que mudou para a sua empresa na semana de 16 a 20/11',
    curto: 'O que mudou para a sua empresa esta semana',
    url: 'boletim-semanal-16-a-20-novembro-2026.html',
    atualizado: '17/11/2026'
  };
  try {
    const path = location.pathname;
    const ehBoletim = /\/boletim-semanal-[^/]+\.html$/.test(path);
    const ehAtual = path.endsWith('/' + BOLETIM.url);
    // Edição antiga: aviso no topo do texto apontando para a mais recente.
    if (ehBoletim && !ehAtual) {
      const art = document.querySelector('article.art');
      const meta = art && art.querySelector('.meta');
      const dt = meta ? (meta.textContent.match(/Edição de (\d{2}\/\d{2}\/\d{4})/) || [])[1] : '';
      if (art) {
        const av = document.createElement('div');
        av.setAttribute('role', 'note');
        av.style.cssText = 'border-left:3px solid var(--gold,#B08A57);background:var(--off,#F6F2EB);padding:14px 18px;border-radius:0 8px 8px 0;margin:0 0 24px;font-size:.95rem;line-height:1.5';
        av.innerHTML = '<strong style="color:var(--navy,#102742)">Esta edição é ' + (dt ? 'de ' + dt : 'antiga') + '.</strong> Algumas informações podem ter mudado. ' +
          '<a href="' + BOLETIM.url + '" style="color:var(--gold-3,#8a6a3f);font-weight:600">Veja o boletim mais recente (nº ' + BOLETIM.edicao + ', atualizado em ' + BOLETIM.atualizado + ') →</a>';
        art.insertBefore(av, art.firstChild);
      }
    }
    if (ehAtual) return;
    const chave = 'cs-faixa-boletim-' + BOLETIM.edicao;
    try { if (localStorage.getItem(chave) === 'fechada') return; } catch (e) {}
    const st = document.createElement('style');
    st.textContent =
      '.faixa-boletim{background:var(--navy,#102742);color:#fff;font-size:.86rem;line-height:1.4}' +
      '.faixa-boletim .fb-in{max-width:1200px;margin:0 auto;padding:9px 48px 9px 24px;display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;position:relative}' +
      '.faixa-boletim .fb-tag{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold,#B08A57);font-weight:600;white-space:nowrap}' +
      '.faixa-boletim a.fb-link{color:#fff;text-decoration:none;font-weight:500}' +
      '.faixa-boletim a.fb-link:hover .fb-tit{text-decoration:underline}' +
      '.faixa-boletim .fb-cta{color:var(--gold,#B08A57);font-weight:600;margin-left:6px;white-space:nowrap}' +
      '.faixa-boletim .fb-data{color:rgba(255,255,255,.62);font-size:.78rem;white-space:nowrap}' +
      '.faixa-boletim .fb-x{position:absolute;right:14px;top:50%;transform:translateY(-50%);background:none;border:0;color:rgba(255,255,255,.6);font-size:1.15rem;cursor:pointer;padding:4px 8px;line-height:1}' +
      '.faixa-boletim .fb-x:hover{color:#fff}' +
      '.faixa-boletim .fb-curto{display:none}' +
      '@media (max-width:640px){.faixa-boletim .fb-in{gap:4px 10px;padding:8px 40px 8px 16px;justify-content:flex-start}.faixa-boletim .fb-tit{display:none}.faixa-boletim .fb-curto{display:inline}.faixa-boletim .fb-data{width:100%}}';
    document.head.appendChild(st);
    const f = document.createElement('div');
    f.className = 'faixa-boletim';
    f.setAttribute('role', 'region');
    f.setAttribute('aria-label', 'Boletim da semana');
    f.innerHTML =
      '<div class="fb-in">' +
      '<span class="fb-tag">Boletim nº ' + BOLETIM.edicao + '</span>' +
      '<a class="fb-link" href="' + BOLETIM.url + '"><span class="fb-tit">' + BOLETIM.titulo + '</span>' +
      '<span class="fb-curto">' + BOLETIM.curto + '</span><span class="fb-cta">Ler →</span></a>' +
      '<span class="fb-data">Atualizado em ' + BOLETIM.atualizado + '</span>' +
      '<button class="fb-x" type="button" aria-label="Fechar aviso do boletim">×</button>' +
      '</div>';
    f.querySelector('.fb-x').addEventListener('click', function () {
      f.remove();
      try { localStorage.setItem(chave, 'fechada'); } catch (e) {}
    });
    document.body.insertBefore(f, document.body.firstChild);
  } catch (e) { /* a faixa nunca atrapalha a página */ }
})();
