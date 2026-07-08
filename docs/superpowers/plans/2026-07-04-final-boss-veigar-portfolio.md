# Final Boss Veigar Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page portfolio site themed after Final Boss Veigar with Dragon City-style RPG UI frames.

**Architecture:** Static single-page site. All pixel art elements are generated via CSS and JavaScript — no external image assets. Sections are stacked vertically with scroll-based interactions. RPG frame borders, glitch text, and pixel particles are implemented through CSS pseudo-elements, clip-path, and keyframe animations.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript. No frameworks, no build tools.

**File Structure:**
- `index.html` — All HTML content, links to CSS/JS
- `css/style.css` — All styles (reset, palette, layout, components, animations, responsive)
- `js/script.js` — All JavaScript (scroll progress, particles, nav, animations)

## Global Constraints

- Palette hex values must match exactly: `#0d0415`, `#1a0a2e`, `#6c3483`, `#8b5cf6`, `#ff00ff`, `#00ffff`, `#39ff14`, `#c4b5fd`
- Monospace font for all text (system monospace or `'Courier New'`)
- No external image assets — all pixel art via CSS/JS
- No frameworks or build tools
- Single-page application — no routing
- No backend or database
- Contact form is static placeholder only (no processing)

---

### Task 1: Project Scaffold — HTML skeleton, CSS reset, palette, font setup

**Files:**
- Create: `index.html`
- Create: `css/style.css`
- Create: `js/script.js`

**Interfaces:**
- Produces: HTML with `<header>`, `<main>`, `<footer>` containers; CSS with `:root` variables, reset, fonts; JS with `DOMContentLoaded` listener

- [ ] **Step 1: Create `index.html` with document skeleton**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav id="nav"></nav>
  <main id="main-content">
    <section id="hero"></section>
    <section id="about"></section>
    <section id="projects"></section>
    <section id="skills"></section>
    <section id="contact"></section>
  </main>
  <div id="scroll-progress"></div>
  <div id="scanlines"></div>
  <script src="js/script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create `css/style.css` with reset, variables, fonts, global styles**

```css
:root {
  --void: #0d0415;
  --dark-purple: #1a0a2e;
  --mid-purple: #6c3483;
  --bright-violet: #8b5cf6;
  --magenta: #ff00ff;
  --cyan: #00ffff;
  --green: #39ff14;
  --text: #c4b5fd;
}

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Courier New', Courier, monospace;
  background: var(--void);
  color: var(--text);
  overflow-x: hidden;
}

section {
  min-height: 100vh;
  padding: 80px 20px;
  position: relative;
}

/* scanlines overlay */
#scanlines {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255, 255, 255, 0.015) 2px,
    rgba(255, 255, 255, 0.015) 4px
  );
}

/* scroll progress bar */
#scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--magenta), var(--cyan), var(--green));
  z-index: 10000;
  width: 0%;
  transition: width 0.1s linear;
}
```

- [ ] **Step 3: Create `js/script.js` with DOMContentLoaded listener**

```js
document.addEventListener('DOMContentLoaded', () => {
  console.log('Portfolio loaded');
});
```

---

### Task 2: Hero Section — Frame border, glitch text, stat bars, particles

**Files:**
- Modify: `index.html` — fill `#hero` content
- Modify: `css/style.css` — hero styles, frame border, glitch, stat bars, particles

**Interfaces:**
- Consumes: `:root` CSS variables from Task 1
- Produces: `#hero` fully styled with all sub-components

- [ ] **Step 1: Add hero HTML to `index.html`**

