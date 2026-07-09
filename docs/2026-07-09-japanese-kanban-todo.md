# Japanese Kanban Todo App — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-featured kanban-style todo app with Japanese Ukiyo-e aesthetic, showcasing CRUD operations, drag-and-drop, and localStorage persistence.

**Architecture:** SvelteKit app with a single runes-based TodoStore class for state management, `@horuse/svelte-dnd` for kanban drag-and-drop, and CSS variables matching the existing portfolio's Japanese theme.

**Tech Stack:** SvelteKit, Svelte 5 (runes), Vite, `@horuse/svelte-dnd`, localStorage

## Global Constraints

- SvelteKit project scaffold (not vanilla Vite)
- Svelte 5 runes (`$state`, `$derived`, `$effect`) — no legacy `let` reactivity
- CSS variables only — no Tailwind, no CSS-in-JS
- Fonts: Noto Serif JP + Zen Kaku Gothic New (Google Fonts)
- Palette: Linen `#f5f0e8`, Vermilion `#c41a1a`, Indigo `#1a2a3a`, Charcoal `#2c2c2c`, Matcha `#6b8f5e`, Gold `#c5a059`
- Borders: 4px solid charcoal
- Shadows: Offset `5px 5px 0`
- localStorage auto-save on every state change
- No TypeScript initially (plain JS)
- Mobile-responsive (breakpoints: 768px, 520px)

---

## File Structure

```
todo-app/
├── src/
│   ├── lib/
│   │   ├── stores/
│   │   │   └── todoStore.svelte.js       ← TodoStore class with runes
│   │   ├── components/
│   │   │   ├── Header.svelte             ← Title, search, view toggle
│   │   │   ├── Sidebar.svelte            ← Filters container
│   │   │   ├── CategoryFilter.svelte     ← Category checkboxes
│   │   │   ├── PriorityFilter.svelte     ← Priority checkboxes
│   │   │   ├── TagFilter.svelte          ← Tag chips
│   │   │   ├── ViewToggle.svelte         ← List/Board switch
│   │   │   ├── TaskList.svelte           ← List view container
│   │   │   ├── TaskRow.svelte            ← Single task row
│   │   │   ├── KanbanBoard.svelte        ← Board view container
│   │   │   ├── KanbanColumn.svelte       ← Single kanban column
│   │   │   ├── TaskCard.svelte           ← Draggable task card
│   │   │   ├── AddTaskForm.svelte        ← Create task form
│   │   │   ├── EditTaskModal.svelte      ← Edit task modal
│   │   │   └── Loader.svelte             ← Torii gate spinner
│   │   └── utils/
│   │       ├── storage.js                ← localStorage helpers
│   │       └── filters.js                ← Filter/search logic
│   ├── routes/
│   │   └── +page.svelte                  ← Main page (assembles all)
│   ├── app.html                          ← HTML shell
│   └── app.css                           ← Global styles, variables, fonts
├── static/
│   └── images/                           ← SVG patterns if needed
├── package.json
├── svelte.config.js
└── vite.config.js
```

---

## Tasks Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | Scaffold SvelteKit project | 10 min |
| 2 | Global styles & CSS variables | 15 min |
| 3 | TodoStore — data model & CRUD | 20 min |
| 4 | Header component | 15 min |
| 5 | Sidebar with filters | 25 min |
| 6 | Add task form | 15 min |
| 7 | Task row (list view) | 20 min |
| 8 | Kanban board view | 30 min |
| 9 | Loader component | 10 min |
| 10 | Edit task modal | 15 min |
| 11 | Final polish & responsive | 15 min |
| 12 | Deploy to GitHub Pages | 15 min |

**Total estimated time: ~3.5 hours**

---

## Execution Handoff

Plan complete. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
