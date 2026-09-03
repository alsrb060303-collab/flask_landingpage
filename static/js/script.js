/* ==========================================================================
   UNIV — 인터랙션
   순수 JavaScript. 외부 라이브러리 없음.
   1. 유틸  2. 헤더  3. 스크롤 리빌  4. 카운트업  5. 패럴랙스
   6. 타이핑  7. 마그네틱 버튼  8. 카드 포인터 글로우  9. 모바일 메뉴
   10. 문의 폼  11. 페이지 전환
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raf = window.requestAnimationFrame || function (cb) { return setTimeout(cb, 16); };

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function on(el, ev, fn, opt) { if (el) el.addEventListener(ev, fn, opt); }

  /* 스크롤 이벤트를 rAF 로 묶어 한 프레임에 한 번만 처리한다. */
  var scrollTasks = [];
  var ticking = false;
  function onScroll(fn) {
    scrollTasks.push(fn);
    if (scrollTasks.length === 1) {
      window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        raf(function () {
          var y = window.pageYOffset;
          for (var i = 0; i < scrollTasks.length; i++) scrollTasks[i](y);
          ticking = false;
        });
      }, { passive: true });
    }
    fn(window.pageYOffset);
  }

  document.documentElement.classList.remove('no-js');


  /* ---------------------------------------------------------------- 헤더 */
  function initHeader() {
    var header = $('#header');
    var progress = $('#scrollProgress');
    if (!header) return;

    var last = 0;

    onScroll(function (y) {
      header.classList.toggle('is-stuck', y > 12);

      // 아래로 빠르게 스크롤하면 헤더를 숨기고, 위로 올리면 즉시 되돌린다.
      var nav = $('#nav');
      var menuOpen = nav && nav.classList.contains('is-open');
      if (!menuOpen) {
        header.classList.toggle('is-hidden', y > 240 && y > last + 4);
      }
      last = y;

      if (progress) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
      }
    });
  }


  /* ------------------------------------------------------ 스크롤 리빌 */
  function initReveal() {
    var els = $$('.reveal');
    if (!els.length) return;

    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    els.forEach(function (el) {
      var d = el.getAttribute('data-delay');
      if (d) el.style.setProperty('--reveal-delay', d + 'ms');
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    els.forEach(function (el) { io.observe(el); });
  }


  /* ---------------------------------------------------------- 카운트업 */
  function initCounters() {
    var els = $$('[data-count]');
    if (!els.length || !('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        count(e.target);
      });
    }, { threshold: 0.5 });

    els.forEach(function (el) { io.observe(el); });

    function count(el) {
      var target = parseFloat(el.getAttribute('data-count')) || 0;
      var suffix = el.getAttribute('data-suffix') || '';
      if (reduced) { el.textContent = target + suffix; return; }

      var dur = 1500;
      var start = null;

      function frame(ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);           // easeOutCubic
        el.textContent = Math.round(target * eased) + (p === 1 ? suffix : '');
        if (p < 1) raf(frame);
      }
      raf(frame);
    }
  }


  /* ---------------------------------------------------------- 패럴랙스 */
  function initParallax() {
    if (reduced) return;
    var els = $$('[data-parallax]');
    if (!els.length) return;

    onScroll(function (y) {
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var rect = el.getBoundingClientRect();
        if (rect.bottom < -200 || rect.top > vh + 200) return;
        var speed = parseFloat(el.getAttribute('data-parallax')) || 0;
        var offset = (rect.top + rect.height / 2 - vh / 2) * speed;
        el.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,0)';
      });
    });
  }


  /* -------------------------------------------------------- 타이핑 연출 */
  function initTypewriter() {
    var box = $('.typewriter');
    if (!box) return;

    var out = $('.typewriter__text', box);
    var words;
    try { words = JSON.parse(box.getAttribute('data-words') || '[]'); }
    catch (err) { words = []; }
    if (!words.length || !out) return;

    if (reduced) { out.textContent = words[0]; return; }

    var wi = 0, ci = 0, deleting = false;

    function tick() {
      var word = words[wi];
      ci += deleting ? -1 : 1;
      out.textContent = word.slice(0, ci);

      var wait = deleting ? 34 : 68;
      if (!deleting && ci === word.length) { deleting = true; wait = 1700; }
      else if (deleting && ci === 0) { deleting = false; wi = (wi + 1) % words.length; wait = 320; }

      setTimeout(tick, wait);
    }
    setTimeout(tick, 900);
  }


  /* ------------------------------------------------------ 마그네틱 버튼 */
  function initMagnetic() {
    if (reduced || !window.matchMedia('(hover: hover)').matches) return;

    $$('.magnetic').forEach(function (el) {
      var raf_ = null;

      on(el, 'pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var mx = e.clientX - r.left - r.width / 2;
        var my = e.clientY - r.top - r.height / 2;
        if (raf_) return;
        raf_ = raf(function () {
          el.style.transform = 'translate(' + (mx * 0.22).toFixed(2) + 'px,' + (my * 0.3).toFixed(2) + 'px)';
          raf_ = null;
        });
      });

      on(el, 'pointerleave', function () { el.style.transform = ''; });
    });
  }


  /* ------------------------------------------------ 카드 포인터 글로우 */
  function initCardGlow() {
    if (reduced || !window.matchMedia('(hover: hover)').matches) return;

    $$('.service-card').forEach(function (card) {
      on(card, 'pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }


  /* -------------------------------------------------------- 모바일 메뉴 */
  function initNav() {
    var toggle = $('#navToggle');
    var nav = $('#nav');
    if (!toggle || !nav) return;

    function close() {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
    }

    on(toggle, 'click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('is-locked', open);
      if (open) $('#header').classList.remove('is-hidden');
    });

    $$('a', nav).forEach(function (a) { on(a, 'click', close); });

    on(document, 'keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { close(); toggle.focus(); }
    });

    on(window, 'resize', function () {
      if (window.innerWidth > 860) close();
    });
  }


  /* ------------------------------------------------------------ 문의 폼 */
  function initContactForm() {
    var form = $('#contactForm');
    if (!form) return;

    // 서비스 상세 페이지에서 넘어온 ?service=slug 를 미리 선택해 둔다.
    var slug = new URLSearchParams(window.location.search).get('service');
    var select = $('#f-service', form);
    if (slug && select) {
      $$('option', select).forEach(function (opt) {
        if (opt.getAttribute('data-slug') === slug) opt.selected = true;
      });
    }

    on(form, 'submit', function (e) {
      e.preventDefault();

      var ok = true;
      $$('input, textarea, select', form).forEach(function (el) {
        var field = el.closest('.field');
        var bad = el.hasAttribute('required') && !el.value.trim();
        if (field) field.classList.toggle('is-invalid', bad);
        if (bad && ok) { el.focus(); ok = false; }
      });
      if (!ok) return;

      var v = function (id) { var el = $('#' + id, form); return el ? el.value.trim() : ''; };
      var ko = document.body.getAttribute('data-lang') === 'ko';

      var subject = (ko ? '[상담 문의] ' : '[Enquiry] ') + v('f-service') + ' — ' + v('f-company');
      var body = [
        (ko ? '회사명: ' : 'Company: ') + v('f-company'),
        (ko ? '담당자: ' : 'Name: ') + v('f-name'),
        (ko ? '이메일: ' : 'Email: ') + v('f-email'),
        (ko ? '연락처: ' : 'Phone: ') + (v('f-phone') || '-'),
        (ko ? '관심 서비스: ' : 'Service: ') + v('f-service'),
        '',
        (ko ? '문의 내용' : 'Message'),
        '----------------------------------------',
        v('f-message')
      ].join('\n');

      window.location.href = 'mailto:' + form.getAttribute('data-to') +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
    });

    $$('input, textarea, select', form).forEach(function (el) {
      on(el, 'input', function () {
        var field = el.closest('.field');
        if (field) field.classList.remove('is-invalid');
      });
    });
  }


  /* -------------------------------------------------------- 페이지 전환 */
  function initPageFade() {
    if (reduced) return;

    // 진입 시 페이드인은 CSS 애니메이션(body)이 담당한다.
    // 여기서는 나갈 때의 페이드아웃만 처리한다. JS 가 죽어도 화면은 항상 보인다.
    on(window, 'pageshow', function (e) {
      if (e.persisted) document.body.classList.remove('is-leaving');
    });

    $$('a[href]').forEach(function (a) {
      var url;
      try { url = new URL(a.href, window.location.href); } catch (err) { return; }
      if (url.origin !== window.location.origin) return;
      if (a.target === '_blank' || url.hash && url.pathname === window.location.pathname) return;
      if (/^(mailto|tel):/.test(a.getAttribute('href') || '')) return;

      on(a, 'click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        document.body.classList.add('is-leaving');
        setTimeout(function () { window.location.href = a.href; }, 220);
      });
    });
  }


  /* ------------------------------------------------------------ 부트스트랩 */
  function boot() {
    initHeader();
    initReveal();
    initCounters();
    initParallax();
    initTypewriter();
    initMagnetic();
    initCardGlow();
    initNav();
    initContactForm();
    initPageFade();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
