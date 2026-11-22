/*
  Cookie consent + deferred Google Analytics 4.
  GA4 (G-3SXHN4B877) is loaded ONLY after the visitor accepts.
  Choice is stored in localStorage under "hs-cookie-choice" (accepted | declined).
  A "Cookie settings" link is added to the footer on every page.
*/
(function () {
  var KEY = 'hs-cookie-choice';
  var GA_ID = 'G-3SXHN4B877';
  var loaded = false;

  function choice() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  function loadGA() {
    if (loaded || window.__hsGaLoaded) return;
    loaded = true;
    window.__hsGaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  }

  /* ---------- banner ---------- */
  function buildBanner() {
    if (document.getElementById('hsCookieBar')) return;
    var bar = document.createElement('div');
    bar.id = 'hsCookieBar';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'Cookie notice');
    bar.style.cssText =
      'position:fixed;left:0;right:0;bottom:0;z-index:9999;padding:14px 16px;' +
      'background:#0a0e1a;border-top:1px solid rgba(56,200,200,.35);' +
      'box-shadow:0 -6px 24px rgba(0,0,0,.35);font-family:Arial,Helvetica,sans-serif;';
    bar.innerHTML =
      '<div style="max-width:1100px;margin:0 auto;display:flex;gap:14px;flex-wrap:wrap;align-items:center;">' +
        '<div style="flex:1 1 340px;min-width:240px;color:#dfe9f3;font-size:13px;line-height:1.55;">' +
          'This site uses Google Analytics cookies to see which pages are useful. ' +
          'They are only set if you accept. ' +
          '<a href="/privacy.html" style="color:#38c8c8;text-decoration:underline;">Read the privacy notice</a>' +
        '</div>' +
        '<div style="display:flex;gap:10px;flex:0 0 auto;">' +
          '<button type="button" id="hsCookieDecline" style="padding:10px 18px;border-radius:8px;' +
            'border:1px solid rgba(223,233,243,.45);background:transparent;color:#dfe9f3;font-size:13.5px;' +
            'font-weight:600;cursor:pointer;">Decline</button>' +
          '<button type="button" id="hsCookieAccept" style="padding:10px 18px;border-radius:8px;border:none;' +
            'background:linear-gradient(135deg,#e8c558,#d4a73a);color:#0a0e1a;font-size:13.5px;' +
            'font-weight:800;cursor:pointer;">Accept</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(bar);

    document.getElementById('hsCookieAccept').addEventListener('click', function () {
      store('accepted'); loadGA(); hide();
    });
    document.getElementById('hsCookieDecline').addEventListener('click', function () {
      store('declined'); hide();
    });
  }

  function hide() {
    var bar = document.getElementById('hsCookieBar');
    if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
  }

  /* ---------- footer "Cookie settings" link ---------- */
  function addFooterLink() {
    var foot = document.querySelector('.site-foot');
    if (!foot || document.getElementById('hsCookieSettings')) return;
    var a = document.createElement('a');
    a.id = 'hsCookieSettings';
    a.href = '#';
    a.textContent = 'Cookie settings';
    a.style.cssText = 'font-family:var(--font-mono,monospace);font-size:11px;letter-spacing:1px;' +
      'text-transform:uppercase;color:var(--text-dim);text-decoration:underline;margin:0 0 10px;' +
      'flex:1 0 100%;display:inline-block;';
    a.addEventListener('click', function (e) {
      e.preventDefault();
      try { localStorage.removeItem(KEY); } catch (err) {}
      buildBanner();
    });
    foot.appendChild(a);
  }

  function start() {
    var c = choice();
    if (c === 'accepted') loadGA();
    else if (c !== 'declined') buildBanner();
    addFooterLink();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
