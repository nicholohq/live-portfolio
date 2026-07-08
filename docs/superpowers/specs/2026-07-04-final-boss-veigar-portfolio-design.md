# Final Boss Veigar Portfolio — Design Spec

## Overview

A single-page portfolio site for a web developer (websites and systems) themed after Final Boss Veigar from League of Legends. The site uses a corrupted dark wizard aesthetic with Dragon City-style ornate RPG UI framing. Purpose: job hunting, freelancing, and personal brand.

## Target Audience

- Potential employers
- Freelance clients
- General visitors

## Tech Stack

- HTML5 + CSS3
- Vanilla JavaScript (glitch animations, particles, scroll progress)
- No frameworks or build tools (single-page portfolio, no routing needed)

## Palette

| Role | Hex | Usage |
|------|-----|-------|
| Void black | `#0d0415` | Deepest backgrounds |
| Dark purple | `#1a0a2e` | Section backgrounds, cards |
| Mid purple | `#6c3483` | UI borders, scale pattern |
| Bright violet | `#8b5cf6` | Accents, hover states |
| Magenta | `#ff00ff` | Eyes, glows, CTAs, corruption |
| Cyan | `#00ffff` | Glitch accents, secondary glow |
| Neon green | `#39ff14` | Corruption, stat bars, XP |
| Faded lavender | `#c4b5fd` | Body text |

## Sections

### 1. Hero

- Full viewport height
- Background: `#0d0415`, floating pixel particles (4x4, 6x6 squares in magenta/cyan/green)
- Name in glitch text: RGB channel offset layers using CSS `clip-path` and `position: absolute`
- Title in pixel-border label: `border: 1px solid #6c3483`, monospace font
- RPG stat bars: HP ("Projects Done"), MP ("Tech Stack"), XP ("Experience") — each a 4px-tall bar with colored gradient fill over `#0d0415` background, bordered `#6c3483`
- Scanline overlay: `repeating-linear-gradient` with 2px transparent / 2px `rgba(255,255,255,0.015)`
- Ornate RPG frame border around viewport edge: dragon scale pattern (CSS `clip-path: polygon()` triangles in alternating `#6c3483` / `#8b5cf6`) along top/bottom, pixel corner flourishes

### 2. About

- Pixel art avatar placeholder (16-bit style portrait ~120x120px)
- Bio in RPG dialogue box: `#1a0a2e` background, pixel border, speaking-style intro text
- Stats panel: years of experience, languages, frameworks as RPG character stats (name + value pairs)
- Frame border around section

### 3. Projects

- Mix of featured case studies (wider cards) and project cards (grid)
- Each card in ornate RPG frame:
  - Dragon scale corner decorations (CSS clip-path triangles)
  - Pixel border top/bottom (small colored squares)
  - Tech tags as RPG badges (`#6c3483` bg, `#c4b5fd` text, monospace)
- Hover state: corruption overlay with glitch blocks (`#ff00ff`, `#00ffff`, `#39ff14`), RGB text shift
- Featured case studies get wider "boss battle" frame
- Responsive grid: 1-col mobile, 2-col tablet, 3-col desktop

### 4. Skills/Tech

- "Inventory" screen layout
- Tech items as RPG inventory cards with pixel art icons, stat descriptions
- Grid layout like game inventory
- Hover: glow effect on item card border

### 5. Contact

- RPG dialogue box: "The hero approaches the final gate..." text
- Form fields: pixel input boxes with `#ff00ff` glowing border on focus
- Submit button: "QUEST COMPLETE" text, magenta bg, hover glow
- Corrupted corner decorations

## Global Elements

- **Navigation:** Minimal RPG-style tabs along top, monospace font, pixel border indicators on active section
- **Scroll progress:** XP bar fixed at top that fills from 0% to 100% as user scrolls
- **Transitions:** CSS glitch effect on section enter/scroll (brief RGB shift, fade)
- **Cursor:** Optional custom pixel cursor (defer to later phase)

## Pixel Art Elements (CSS/JS only, no external images)

| Element | Implementation |
|---------|---------------|
| RPG frame borders | Nested div patterns or border-image |
| Dragon scale corners | CSS `clip-path: polygon()` alternating colors |
| Pixel particles | Absolutely positioned small divs with keyframe animation |
| Glitch text | CSS clip-path layers + hover RGB offset |
| Corruption blocks | Small colored divs with opacity, absolute positioned |
| Scanlines | repeating-linear-gradient overlay, pointer-events: none |
| Stat bars | Inner div percentage width, gradient fill |

## Responsive Breakpoints

- Mobile: Simplified frames, stacked layout, single-column project grid
- Tablet: 2-column project grid, partial frame ornamentation
- Desktop: Full RPG frame treatment, 3-column project grid

## Non-Goals (out of scope)

- No backend or database
- No contact form backend processing (static placeholder)
- No image assets to create — all pixel art is CSS/JS
- No multi-page routing
