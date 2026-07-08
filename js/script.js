/* =====================================================================
   Nicholo Dela Rosa — Portfolio interactions
   ===================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  setupScrollProgress();
  setupNavHighlight();
  setupScrollNav();
  setupHamburger();
  setupSectionAnimations();
  setupScrollReveal();
  setupRevealButton();
  setupContactForm();
});

// Hide the loading screen once everything (incl. SVG art) has loaded.
window.addEventListener('load', () => {
  const loader = document.getElementById('loader');
  if (loader) setTimeout(() => loader.classList.add('done'), 350);
});

function setupScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
  }, { passive: true });
}

function setupNavHighlight() {
  const links = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { threshold: 0.5 });
  sections.forEach(s => observer.observe(s));
}

function setupSectionAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('section').forEach(s => observer.observe(s));
}

function setupScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('revealed');
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

function setupRevealButton() {
  const btn = document.getElementById('skillsRevealBtn');
  const content = document.getElementById('skillsContent');
  if (!btn || !content) return;
  btn.addEventListener('click', () => {
    const wasHidden = content.classList.contains('hidden');
    content.classList.toggle('hidden');
    btn.textContent = wasHidden ? 'Slide the Screen Shut' : 'Open the Screen';
    btn.setAttribute('aria-expanded', String(wasHidden));
  });
}

function setupScrollNav() {
  const nav = document.getElementById('nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });
}

function setupHamburger() {
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');
  if (!hamburger || !navLinks) return;
  const toggle = (open) => {
    navLinks.classList.toggle('open', open);
    hamburger.classList.toggle('active', open);
    hamburger.setAttribute('aria-expanded', String(open));
  };
  hamburger.addEventListener('click', () => toggle(!navLinks.classList.contains('open')));
  // Close the menu after tapping a link (mobile).
  navLinks.querySelectorAll('.nav-link').forEach(link =>
    link.addEventListener('click', () => toggle(false))
  );
}

function setupContactForm() {
  const form = document.querySelector('.contact-form');
  const status = document.getElementById('formStatus');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.querySelector('#c-name');
    const email = form.querySelector('#c-email');
    const msg = form.querySelector('#c-msg');
    if (!name.value.trim() || !email.value.trim() || !msg.value.trim()) {
      if (status) { status.style.color = 'var(--vermilion)'; status.textContent = 'Please fill in every field.'; }
      return;
    }
    if (status) {
      status.style.color = 'var(--matcha)';
      status.textContent = `Thank you, ${name.value.trim()} — your message has been received.`;
    }
    form.reset();
  });
}