```html
<section id="hero">
  <div id="hero-frame-top" class="frame-bar">
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
    <span class="dragon-scale"></span>
  </div>
  <div id="particles"></div>
  <div class="hero-content">
    <div class="glitch-wrapper">
      <h1 class="glitch" data-text="YOUR NAME">YOUR NAME</h1>
    </div>
    <div class="title-label">&gt; FULL-STACK DEVELOPER</div>
    <div class="stat-bars">
      <div class="stat-bar">
        <span class="stat-label">HP</span>
        <div class="stat-track"><div class="stat-fill hp" style="width:85%"></div></div>
        <span class="stat-name">Projects</span>
      </div>
      <div class="stat-bar">
        <span class="stat-label">MP</span>
        <div class="stat-track"><div class="stat-fill mp" style="width:70%"></div></div>
        <span class="stat-name">Tech Stack</span>
      </div>
      <div class="stat-bar">
        <span class="stat-label">XP</span>
        <div class="stat-track"><div class="stat-fill xp" style="width:42%"></div></div>
        <span class="stat-name">Experience</span>
      </div>
    </div>
  </div>
  <div class="corner-tl"></div><div class="corner-tr"></div>
  <div class="corner-bl"></div><div class="corner-br"></div>
</section>
```

- [ ] **Step 2: Add hero CSS — layout, glitch text, stat bars**

```css
#hero {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: var(--void);
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
}

/* Glitch text */
.glitch-wrapper {
  display: inline-block;
  position: relative;
}

.glitch {
  font-size: clamp(2rem, 6vw, 4rem);
  color: #fff;
  letter-spacing: 4px;
  text-transform: uppercase;
  position: relative;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch::before {
  color: var(--magenta);
  clip-path: inset(10% 0 60% 0);
  left: -2px;
}

.glitch::after {
  color: var(--cyan);
  clip-path: inset(55% 0 5% 0);
  left: 2px;
}

.glitch:hover::before {
  left: 2px;
  transition: left 0.1s;
}

.glitch:hover::after {
  left: -2px;
  transition: left 0.15s;
}

/* Title label */
.title-label {
  display: inline-block;
  margin-top: 12px;
  font-size: clamp(0.7rem, 1.5vw, 0.9rem);
  color: var(--bright-violet);
  letter-spacing: 4px;
  border: 1px solid var(--mid-purple);
  padding: 8px 20px;
}

/* Stat bars */
.stat-bars {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.stat-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 280px;
  max-width: 80vw;
}

.stat-label {
  color: var(--magenta);
  font-size: 0.7rem;
  width: 24px;
  text-align: right;
}

.stat-track {
  flex: 1;
  height: 4px;
  background: var(--void);
  border: 1px solid var(--mid-purple);
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  transition: width 1.5s ease;
}

.stat-fill.hp {
  background: linear-gradient(90deg, var(--green), var(--magenta));
}

.stat-fill.mp {
  background: linear-gradient(90deg, var(--bright-violet), var(--cyan));
}

.stat-fill.xp {
  background: linear-gradient(90deg, var(--mid-purple), var(--green));
}

.stat-name {
  color: var(--text);
  font-size: 0.65rem;
  width: 80px;
  text-align: left;
}
```

- [ ] **Step 3: Add RPG frame border CSS — dragon scale pattern + corner art**

```css
/* Frame bar — dragon scale pattern */
.frame-bar {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  gap: 2px;
  justify-content: center;
  z-index: 10;
}

#hero-frame-top {
  top: 0;
}

.dragon-scale {
  width: 10px;
  height: 10px;
  clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
}

.dragon-scale:nth-child(odd) {
  background: var(--mid-purple);
}

.dragon-scale:nth-child(even) {
  background: var(--bright-violet);
}

/* Corner decorations */
.corner-tl, .corner-tr, .corner-bl, .corner-br {
  position: absolute;
  width: 40px;
  height: 40px;
  z-index: 10;
}

.corner-tl {
  top: 0;
  left: 0;
  border-top: 3px solid var(--magenta);
  border-left: 3px solid var(--magenta);
}

.corner-tr {
  top: 0;
  right: 0;
  border-top: 3px solid var(--cyan);
  border-right: 3px solid var(--cyan);
}

.corner-bl {
  bottom: 0;
  left: 0;
  border-bottom: 3px solid var(--green);
  border-left: 3px solid var(--green);
}

.corner-br {
  bottom: 0;
  right: 0;
  border-bottom: 3px solid var(--magenta);
  border-right: 3px solid var(--magenta);
}
```

- [ ] **Step 4: Add floating pixel particles (CSS animation structure, JS generates elements)**

