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

    var last = window.pageYOffset;
    var acc = 0;          // 같은 방향으로 누적된 스크롤량
    var hidden = false;

    // 히스테리시스 임계값. 프레임 단위 델타로 토글하면 헤더가 계속 떨린다.
    var HIDE_AFTER = 110; // 아래로 이만큼 연속 스크롤해야 숨김
    var SHOW_AFTER = 60;  // 위로 이만큼 연속 스크롤해야 복귀
    var LOCK_TOP = 260;   // 이 지점 위쪽에서는 항상 보여준다

    function setHidden(v) {
      if (hidden === v) return;
      hidden = v;
      header.classList.toggle('is-hidden', v);
      acc = 0;
    }

    onScroll(function (y) {
      header.classList.toggle('is-stuck', y > 12);

      var d = y - last;
      last = y;

      // 방향이 바뀌면 누적을 초기화한다.
      if (d !== 0 && (d > 0) !== (acc > 0)) acc = 0;
      acc += d;

      var nav = $('#nav');
      var menuOpen = nav && nav.classList.contains('is-open');

      if (menuOpen || y <= LOCK_TOP) {
        setHidden(false);
      } else if (acc > HIDE_AFTER) {
        setHidden(true);
      } else if (acc < -SHOW_AFTER) {
        setHidden(false);
      }

      if (progress) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var p = max > 0 ? Math.min(Math.max(y / max, 0), 1) : 0;
        progress.style.transform = 'scaleX(' + p.toFixed(4) + ')';
        progress.classList.toggle('is-on', y > 12);
      }
    });
  }


  /* ------------------------------------------------------ 스크롤 리빌 */
  // 나중에 붙는 요소(동적 로딩된 인사이트 카드 등)도 같은 옵저버를 쓰도록
  // 모듈 스코프에 보관한다.
  var revealIO = null;

  function observeReveals(root) {
    var scope = root || document;
    var els = $$('.reveal:not(.is-in)', scope);
    // root 자체가 .reveal 인 경우(동적으로 붙인 카드)도 포함시킨다
    if (scope.nodeType === 1 && scope.matches && scope.matches('.reveal:not(.is-in)')) {
      els.unshift(scope);
    }
    if (!els.length) return;

    if (!revealIO) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    els.forEach(function (el) {
      var d = el.getAttribute('data-delay');
      if (d) el.style.setProperty('--reveal-delay', d + 'ms');
      revealIO.observe(el);
    });
  }

  function initReveal() {
    if (!reduced && 'IntersectionObserver' in window) {
      revealIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          revealIO.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    }
    observeReveals(document);
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
  var fadeEnabled = false;

  function bindFade(a) {
    if (!fadeEnabled || a.__faded) return;
    if (a.hasAttribute('data-no-fade')) return;

    var url;
    try { url = new URL(a.href, window.location.href); } catch (err) { return; }
    if (url.origin !== window.location.origin) return;
    if (a.target === '_blank' || (url.hash && url.pathname === window.location.pathname)) return;
    if (/^(mailto|tel):/.test(a.getAttribute('href') || '')) return;

    a.__faded = true;
    on(a, 'click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      document.body.classList.add('is-leaving');
      setTimeout(function () { window.location.href = a.href; }, 220);
    });
  }

  function bindFadeIn(root) {
    $$('a[href]', root || document).forEach(bindFade);
  }

  function initPageFade() {
    if (reduced) return;
    fadeEnabled = true;

    // 진입 시 페이드인은 CSS 애니메이션(body)이 담당한다.
    // 여기서는 나갈 때의 페이드아웃만 처리한다. JS 가 죽어도 화면은 항상 보인다.
    on(window, 'pageshow', function (e) {
      if (e.persisted) document.body.classList.remove('is-leaving');
    });

    bindFadeIn(document);
  }


  /* ------------------------------------------------ 인사이트 동적 로딩 */
  /*
   * 서버가 처음 몇 편을 그려 두고, 나머지는 여기서 한 편씩 이어 붙인다.
   *  · 아래로 스크롤해 센티넬에 닿으면 한 편
   *  · "더보기" 를 누르면 한 편
   * 한 편을 붙이면 센티넬이 화면 밖으로 밀려나므로, 다시 내려야 다음 편이 온다.
   * JS 가 없으면 더보기 링크가 ?show=N 로 그냥 동작한다.
   */
  function initInsightFeed() {
    var feed = $('#insightFeed');
    var foot = $('#feedFoot');
    if (!feed || !foot) return;

    var moreBtn = $('#feedMore');
    var sentinel = $('#feedSentinel');
    var hint = $('#feedHint');
    var doneEl = $('#feedDone');
    var errEl = $('#feedError');
    var countEl = $('.feed-more__count', moreBtn);

    var endpoint = feed.getAttribute('data-endpoint');
    var total = parseInt(feed.getAttribute('data-total'), 10) || 0;
    var step = parseInt(feed.getAttribute('data-step'), 10) || 1;
    var offset = parseInt(feed.getAttribute('data-offset'), 10) || 0;

    var INTENT_PX = 110;     // 아래로 이만큼 움직여야 다음 한 편
    var COOLDOWN = 700;      // 한 번의 플릭으로 여러 편이 쏟아지지 않게

    var busy = false;
    var intent = 0;          // 마지막 로딩 이후 아래로 움직인 양
    var lastY = window.pageYOffset;
    var cooldownUntil = 0;

    function remaining() { return Math.max(0, total - offset); }

    function syncFoot() {
      var left = remaining();
      if (countEl) countEl.textContent = left;
      if (left <= 0) {
        foot.hidden = true;
        if (doneEl) doneEl.hidden = false;
      }
    }

    function setBusy(state) {
      busy = state;
      moreBtn.classList.toggle('is-loading', state);
      moreBtn.setAttribute('aria-busy', state ? 'true' : 'false');
      if (hint) hint.classList.toggle('is-dim', state);
    }

    function load() {
      if (busy || remaining() <= 0) return;

      // 로딩을 시작하는 순간 트리거를 해제한다. 이렇게 해야 더보기 클릭과
      // 스크롤 트리거가 겹쳐 두 편이 한꺼번에 들어오는 일이 없다.
      intent = 0;
      lastY = window.pageYOffset;
      cooldownUntil = Date.now() + COOLDOWN;

      setBusy(true);
      if (errEl) errEl.hidden = true;

      var url = endpoint + '?offset=' + offset + '&limit=' + step;

      fetch(url, { headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (data) {
          if (!data || !data.count) { total = offset; syncFoot(); return; }

          var first = feed.children.length;
          feed.insertAdjacentHTML('beforeend', data.html);

          // 새로 붙은 카드에만 리빌·페이드 처리를 걸어 준다
          var added = Array.prototype.slice.call(feed.children, first);
          added.forEach(function (el) {
            observeReveals(el);
            if (el.matches && el.matches('a[href]')) bindFade(el);
            bindFadeIn(el);
          });

          offset = typeof data.next_offset === 'number' ? data.next_offset : offset + data.count;
          if (typeof data.total === 'number') total = data.total;
          syncFoot();

          // 더보기 링크의 no-JS 폴백 주소도 최신 상태로 유지
          moreBtn.setAttribute('href', moreBtn.pathname + '?show=' + (offset + step));
        })
        .catch(function () {
          if (errEl) errEl.hidden = false;
        })
        .then(function () { setBusy(false); });
    }

    on(moreBtn, 'click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      load();
    });

    /*
     * 자동 로딩 트리거.
     *
     * IntersectionObserver 도, 스크롤 '위치' 비교도 쓸 수 없다.
     * 카드가 그리드에 가로로 채워지면 문서 높이가 오히려 줄어들 수 있어서
     * (2장 → 3장으로 한 줄에 들어차면서 카드가 낮아진다) "더 내려와야 한다" 는
     * 조건이 영원히 충족되지 않고, 바닥에 붙은 뒤로는 scroll 이벤트 자체가 없다.
     *
     * 그래서 위치가 아니라 아래로 움직이려는 '의도' 를 누적한다.
     *   · scroll  — 실제로 내려간 거리
     *   · wheel   — 바닥에 닿아 더 안 내려가도 이벤트는 계속 온다
     *   · touch   — 모바일에서 위로 미는 동작
     * 조건: 누적 ≥ INTENT_PX · 쿨다운 경과 · 센티넬이 화면 아래 140px 안
     */
    function sentinelNear() {
      return sentinel.getBoundingClientRect().top < window.innerHeight + 140;
    }

    function nudge(px) {
      if (!sentinel || busy || remaining() <= 0) return;
      if (px > 0) intent += px;
      if (intent < INTENT_PX) return;
      if (Date.now() < cooldownUntil) return;
      if (sentinelNear()) load();
    }

    onScroll(function (y) {
      var d = y - lastY;
      lastY = y;
      nudge(d);
    });

    on(window, 'wheel', function (e) {
      if (e.deltaY > 0) nudge(Math.min(e.deltaY, 120));
    }, { passive: true });

    var touchY = null;
    on(window, 'touchstart', function (e) {
      touchY = e.touches && e.touches[0] ? e.touches[0].clientY : null;
    }, { passive: true });
    on(window, 'touchmove', function (e) {
      if (touchY === null || !e.touches || !e.touches[0]) return;
      var y = e.touches[0].clientY;
      nudge(touchY - y);          // 손가락을 위로 밀면 아래로 내려가는 것
      touchY = y;
    }, { passive: true });

    syncFoot();
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
    initInsightFeed();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
