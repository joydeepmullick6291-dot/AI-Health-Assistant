document.addEventListener('DOMContentLoaded', () => {
  const patient = JSON.parse(localStorage.getItem('biocanvas-current-user') || '{}');

  const fill = (selector, value) => {
    document.querySelectorAll(selector).forEach((el) => {
      if (el) el.textContent = value;
    });
  };

  if (patient.name) fill('.user-pill strong', patient.name);
  if (patient.id) fill('.user-pill span', `PATIENT ID · ${patient.id}`);
  if (patient.refill) fill('#dashboard .mini-card:nth-of-type(1) h2', patient.refill);
  if (patient.updates) fill('#dashboard .mini-card:nth-of-type(2) h2', patient.updates);

  document.querySelectorAll('.nav-link[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.querySelectorAll('.nav-link').forEach((item) => item.classList.remove('active'));
      link.classList.add('active');
    });
  });

  const setActiveByScroll = () => {
    const sections = ['dashboard','appointments','records','prescriptions','labreports','profile']
      .map((id) => document.getElementById(id))
      .filter(Boolean);

    const fromTop = window.scrollY + 140;
    let current = sections[0]?.id || 'dashboard';

    sections.forEach((section) => {
      if (section.offsetTop <= fromTop) current = section.id;
    });

    document.querySelectorAll('.nav-link').forEach((item) => {
      item.classList.toggle('active', item.getAttribute('href') === `#${current}`);
    });
  };

  window.addEventListener('scroll', setActiveByScroll, { passive: true });
  setActiveByScroll();

  const toast = (message) => {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = message;
    document.body.appendChild(el);

    requestAnimationFrame(() => el.classList.add('show'));

    setTimeout(() => {
      el.classList.remove('show');
      setTimeout(() => el.remove(), 200);
    }, 1600);
  };

  document.querySelectorAll('[data-book-slot]').forEach((button) => {
    button.addEventListener('click', () => toast(`Selected ${button.dataset.book-slot}`));
  });

  document.querySelectorAll('[data-download-report]').forEach((button) => {
    button.addEventListener('click', () => toast('Report download started'));
  });

  document.querySelectorAll('[data-run-prediction]').forEach((button) => {
    button.addEventListener('click', () => toast('Prediction started'));
  });

  document.querySelectorAll('[data-save-vitals]').forEach((button) => {
    button.addEventListener('click', () => toast('Vitals saved'));
  });

  document.querySelectorAll('.btn.btn-primary[type="button"]').forEach((button) => {
    if (button.textContent.trim() === 'Edit profile') {
      button.addEventListener('click', () => toast('Profile editor coming next'));
    }
  });
});