Add to `css/style.css`:
```css
.particle {
  position: absolute;
  z-index: 1;
  pointer-events: none;
  animation: float-up linear infinite;
}

@keyframes float-up {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100vh) scale(0.5);
    opacity: 0;
  }
}
```

Add to `js/script.js`:
```js
function createParticles() {
  const container = document.getElementById('particles');
  const colors = ['#ff00ff', '#00ffff', '#39ff14', '#8b5cf6'];
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = 3 + Math.random() * 4;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      left:${Math.random()*100}%;
      bottom:${Math.random()*20}%;
      animation-duration:${8 + Math.random()*12}s;
      animation-delay:${Math.random()*10}s;
      opacity:${0.2 + Math.random()*0.5};
    `;
    container.appendChild(p);
  }
}
```

Call `createParticles()` inside the `DOMContentLoaded` callback.

---

### Task 3: About Section — Dialogue box, pixel avatar, stats panel

**Files:**
- Modify: `index.html` — fill `#about` content
- Modify: `css/style.css` — about styles

- [ ] **Step 1: Add about HTML to `index.html`**

```html
<section id="about">
  <h2 class="section-title">&gt; ABOUT</h2>
  <div class="about-content">
    <div class="avatar-frame">
      <div class="pixel-avatar">
        <!-- 16-bit style portrait built with CSS div grid -->
        <div class="avatar-head"></div>
        <div class="avatar-body"></div>
        <div class="avatar-hat"></div>
      </div>
    </div>
    <div class="dialogue-box">
      <p class="dialogue-text">
        <span class="dialogue-arrow">&gt;&gt;</span>
        Full-stack developer who builds websites and systems. 
        Passionate about clean architecture and pixel-perfect 
        implementations.
      </p>
    </div>
    <div class="stats-panel">
      <div class="stat-row"><span class="stat-key">LEVEL</span><span class="stat-val">42</span></div>
      <div class="stat-row"><span class="stat-key">YEARS</span><span class="stat-val">8</span></div>
      <div class="stat-row"><span class="stat-key">PROJECTS</span><span class="stat-val">20+</span></div>
      <div class="stat-row"><span class="stat-key">LANGUAGES</span><span class="stat-val">6</span></div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add about CSS**

```css
#about {
  background: var(--dark-purple);
}

.section-title {
  font-size: 1.2rem;
  color: var(--magenta);
  letter-spacing: 6px;
  text-align: center;
  margin-bottom: 40px;
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 120px 1fr 120px;
  gap: 20px;
  align-items: start;
}

@media (max-width: 600px) {
  .about-content {
    grid-template-columns: 1fr;
    justify-items: center;
  }
}

/* Pixel avatar */
.avatar-frame {
  width: 120px;
  height: 120px;
  border: 2px solid var(--mid-purple);
  background: var(--void);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.pixel-avatar {
  position: relative;
  width: 80px;
  height: 100px;
}

.avatar-hat {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-bottom: 25px solid var(--mid-purple);
}

.avatar-head {
  position: absolute;
  top: 25px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 28px;
  background: var(--mid-purple);
  border-radius: 4px;
  box-shadow: 
    inset 4px 6px 0 var(--magenta),
    inset -4px 6px 0 var(--cyan);
}

.avatar-body {
  position: absolute;
  top: 53px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 45px;
  background: var(--dark-purple);
  border: 1px solid var(--mid-purple);
}

/* Dialogue box */
.dialogue-box {
  background: var(--void);
  border: 2px solid var(--mid-purple);
  padding: 20px;
  position: relative;
}

.dialogue-box::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  height: 3px;
  background: linear-gradient(90deg, var(--magenta), var(--cyan), var(--green));
}

.dialogue-text {
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--text);
}

.dialogue-arrow {
  color: var(--green);
  margin-right: 6px;
}

/* Stats panel */
.stats-panel {
  border: 2px solid var(--mid-purple);
  background: var(--void);
  padding: 12px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--dark-purple);
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-key {
  color: var(--magenta);
  font-size: 0.65rem;
  letter-spacing: 2px;
}

