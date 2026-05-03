/* ============================================================
   Ben Mann — interactions
   - Sticky-nav state
   - Scroll reveals
   - Form validation + success/error states
   - Footer year
   ============================================================ */

(() => {
  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---- Footer year ---- */
  const yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Live NZT clock in footer (HH:MM, updates every 30s) ---- */
  const clockEl = $('#clock');
  if (clockEl) {
    const tick = () => {
      const t = new Date().toLocaleTimeString('en-NZ', {
        timeZone: 'Pacific/Auckland',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      });
      clockEl.textContent = t;
    };
    tick();
    setInterval(tick, 30000);
  }

  /* ---- Sticky nav border once we've scrolled past the top ---- */
  const nav = $('#nav');
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Scroll reveals via IntersectionObserver ---- */
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = $$('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-in'));
  } else {
    // Apply per-element delay from data-delay attribute
    reveals.forEach((el) => {
      const d = el.dataset.delay;
      if (d) el.style.setProperty('--reveal-delay', `${d}ms`);
    });

    // Auto-stagger reveals inside groups that share a parent — capability tiles,
    // case studies, sector tags. The first reveal in the group enters at its own
    // delay; each subsequent sibling adds a step.
    const stagger = (selector, step = 90) => {
      const groups = new Map();
      $$(selector).forEach((el) => {
        const parent = el.parentElement;
        if (!parent) return;
        const list = groups.get(parent) || [];
        list.push(el);
        groups.set(parent, list);
      });
      groups.forEach((list) => {
        list.forEach((el, i) => {
          const base = parseInt(el.dataset.delay || '0', 10);
          el.style.setProperty('--reveal-delay', `${base + i * step}ms`);
        });
      });
    };
    stagger('.cap.reveal', 80);
    stagger('.case.reveal', 90);

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );

    reveals.forEach((el) => io.observe(el));
  }

  /* ---- Smooth-scroll offset for sticky nav (handled by CSS smooth scroll;
          add focus management for accessibility) ---- */
  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href').slice(1);
      if (!id) return;
      const target = document.getElementById(id);
      if (!target) return;
      // Let the browser smooth-scroll, then move focus for keyboard users
      setTimeout(() => {
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }, 600);
    });
  });

  /* ---- Form: lightweight validation, fake success state ---- */
  const form   = $('#enquiry');
  const status = $('#formStatus');

  const setStatus = (msg, kind = '') => {
    if (!status) return;
    status.textContent = msg;
    status.classList.remove('is-success', 'is-error');
    if (kind) status.classList.add(`is-${kind}`);
  };

  const isEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  if (form) {
    // Live-clear invalid state when the user starts typing again
    form.addEventListener('input', (e) => {
      const t = e.target;
      if (t.classList && t.classList.contains('is-invalid')) {
        t.classList.remove('is-invalid');
      }
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const fd = new FormData(form);
      const name    = (fd.get('name')    || '').toString().trim();
      const email   = (fd.get('email')   || '').toString().trim();
      const message = (fd.get('message') || '').toString().trim();

      const fields = {
        name:    { value: name,    valid: name.length    >= 2 },
        email:   { value: email,   valid: isEmail(email) },
        message: { value: message, valid: message.length >= 5 },
      };

      let firstInvalid = null;
      Object.entries(fields).forEach(([key, info]) => {
        const input = form.querySelector(`[name="${key}"]`);
        if (!input) return;
        if (!info.valid) {
          input.classList.add('is-invalid');
          input.setAttribute('aria-invalid', 'true');
          if (!firstInvalid) firstInvalid = input;
        } else {
          input.removeAttribute('aria-invalid');
        }
      });

      if (firstInvalid) {
        firstInvalid.focus();
        setStatus('Please fill in the highlighted fields so I can get back to you.', 'error');
        return;
      }

      // Disable submit + show pending state
      const submitBtn = form.querySelector('button[type="submit"]');
      const labelEl   = submitBtn?.querySelector('.btn__label');
      const originalLabel = labelEl?.textContent;
      if (submitBtn) submitBtn.disabled = true;
      if (labelEl)   labelEl.textContent = 'Sending…';
      setStatus('');

      /* ---- Front-end only for now. Wire to a real endpoint later, e.g.:
              fetch('/api/enquiry', { method: 'POST', body: fd })
                .then(...)
         For now we simulate a successful send. */
      setTimeout(() => {
        form.reset();
        form.classList.add('is-sent');
        if (submitBtn) submitBtn.disabled = false;
        if (labelEl)   labelEl.textContent = originalLabel || 'Send enquiry';
        setStatus(`Thanks ${name.split(' ')[0]} — your enquiry's in. I'll reply within one working day.`, 'success');
      }, 700);
    });
  }
})();