.stat-val {
  color: var(--cyan);
  font-size: 0.7rem;
}
```

---

### Task 4: Projects Section — Cards with RPG frames, hover corruption

**Files:**
- Modify: `index.html` — fill `#projects` content
- Modify: `css/style.css` — project card styles, hover corruption

- [ ] **Step 1: Add projects HTML**

```html
<section id="projects">
  <h2 class="section-title">&gt; PROJECTS</h2>
  <div class="projects-grid">
    <!-- Featured case study -->
    <div class="project-card featured" data-featured="true">
      <div class="card-frame-top">
        <span class="scale"></span><span class="scale"></span>
        <span class="scale"></span><span class="scale"></span>
        <span class="scale"></span><span class="scale"></span>
      </div>
      <div class="card-body">
        <div class="card-thumb">[ SCREENSHOT ]</div>
        <h3 class="card-title">Real-Time Dashboard</h3>
        <p class="card-desc">Built with React, Node.js, WebSockets — handling 10k concurrent users.</p>
        <div class="card-tags">
          <span class="tag">React</span>
          <span class="tag">Node.js</span>
          <span class="tag">WebSockets</span>
        </div>
      </div>
      <div class="corruption-overlay">
        <span class="glitch-text">VIEW CASE STUDY</span>
      </div>
      <div class="corner-tl"></div><div class="corner-tr"></div>
      <div class="corner-bl"></div><div class="corner-br"></div>
    </div>
    <!-- Project card 2 -->
    <div class="project-card">
      <div class="card-frame-top">
        <span class="scale"></span><span class="scale"></span>
        <span class="scale"></span><span class="scale"></span>
      </div>
      <div class="card-body">
        <div class="card-thumb">[ SCREENSHOT ]</div>
        <h3 class="card-title">Headless CMS</h3>
        <p class="card-desc">Next.js + Strapi for a publishing platform with automated workflows.</p>
        <div class="card-tags">
          <span class="tag">Next.js</span>
          <span class="tag">Strapi</span>
          <span class="tag">Postgres</span>
        </div>
      </div>
      <div class="corruption-overlay">
        <span class="glitch-text">VIEW DETAILS</span>
      </div>
      <div class="corner-tl"></div><div class="corner-tr"></div>
      <div class="corner-bl"></div><div class="corner-br"></div>
    </div>
    <!-- Project card 3 -->
    <div class="project-card">
      <div class="card-frame-top">
        <span class="scale"></span><span class="scale"></span>
        <span class="scale"></span><span class="scale"></span>
      </div>
      <div class="card-body">
        <div class="card-thumb">[ SCREENSHOT ]</div>
        <h3 class="card-title">E-Commerce Platform</h3>
        <p class="card-desc">Full-stack marketplace with payment integration and inventory management.</p>
        <div class="card-tags">
          <span class="tag">React</span>
          <span class="tag">Express</span>
          <span class="tag">Stripe</span>
        </div>
      </div>
      <div class="corruption-overlay">
        <span class="glitch-text">VIEW DETAILS</span>
      </div>
      <div class="corner-tl"></div><div class="corner-tr"></div>
      <div class="corner-bl"></div><div class="corner-br"></div>
    </div>
    <!-- Project card 4 -->
    <div class="project-card">
      <div class="card-frame-top">
        <span class="scale"></span><span class="scale"></span>
        <span class="scale"></span><span class="scale"></span>
      </div>
      <div class="card-body">
        <div class="card-thumb">[ SCREENSHOT ]</div>
        <h3 class="card-title">CLI Tool</h3>
        <p class="card-desc">Node.js CLI for scaffolding microservices with interactive prompts.</p>
        <div class="card-tags">
          <span class="tag">Node.js</span>
          <span class="tag">Commander</span>
          <span class="tag">Inquirer</span>
        </div>
      </div>
      <div class="corruption-overlay">
        <span class="glitch-text">VIEW DETAILS</span>
      </div>
      <div class="corner-tl"></div><div class="corner-tr"></div>
      <div class="corner-bl"></div><div class="corner-br"></div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add projects CSS**

```css
.projects-grid {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 800px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}

.project-card.featured {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

@media (max-width: 600px) {
  .project-card.featured {
    grid-template-columns: 1fr;
  }
}

.project-card {
  background: var(--dark-purple);
  border: 1px solid var(--mid-purple);
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.project-card:hover {
  border-color: var(--magenta);
}

.card-frame-top {
  display: flex;
  gap: 2px;
}

.card-frame-top .scale {
  width: 8px;
  height: 8px;
  clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
}

.card-frame-top .scale:nth-child(odd) {
  background: var(--mid-purple);
}

.card-frame-top .scale:nth-child(even) {
  background: var(--bright-violet);
}

.card-body {
  padding: 16px;
}

.card-thumb {
  background: var(--void);
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--mid-purple);
  font-size: 0.7rem;
  border: 1px solid var(--mid-purple);
  margin-bottom: 12px;
}

.card-title {
  color: #fff;
  font-size: 0.9rem;
  margin-bottom: 6px;
}

.card-desc {
  font-size: 0.75rem;
  line-height: 1.5;
  margin-bottom: 10px;
  color: var(--text);
}

.card-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.tag {
  background: var(--mid-purple);
  color: var(--text);
  font-size: 0.6rem;
  padding: 2px 8px;
}

/* Corruption overlay on hover */
.corruption-overlay {
  position: absolute;
  inset: 0;
  background: rgba(13, 4, 21, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 5;
}

.project-card:hover .corruption-overlay {
  opacity: 1;
}

.glitch-text {
  color: var(--magenta);
  font-size: 0.8rem;
  letter-spacing: 4px;
}

/* Corruption blocks generated dynamically via JS on hover */
```

- [ ] **Step 3: Add corruption block JS in `script.js`**

```js
function setupCorruption() {
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      const overlay = card.querySelector('.corruption-overlay');
      // Remove old corruption blocks
      overlay.querySelectorAll('.corruption-block').forEach(b => b.remove());
      // Add new random corruption blocks
      const colors = ['#ff00ff', '#00ffff', '#39ff14'];
      for (let i = 0; i < 7; i++) {
        const block = document.createElement('div');
        block.className = 'corruption-block';
        const w = 3 + Math.random() * 5;
        const h = 2 + Math.random() * 4;
        block.style.cssText = `
          position: absolute;
          width: ${w}px; height: ${h}px;
          background: ${colors[Math.floor(Math.random() * colors.length)]};
          top: ${Math.random() * 100}%;
          left: ${Math.random() * 100}%;
          opacity: ${0.3 + Math.random() * 0.5};
          pointer-events: none;
        `;
        overlay.appendChild(block);
      }
    });
  });
}
```

---

### Task 5: Skills Section — Inventory grid layout

**Files:**
- Modify: `index.html` — fill `#skills` content
- Modify: `css/style.css` — skills styles

- [ ] **Step 1: Add skills HTML**

```html
<section id="skills">
  <h2 class="section-title">&gt; INVENTORY</h2>
  <div class="inventory-grid">
    <div class="item-card">
      <div class="item-icon">⚛</div>
      <div class="item-name">React</div>
      <div class="item-stat">LVL 8</div>
    </div>
    <div class="item-card">
      <div class="item-icon">🟢</div>
      <div class="item-name">Node.js</div>
      <div class="item-stat">LVL 7</div>
    </div>
    <div class="item-card">
      <div class="item-icon">🐘</div>
      <div class="item-name">Postgres</div>
      <div class="item-stat">LVL 6</div>
    </div>
    <div class="item-card">
      <div class="item-icon">#️⃣</div>
      <div class="item-name">TypeScript</div>
      <div class="item-stat">LVL 7</div>
    </div>
    <div class="item-card">
      <div class="item-icon">🎨</div>
      <div class="item-name">CSS/SCSS</div>
      <div class="item-stat">LVL 8</div>
    </div>
    <div class="item-card">
      <div class="item-icon">📦</div>
      <div class="item-name">Docker</div>
      <div class="item-stat">LVL 5</div>
    </div>
    <div class="item-card">
      <div class="item-icon">☁️</div>
      <div class="item-name">AWS</div>
      <div class="item-stat">LVL 5</div>
    </div>
    <div class="item-card">
      <div class="item-icon">🔷</div>
      <div class="item-name">Python</div>
      <div class="item-stat">LVL 6</div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add skills CSS**

```css
#skills {
  background: var(--void);
}

.inventory-grid {
  max-width: 700px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

@media (max-width: 600px) {
  .inventory-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.item-card {
  background: var(--dark-purple);
  border: 1px solid var(--mid-purple);
  padding: 20px 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.item-card:hover {
  border-color: var(--magenta);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2), 0 0 40px rgba(255, 0, 255, 0.1);
  transform: translateY(-2px);
}

.item-icon {
  font-size: 1.8rem;
  margin-bottom: 8px;
  filter: drop-shadow(0 0 6px var(--magenta));
}

.item-name {
  color: #fff;
  font-size: 0.8rem;
  letter-spacing: 2px;
}

.item-stat {
  color: var(--green);
  font-size: 0.65rem;
  margin-top: 4px;
  letter-spacing: 1px;
}
```

---

### Task 6: Contact Section — RPG dialogue, pixel form, submit button

**Files:**
- Modify: `index.html` — fill `#contact` content
- Modify: `css/style.css` — contact styles

- [ ] **Step 1: Add contact HTML**

```html
<section id="contact">
  <h2 class="section-title">&gt; FINAL GATE</h2>
  <div class="contact-dialogue">
    <p class="dialogue-line">
      <span class="dialogue-arrow">&gt;&gt;</span>
      The hero approaches the final gate...
    </p>
    <p class="dialogue-line">
      <span class="dialogue-arrow">&gt;&gt;</span>
      Leave your message to challenge the final boss.
    </p>
  </div>
  <form class="contact-form">
    <div class="pixel-input-group">
      <label class="input-label">NAME</label>
      <input type="text" class="pixel-input" placeholder="Your name">
    </div>
    <div class="pixel-input-group">
      <label class="input-label">EMAIL</label>
      <input type="email" class="pixel-input" placeholder="your@email.com">
    </div>
    <div class="pixel-input-group">
      <label class="input-label">MESSAGE</label>
      <textarea class="pixel-input pixel-textarea" placeholder="Your message..."></textarea>
    </div>
    <button type="submit" class="quest-btn">[ QUEST COMPLETE ]</button>
  </form>
</section>
```

- [ ] **Step 2: Add contact CSS**

```css
#contact {
  background: var(--dark-purple);
}

.contact-dialogue {
  max-width: 500px;
  margin: 0 auto 30px;
  background: var(--void);
  border: 2px solid var(--mid-purple);
  padding: 16px 20px;
}

.dialogue-line {
  font-size: 0.8rem;
  line-height: 1.8;
  color: var(--text);
}

.dialogue-line:last-child {
  color: var(--bright-violet);
}

.contact-form {
  max-width: 400px;
  margin: 0 auto;
}

.pixel-input-group {
  margin-bottom: 16px;
}

.input-label {
  display: block;
  color: var(--magenta);
  font-size: 0.65rem;
  letter-spacing: 3px;
  margin-bottom: 6px;
}

.pixel-input {
  width: 100%;
  background: var(--void);
  border: 1px solid var(--mid-purple);
  color: var(--text);
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  padding: 10px 12px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.pixel-input:focus {
  border-color: var(--magenta);
  box-shadow: 0 0 12px rgba(255, 0, 255, 0.3);
}

.pixel-input::placeholder {
  color: var(--mid-purple);
}

.pixel-textarea {
  resize: vertical;
  min-height: 100px;
}

.quest-btn {
  display: block;
  width: 100%;
  padding: 12px;
  background: transparent;
  border: 2px solid var(--magenta);
  color: var(--magenta);
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.quest-btn:hover {
  background: var(--magenta);
  color: var(--void);
  box-shadow: 0 0 30px rgba(255, 0, 255, 0.4);
}
```

---

### Task 7: Navigation and Scroll Progress — Nav tabs, XP bar, intersection observer

**Files:**
- Modify: `index.html` — fill `#nav` with nav links
- Modify: `css/style.css` — nav styles
- Modify: `js/script.js` — scroll progress, nav highlighting, section animations

- [ ] **Step 1: Add nav HTML**

```html
<nav id="nav">
  <a href="#hero" class="nav-link active">HOME</a>
  <a href="#about" class="nav-link">ABOUT</a>
  <a href="#projects" class="nav-link">WORK</a>
  <a href="#skills" class="nav-link">SKILLS</a>
  <a href="#contact" class="nav-link">CONTACT</a>
</nav>
```

- [ ] **Step 2: Add nav CSS**

```css
#nav {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  gap: 4px;
  background: rgba(13, 4, 21, 0.85);
  border: 1px solid var(--mid-purple);
  padding: 6px 10px;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  font-size: 0.65rem;
  letter-spacing: 2px;
  padding: 4px 10px;
  transition: color 0.3s, background 0.3s;
}

.nav-link:hover,
.nav-link.active {
  color: var(--magenta);
  background: rgba(255, 0, 255, 0.1);
}

@media (max-width: 500px) {
  #nav {
    top: 0;
    left: 0;
    right: 0;
    transform: none;
    border: none;
    border-bottom: 1px solid var(--mid-purple);
    justify-content: center;
    gap: 0;
  }

  .nav-link {
    font-size: 0.55rem;
    padding: 6px 6px;
  }
}
```

- [ ] **Step 3: Add JS for scroll progress + nav highlighting + section animation**

```js
function setupScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = progress + '%';
  });
}

function setupNavHighlight() {
  const links = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
        if (activeLink) activeLink.classList.add('active');
      }
    });
  }, { threshold: 0.5 });
  sections.forEach(s => observer.observe(s));
}

function setupSectionAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('section').forEach(s => observer.observe(s));
}
```

Add CSS for section entrance:
```css
section {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

section.visible {
  opacity: 1;
  transform: translateY(0);
}
```

Call all setup functions inside `DOMContentLoaded`.

---

### Task 8: Cursor and Glitch Polish — Custom cursor, hover glitch effects, final styling

**Files:**
- Modify: `css/style.css` — cursor, final polish
- Modify: `js/script.js` — cursor logic

- [ ] **Step 1: Add cursor CSS**

```css
.custom-cursor {
  width: 16px;
  height: 16px;
  border: 2px solid var(--magenta);
  position: fixed;
  pointer-events: none;
  z-index: 99999;
  transition: transform 0.1s;
}

.custom-cursor::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 4px;
  height: 4px;
  background: var(--cyan);
}

.custom-cursor.hovering {
  transform: scale(1.5);
  border-color: var(--green);
}
```

- [ ] **Step 2: Add cursor JS**

```js
function setupCursor() {
  const cursor = document.createElement('div');
  cursor.className = 'custom-cursor';
  document.body.appendChild(cursor);

  document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });

  document.querySelectorAll('a, button, .project-card, .item-card').forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
  });
}
```

- [ ] **Step 3: Final polish — ensure all sections have `#` IDs matching nav links and scroll progress bar is visible**

Verify `index.html` sections have correct IDs: `hero`, `about`, `projects`, `skills`, `contact`.

Verify `#scroll-progress` is present in `index.html`.

---

### Spec Coverage Check

| Spec Requirement | Task |
|-----------------|------|
| Hero — glitch text, stat bars, particles, scanlines | Task 2 |
| About — dialogue box, pixel avatar, stats panel | Task 3 |
| Projects — RPG frame cards, hover corruption, grid | Task 4 |
| Skills — inventory grid, glow hover | Task 5 |
| Contact — dialogue, pixel form, quest button | Task 6 |
| Navigation — RPG tabs, active highlighting | Task 7 |
| Scroll progress — XP bar | Task 7 |
| Section entrance animations | Task 7 |
| Custom pixel cursor | Task 8 |
| Responsive breakpoints | Included per section CSS |
