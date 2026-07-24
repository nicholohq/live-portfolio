# Kaze — Crypto Portfolio Tracker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Japanese-themed crypto portfolio tracker with wallet integration, real-time prices from CoinGecko, on-chain balance reading via Alchemy, and cloud persistence via Turso DB with JWT auth.

**Architecture:** SvelteKit full-stack app. Server-side API routes handle Turso DB operations, CoinGecko data fetching, and Alchemy balance queries. Client-side stores (Svelte 5 runes) manage auth state and portfolio data. TradingView Lightweight Charts for visualization. Vercel deployment.

**Tech Stack:** SvelteKit 2 + TypeScript + Svelte 5 runes + Tailwind CSS + Turso (libSQL) + bcryptjs + jsonwebtoken + Lightweight Charts + ethers + Alchemy SDK

## Global Constraints
- All `.svelte` files use Svelte 5 runes syntax (`$state`, `$derived`, `$effect`, `$props`)
- All server code in `.ts` files (TypeScript)
- Follow todo-app conventions: JWT cookie auth, Turso via `@libsql/client`, `makeId()` for IDs
- Design tokens match Great Wave theme (deep ocean blues, foam white, vermilion accents)
- `getDb()` singleton pattern for Turso connection
- `hooks.server.ts` for session + auto-migration
- Vercel adapter for deployment
- `.env` files for secrets (TURSO_DB_URL, TURSO_AUTH_TOKEN, JWT_SECRET)

---

### Task 1: Project Scaffolding

**Files:**
- Create: `kaze/package.json`
- Create: `kaze/vite.config.ts`
- Create: `kaze/svelte.config.js`
- Create: `kaze/tsconfig.json`
- Create: `kaze/.gitignore`
- Create: `kaze/.env`
- Create: `kaze/src/app.html`
- Create: `kaze/src/app.css`
- Create: `kaze/src/lib/server/db.ts`
- Create: `kaze/src/lib/server/auth.ts`
- Create: `kaze/src/lib/server/migrate.ts`
- Create: `kaze/src/lib/server/id.ts`
- Create: `kaze/src/hooks.server.ts`

**Interfaces:**
- Consumes: nothing (first task)
- Produces: `getDb() → Client`, `hashPassword(pw) → string`, `verifyPassword(pw, hash) → bool`, `createToken(user) → string`, `verifyToken(token) → payload|null`, `makeId() → string`, `migrate() → Promise<void>`, hooks.server.ts with session + migration

- [ ] **Step 1: Create project directory and package.json**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio
mkdir kaze
```

```json
{
  "name": "kaze",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview",
    "prepare": "svelte-kit sync || echo ''"
  },
  "devDependencies": {
    "@libsql/client": "^0.17.4",
    "@sveltejs/adapter-vercel": "^6.3.4",
    "@sveltejs/kit": "^2.63.0",
    "@sveltejs/vite-plugin-svelte": "^7.1.2",
    "bcryptjs": "^3.0.3",
    "jsonwebtoken": "^9.0.3",
    "svelte": "^5.56.1",
    "vite": "^8.0.16",
    "typescript": "^5.8.0",
    "lightweight-charts": "^5.0.0"
  },
  "dependencies": {
    "alchemy-sdk": "^3.0.0",
    "ethers": "^6.0.0"
  }
}
```

- [ ] **Step 2: Create config files**

**vite.config.ts:**
```ts
import adapter from '@sveltejs/adapter-vercel';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    sveltekit({
      compilerOptions: {
        runes: ({ filename }) =>
          filename.split(/[/\\]/).includes('node_modules') ? undefined : true
      }
    })
  ]
});
```

**svelte.config.js:**
```js
import adapter from '@sveltejs/adapter-vercel';
export default { kit: { adapter: adapter() } };
```

**tsconfig.json:**
```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "module": "ESNext",
    "target": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "types": ["svelte"]
  }
}
```

**.gitignore:**
```
node_modules/
.env
.env.local
build/
.svelte-kit/
.vercel/
```

**.env:**
```
TURSO_DB_URL=libsql://kaze-nicholohq.aws-ap-northeast-1.turso.io
TURSO_AUTH_TOKEN=
JWT_SECRET=
```

- [ ] **Step 3: Create app.html**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌊</text></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    %sveltekit.head%
  </head>
  <body data-sveltekit-prerender="true">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
```

- [ ] **Step 4: Create app.css (design tokens)**

```css
:root {
  --wave-deep: #1a2a3a;
  --wave-mid: #2c4a6a;
  --wave-foam: #e8f0f8;
  --wave-spray: #f5f0e8;
  --vermilion: #c41a1a;
  --vermilion-2: #a01414;
  --gold: #c5a059;
  --ink: #1a1a1a;
  --matcha: #6b8f5e;
  --crimson: #dc3545;
  --paper: #ffffff;
  --charcoal: #2c2c2c;
  --linen: #f5f0e8;
  --linen-2: #ece4d6;
  --serif: 'Noto Serif JP', 'Times New Roman', serif;
  --gothic: 'Zen Kaku Gothic New', 'Segoe UI', system-ui, sans-serif;
  --s1: 4px;
  --s2: 8px;
  --s3: 16px;
  --s4: 24px;
  --s5: 32px;
  --s6: 48px;
  --border: 4px solid var(--charcoal);
  --border-thin: 2px solid var(--charcoal);
  --radius: 6px;
  --shadow: 5px 5px 0 var(--charcoal);
  --shadow-sm: 3px 3px 0 var(--charcoal);
  --focus-ring: 0 0 0 3px var(--gold);
  --ease: 0.18s ease;
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  background-color: var(--linen);
  color: var(--charcoal);
  font-family: var(--gothic);
  line-height: 1.6;
  min-height: 100vh;
  background-image: radial-gradient(circle at 1px 1px, rgba(26,42,58,0.05) 1px, transparent 0);
  background-size: 22px 22px;
}
h1, h2, h3, h4 { font-family: var(--serif); color: var(--charcoal); letter-spacing: 0.5px; line-height: 1.25; }
a { color: var(--vermilion); }
::selection { background: var(--vermilion); color: var(--linen); }
:focus-visible { outline: none; box-shadow: var(--focus-ring); border-radius: 2px; }

.btn {
  font-family: var(--gothic); font-weight: 700; font-size: 0.9rem;
  letter-spacing: 0.5px; color: var(--linen); background: var(--charcoal);
  border: var(--border-thin); border-radius: var(--radius);
  padding: var(--s2) var(--s4); cursor: pointer;
  display: inline-flex; align-items: center; gap: var(--s2);
  transition: transform var(--ease), box-shadow var(--ease), background var(--ease);
  box-shadow: var(--shadow-sm);
}
.btn:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--charcoal); }
.btn:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 var(--charcoal); }
.btn--primary { background: var(--vermilion); }
.btn--primary:active { background: var(--vermilion-2); }
.btn--ghost { background: transparent; color: var(--charcoal); box-shadow: none; }
.btn--ghost:hover { background: var(--linen-2); transform: none; box-shadow: none; }
.btn--sm { padding: var(--s1) var(--s2); font-size: 0.78rem; box-shadow: none; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.input {
  font-family: var(--gothic); font-size: 0.92rem; color: var(--charcoal);
  background: var(--paper); border: var(--border-thin); border-radius: var(--radius);
  padding: var(--s2) var(--s3); width: 100%;
}
.input::placeholder { color: #9a948a; }
.input:focus-visible { border-color: var(--vermilion); }

.panel {
  background: var(--paper);
  border: var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
}
```

- [ ] **Step 5: Create server utilities**

**src/lib/server/db.ts:**
```ts
import { createClient } from '@libsql/client';

let _db: ReturnType<typeof createClient>;

export function getDb() {
  if (!_db) {
    const url = process.env.TURSO_DB_URL;
    const authToken = process.env.TURSO_AUTH_TOKEN;
    if (!url) throw new Error('TURSO_DB_URL environment variable is required');
    _db = createClient({ url, authToken });
  }
  return _db;
}
```

**src/lib/server/auth.ts:**
```ts
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const TOKEN_EXPIRY = '7d';
const SALT_ROUNDS = 10;

function getSecret(): string {
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error('JWT_SECRET environment variable is required');
  return secret;
}

export function hashPassword(password: string): string {
  return bcrypt.hashSync(password, SALT_ROUNDS);
}

export function verifyPassword(password: string, hash: string): boolean {
  return bcrypt.compareSync(password, hash);
}

export function createToken(user: { id: string; username: string }): string {
  return jwt.sign({ userId: user.id, username: user.username }, getSecret(), { expiresIn: TOKEN_EXPIRY });
}

export function verifyToken(token: string): { userId: string; username: string } | null {
  try {
    return jwt.verify(token, getSecret()) as { userId: string; username: string };
  } catch {
    return null;
  }
}
```

**src/lib/server/id.ts:**
```ts
export function makeId(): string {
  return crypto.randomUUID();
}
```

**src/lib/server/migrate.ts:**
```ts
import { getDb } from './db.js';

const SCHEMA = `
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  wallet_address TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS holdings (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  coin_id TEXT NOT NULL,
  contract_address TEXT,
  amount REAL NOT NULL,
  purchase_price REAL,
  purchase_date INTEGER,
  source TEXT DEFAULT 'manual',
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS watchlists (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  coin_id TEXT NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_holdings_user ON holdings(user_id);
CREATE INDEX IF NOT EXISTS idx_watchlists_user ON watchlists(user_id);
`;

export async function migrate() {
  const db = getDb();
  await db.executeMultiple(SCHEMA);
}
```

**src/hooks.server.ts:**
```ts
import { migrate } from '$lib/server/migrate.js';
import { verifyToken } from '$lib/server/auth.js';

if (process.env.TURSO_DB_URL) {
  await migrate();
}

export function handle({ event, resolve }: { event: any; resolve: any }) {
  const token = event.cookies.get('session');
  if (token) {
    const payload = verifyToken(token);
    if (payload) {
      event.locals.user = { userId: payload.userId, username: payload.username };
    } else {
      event.cookies.delete('session', { path: '/' });
    }
  }
  return resolve(event);
}
```

- [ ] **Step 6: Install dependencies**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze
npm install
```

- [ ] **Step 7: Test that project boots**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze
npm run build
```

Expected: Build succeeds (app.html has `%sveltekit.body%` placeholder).

- [ ] **Step 8: Commit**

```bash
git add kaze/
git commit -m "kaze: scaffold SvelteKit + TypeScript project with Turso auth"
```

---

### Task 2: Auth API Routes + Login Page

**Files:**
- Create: `kaze/src/routes/api/auth/signup/+server.ts`
- Create: `kaze/src/routes/api/auth/login/+server.ts`
- Create: `kaze/src/routes/api/auth/logout/+server.ts`
- Create: `kaze/src/routes/api/auth/me/+server.ts`
- Create: `kaze/src/lib/stores/auth.svelte.ts`
- Create: `kaze/src/routes/login/+page.svelte`
- Modify: `kaze/src/routes/+layout.svelte`
- Create: `kaze/src/routes/+layout.ts`
- Create: `kaze/src/lib/stores/user.svelte.ts`
- Modify: `kaze/src/routes/+page.svelte` (placeholder redirect)

**Interfaces:**
- Consumes: `hashPassword`, `verifyPassword`, `createToken`, `verifyToken`, `getDb()`, `makeId()` from Task 1
- Produces: Auth API routes, `auth.svelte.ts` store with `login()`, `signup()`, `logout()`, `check()`, login page

- [ ] **Step 1: Create auth API routes**

**src/routes/api/auth/login/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';
import { verifyPassword, createToken } from '$lib/server/auth.js';

export async function POST({ cookies, request }: { cookies: any; request: Request }) {
  const { username, password } = await request.json();
  if (!username || !password) {
    return json({ error: 'Username and password are required.' }, { status: 400 });
  }
  const db = getDb();
  const result = await db.execute({
    sql: 'SELECT * FROM users WHERE username = ?',
    args: [username]
  });
  if (result.rows.length === 0) {
    return json({ error: 'Invalid username or password.' }, { status: 401 });
  }
  const user = result.rows[0] as any;
  if (!verifyPassword(password, user.password_hash)) {
    return json({ error: 'Invalid username or password.' }, { status: 401 });
  }
  const token = createToken({ id: user.id, username: user.username });
  cookies.set('session', token, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60 * 60 * 24 * 7 });
  return json({ id: user.id, username: user.username, walletAddress: user.wallet_address || null });
}
```

**src/routes/api/auth/signup/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';
import { hashPassword, createToken } from '$lib/server/auth.js';
import { makeId } from '$lib/server/id.js';

export async function POST({ cookies, request }: { cookies: any; request: Request }) {
  const { username, password } = await request.json();
  if (!username || !password) {
    return json({ error: 'Username and password are required.' }, { status: 400 });
  }
  if (username.length < 3) {
    return json({ error: 'Username must be at least 3 characters.' }, { status: 400 });
  }
  if (password.length < 6) {
    return json({ error: 'Password must be at least 6 characters.' }, { status: 400 });
  }
  const db = getDb();
  const existing = await db.execute({
    sql: 'SELECT id FROM users WHERE username = ?',
    args: [username]
  });
  if (existing.rows.length > 0) {
    return json({ error: 'Username already taken.' }, { status: 409 });
  }
  const id = makeId();
  const hash = hashPassword(password);
  const now = Date.now();
  await db.execute({
    sql: 'INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)',
    args: [id, username, hash, now]
  });
  const token = createToken({ id, username });
  cookies.set('session', token, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60 * 60 * 24 * 7 });
  return json({ id, username, walletAddress: null });
}
```

**src/routes/api/auth/logout/+server.ts:**
```ts
import { json } from '@sveltejs/kit';

export function POST({ cookies }: { cookies: any }) {
  cookies.delete('session', { path: '/' });
  return json({ ok: true });
}
```

**src/routes/api/auth/me/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';

export async function GET({ locals }: { locals: any }) {
  if (!locals.user) {
    return json(null, { status: 401 });
  }
  const db = getDb();
  const result = await db.execute({
    sql: 'SELECT id, username, wallet_address FROM users WHERE id = ?',
    args: [locals.user.userId]
  });
  if (result.rows.length === 0) {
    return json(null, { status: 401 });
  }
  const user = result.rows[0] as any;
  return json({ id: user.id, username: user.username, walletAddress: user.wallet_address || null });
}
```

- [ ] **Step 2: Create auth client store**

**src/lib/stores/auth.svelte.ts:**
```ts
class AuthStore {
  user = $state<{ id: string; username: string; walletAddress: string | null } | null>(null);
  loading = $state(true);

  async check() {
    try {
      const res = await fetch('/api/auth/me');
      if (res.ok) {
        this.user = await res.json();
      }
    } catch {
      this.user = null;
    } finally {
      this.loading = false;
    }
  }

  async login(username: string, password: string) {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.error || 'Login failed');
    }
    this.user = await res.json();
  }

  async signup(username: string, password: string) {
    const res = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.error || 'Signup failed');
    }
    this.user = await res.json();
  }

  async logout() {
    await fetch('/api/auth/logout', { method: 'POST' });
    this.user = null;
  }
}

export const auth = new AuthStore();
```

- [ ] **Step 3: Create layout files**

**src/routes/+layout.ts:**
```ts
export const ssr = false;
```

**src/routes/+layout.svelte:**
```svelte
<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth.svelte.js';

  let { children } = $props();

  onMount(() => {
    auth.check();
  });
</script>

{#if auth.loading}
  <div style="display:flex;align-items:center;justify-content:center;height:100vh;">
    <p>Loading...</p>
  </div>
{:else}
  {@render children()}
{/if}
```

- [ ] **Step 4: Create login page**

**src/routes/login/+page.svelte:**
```svelte
<script lang="ts">
  import { auth } from '$lib/stores/auth.svelte.js';
  import { goto } from '$app/navigation';

  let mode = $state<'login' | 'signup'>('login');
  let username = $state('');
  let password = $state('');
  let error = $state('');

  async function handleSubmit(e: Event) {
    e.preventDefault();
    error = '';
    try {
      if (mode === 'login') {
        await auth.login(username, password);
      } else {
        await auth.signup(username, password);
      }
      goto('/dashboard');
    } catch (err: any) {
      error = err.message;
    }
  }

  function toggleMode() {
    mode = mode === 'login' ? 'signup' : 'login';
    error = '';
  }
</script>

<div class="page">
  <div class="card panel">
    <div class="wave-icon">🌊</div>
    <h1>{mode === 'login' ? 'Sign In' : 'Create Account'}</h1>
    <p class="subtitle">Kaze — Crypto Portfolio Tracker</p>

    <form onsubmit={handleSubmit}>
      <div class="field">
        <label for="username">Username</label>
        <input id="username" class="input" bind:value={username} required minlength={3} />
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input id="password" type="password" class="input" bind:value={password} required minlength={6} />
      </div>
      {#if error}
        <p class="error">{error}</p>
      {/if}
      <button type="submit" class="btn btn--primary" style="width:100%;justify-content:center;">
        {mode === 'login' ? 'Sign In' : 'Create Account'}
      </button>
    </form>

    <p class="toggle">
      {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
      <button class="btn btn--ghost btn--sm" onclick={toggleMode}>
        {mode === 'login' ? 'Sign Up' : 'Sign In'}
      </button>
    </p>
  </div>
</div>

<style>
  .page { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: var(--s4); }
  .card { width: 100%; max-width: 400px; padding: var(--s5); text-align: center; }
  .wave-icon { font-size: 3rem; margin-bottom: var(--s3); }
  h1 { font-size: 1.5rem; margin-bottom: var(--s1); }
  .subtitle { font-size: 0.85rem; color: var(--wave-mid); margin-bottom: var(--s5); }
  form { display: flex; flex-direction: column; gap: var(--s3); text-align: left; }
  .field { display: flex; flex-direction: column; gap: var(--s1); }
  .field label { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px; color: var(--wave-mid); }
  .error { color: var(--crimson); font-size: 0.85rem; text-align: center; }
  .toggle { margin-top: var(--s4); font-size: 0.85rem; }
</style>
```

- [ ] **Step 5: Create placeholder root page**

**src/routes/+page.svelte:**
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth.svelte.js';
  import { goto } from '$app/navigation';

  onMount(() => {
    if (auth.user) {
      goto('/dashboard');
    } else {
      goto('/login');
    }
  });
</script>
```

- [ ] **Step 6: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

Expected: Build succeeds with no errors.

- [ ] **Step 7: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/routes/api/auth kaze/src/lib/stores/auth.svelte.ts kaze/src/routes/login kaze/src/routes/+layout.svelte kaze/src/routes/+layout.ts kaze/src/routes/+page.svelte
git commit -m "kaze: add auth API routes, store, and login page"
```

---

### Task 3: Market Data API (CoinGecko)

**Files:**
- Create: `kaze/src/lib/server/coingecko.ts`
- Create: `kaze/src/routes/api/market/top/+server.ts`
- Create: `kaze/src/routes/api/market/[coinId]/+server.ts`

**Interfaces:**
- Consumes: nothing server-side (API routes)
- Produces: `fetchTopCoins() → Coin[]`, `fetchCoinDetail(coinId) → CoinDetail`, API routes for /api/market/top and /api/market/[coinId]

- [ ] **Step 1: Create CoinGecko utility**

**src/lib/server/coingecko.ts:**
```ts
const BASE = 'https://api.coingecko.com/api/v3';

export interface CoinMarketData {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  market_cap: number;
  market_cap_rank: number;
  price_change_percentage_24h: number;
  price_change_percentage_7d_in_currency?: number;
  sparkline_in_7d?: { price: number[] };
}

export interface CoinDetail {
  id: string;
  symbol: string;
  name: string;
  image: { large: string };
  market_data: {
    current_price: { usd: number };
    market_cap: { usd: number };
    price_change_percentage_24h: number;
    price_change_percentage_7d: number;
    sparkline_7d?: { price: number[] };
  };
}

async function fetchJson(url: string) {
  const res = await fetch(url, {
    headers: { 'Accept': 'application/json' }
  });
  if (!res.ok) {
    throw new Error(`CoinGecko API error: ${res.status}`);
  }
  return res.json();
}

export async function fetchTopCoins(perPage: number = 100): Promise<CoinMarketData[]> {
  return fetchJson(
    `${BASE}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=${perPage}&page=1&sparkline=true&price_change_percentage=7d`
  ) as Promise<CoinMarketData[]>;
}

export async function fetchCoinDetail(coinId: string): Promise<CoinDetail> {
  return fetchJson(
    `${BASE}/coins/${coinId}?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=true`
  ) as Promise<CoinDetail>;
}

export async function fetchPriceHistory(coinId: string, days: number = 7): Promise<{ prices: [number, number][] }> {
  return fetchJson(
    `${BASE}/coins/${coinId}/market_chart?vs_currency=usd&days=${days}`
  ) as Promise<{ prices: [number, number][] }>;
}

export async function fetchSimplePrice(coinIds: string[]): Promise<Record<string, { usd: number; usd_24h_change?: number }>> {
  return fetchJson(
    `${BASE}/simple/price?ids=${coinIds.join(',')}&vs_currencies=usd&include_24hr_change=true`
  ) as Promise<Record<string, { usd: number; usd_24h_change?: number }>>;
}
```

- [ ] **Step 2: Create market API routes**

**src/routes/api/market/top/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { fetchTopCoins } from '$lib/server/coingecko.js';

export async function GET({ url }: { url: URL }) {
  const perPage = Math.min(Number(url.searchParams.get('per_page')) || 100, 250);
  try {
    const coins = await fetchTopCoins(perPage);
    return json(coins);
  } catch (err: any) {
    return json({ error: err.message }, { status: 502 });
  }
}
```

**src/routes/api/market/[coinId]/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { fetchCoinDetail, fetchPriceHistory } from '$lib/server/coingecko.js';

export async function GET({ params, url }: { params: { coinId: string }; url: URL }) {
  const days = Number(url.searchParams.get('days')) || 7;
  try {
    const [detail, history] = await Promise.all([
      fetchCoinDetail(params.coinId),
      fetchPriceHistory(params.coinId, days)
    ]);
    return json({ detail, history });
  } catch (err: any) {
    return json({ error: err.message }, { status: 502 });
  }
}
```

- [ ] **Step 3: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/lib/server/coingecko.ts kaze/src/routes/api/market
git commit -m "kaze: add CoinGecko market data API routes"
```

---

### Task 4: Holdings + Watchlist API CRUD

**Files:**
- Create: `kaze/src/routes/api/holdings/+server.ts`
- Create: `kaze/src/routes/api/holdings/[id]/+server.ts`
- Create: `kaze/src/routes/api/watchlist/+server.ts`
- Create: `kaze/src/routes/api/watchlist/[id]/+server.ts`

**Interfaces:**
- Consumes: `getDb()`, `makeId()` from Task 1, auth `locals.user` from hooks
- Produces: CRUD API endpoints for holdings and watchlist

- [ ] **Step 1: Create holdings API**

**src/routes/api/holdings/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';
import { makeId } from '$lib/server/id.js';

function rowToHolding(row: any) {
  return {
    id: row.id,
    userId: row.user_id,
    coinId: row.coin_id,
    contractAddress: row.contract_address || null,
    amount: row.amount,
    purchasePrice: row.purchase_price,
    purchaseDate: row.purchase_date || null,
    source: row.source,
    createdAt: row.created_at
  };
}

export async function GET({ locals }: { locals: any }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  const result = await db.execute({
    sql: 'SELECT * FROM holdings WHERE user_id = ? ORDER BY created_at DESC',
    args: [locals.user.userId]
  });
  return json(result.rows.map(rowToHolding));
}

export async function POST({ locals, request }: { locals: any; request: Request }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  const input = await request.json();
  if (!input.coinId || input.amount == null) {
    return json({ error: 'coinId and amount are required.' }, { status: 400 });
  }
  const id = makeId();
  const now = Date.now();
  await db.execute({
    sql: `INSERT INTO holdings (id, user_id, coin_id, contract_address, amount, purchase_price, purchase_date, source, created_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    args: [
      id, locals.user.userId, input.coinId, input.contractAddress || null,
      input.amount, input.purchasePrice || null, input.purchaseDate || null,
      input.source || 'manual', now
    ]
  });
  return json(rowToHolding({
    id, user_id: locals.user.userId, coin_id: input.coinId,
    contract_address: input.contractAddress || null, amount: input.amount,
    purchase_price: input.purchasePrice || null, purchase_date: input.purchaseDate || null,
    source: input.source || 'manual', created_at: now
  }), { status: 201 });
}
```

**src/routes/api/holdings/[id]/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';

export async function PATCH({ locals, params, request }: { locals: any; params: { id: string }; request: Request }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  const input = await request.json();
  const updates: string[] = [];
  const args: any[] = [];

  if (input.amount != null) { updates.push('amount = ?'); args.push(input.amount); }
  if (input.purchasePrice !== undefined) { updates.push('purchase_price = ?'); args.push(input.purchasePrice); }
  if (input.coinId) { updates.push('coin_id = ?'); args.push(input.coinId); }

  if (updates.length === 0) return json({ error: 'No fields to update.' }, { status: 400 });

  args.push(params.id, locals.user.userId);
  await db.execute({
    sql: `UPDATE holdings SET ${updates.join(', ')} WHERE id = ? AND user_id = ?`,
    args
  });
  return json({ ok: true });
}

export async function DELETE({ locals, params }: { locals: any; params: { id: string } }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  await db.execute({
    sql: 'DELETE FROM holdings WHERE id = ? AND user_id = ?',
    args: [params.id, locals.user.userId]
  });
  return json({ ok: true });
}
```

- [ ] **Step 2: Create watchlist API**

**src/routes/api/watchlist/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';
import { makeId } from '$lib/server/id.js';

export async function GET({ locals }: { locals: any }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  const result = await db.execute({
    sql: 'SELECT * FROM watchlists WHERE user_id = ? ORDER BY created_at DESC',
    args: [locals.user.userId]
  });
  return json(result.rows.map((row: any) => ({
    id: row.id, coinId: row.coin_id, createdAt: row.created_at
  })));
}

export async function POST({ locals, request }: { locals: any; request: Request }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  const { coinId } = await request.json();
  if (!coinId) return json({ error: 'coinId is required.' }, { status: 400 });
  const existing = await db.execute({
    sql: 'SELECT id FROM watchlists WHERE user_id = ? AND coin_id = ?',
    args: [locals.user.userId, coinId]
  });
  if (existing.rows.length > 0) return json({ error: 'Already in watchlist.' }, { status: 409 });
  const id = makeId();
  const now = Date.now();
  await db.execute({
    sql: 'INSERT INTO watchlists (id, user_id, coin_id, created_at) VALUES (?, ?, ?, ?)',
    args: [id, locals.user.userId, coinId, now]
  });
  return json({ id, coinId, createdAt: now }, { status: 201 });
}
```

**src/routes/api/watchlist/[id]/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getDb } from '$lib/server/db.js';

export async function DELETE({ locals, params }: { locals: any; params: { id: string } }) {
  if (!locals.user) return json({ error: 'Not authenticated.' }, { status: 401 });
  const db = getDb();
  await db.execute({
    sql: 'DELETE FROM watchlists WHERE id = ? AND user_id = ?',
    args: [params.id, locals.user.userId]
  });
  return json({ ok: true });
}
```

- [ ] **Step 3: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/routes/api/holdings kaze/src/routes/api/watchlist
git commit -m "kaze: add holdings and watchlist CRUD API"
```

---

### Task 5: Wallet Integration (Alchemy + ethers)

**Files:**
- Create: `kaze/src/lib/server/alchemy.ts`
- Create: `kaze/src/routes/api/wallet/balances/+server.ts`
- Create: `kaze/src/lib/components/WalletConnect.svelte`
- Create: `kaze/src/lib/components/AddressInput.svelte`

**Interfaces:**
- Consumes: `getDb()` from Task 1, auth `locals.user` from hooks
- Produces: Alchemy balance endpoint, wallet connection components

- [ ] **Step 1: Create Alchemy utility**

**src/lib/server/alchemy.ts:**
```ts
import { Alchemy, Network } from 'alchemy-sdk';

const API_KEY = process.env.ALCHEMY_API_KEY || 'demo';

export interface TokenBalance {
  contractAddress: string | null;
  symbol: string;
  name: string;
  logo: string | null;
  balance: string;
  decimals: number;
}

const settings = {
  apiKey: API_KEY,
  network: Network.ETH_MAINNET
};

export async function getEthBalance(address: string): Promise<string> {
  const alchemy = new Alchemy(settings);
  const balance = await alchemy.core.getBalance(address);
  return balance.toString();
}

export async function getTokenBalances(address: string): Promise<TokenBalance[]> {
  const alchemy = new Alchemy(settings);
  const balances = await alchemy.core.getTokenBalances(address);
  const tokens: TokenBalance[] = [];

  for (const token of balances.tokenBalances) {
    if (token.tokenBalance === '0') continue;
    try {
      const metadata = await alchemy.core.getTokenMetadata(token.contractAddress);
      tokens.push({
        contractAddress: token.contractAddress,
        symbol: metadata.symbol || 'UNKNOWN',
        name: metadata.name || 'Unknown Token',
        logo: metadata.logo || null,
        balance: token.tokenBalance,
        decimals: metadata.decimals || 18
      });
    } catch {
      // skip tokens we can't read metadata for
    }
  }
  return tokens;
}
```

- [ ] **Step 2: Create wallet balances API route**

**src/routes/api/wallet/balances/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { getEthBalance, getTokenBalances } from '$lib/server/alchemy.js';

export async function POST({ request }: { request: Request }) {
  const { address } = await request.json();
  if (!address || !/^0x[a-fA-F0-9]{40}$/.test(address)) {
    return json({ error: 'Invalid Ethereum address.' }, { status: 400 });
  }
  try {
    const [ethBalance, tokens] = await Promise.all([
      getEthBalance(address),
      getTokenBalances(address)
    ]);
    return json({ address, ethBalance, tokens });
  } catch (err: any) {
    return json({ error: err.message }, { status: 502 });
  }
}
```

- [ ] **Step 3: Create WalletConnect component**

**src/lib/components/WalletConnect.svelte:**
```svelte
<script lang="ts">
  let connecting = $state(false);
  let error = $state('');

  const emit = createEventDispatcher<{ connected: { address: string } }>();

  async function connectMetaMask() {
    connecting = true;
    error = '';
    try {
      const eth = (window as any).ethereum;
      if (!eth) {
        error = 'MetaMask is not installed. Please install MetaMask or paste your address manually.';
        return;
      }
      const accounts: string[] = await eth.request({ method: 'eth_requestAccounts' });
      if (accounts.length > 0) {
        emit('connected', { address: accounts[0] });
      }
    } catch (err: any) {
      error = err.message || 'Failed to connect wallet';
    } finally {
      connecting = false;
    }
  }
</script>

<div class="wallet-connect">
  <button class="btn btn--primary" onclick={connectMetaMask} disabled={connecting}>
    {connecting ? 'Connecting...' : 'Connect MetaMask'}
  </button>
  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

<style>
  .wallet-connect { display: flex; flex-direction: column; gap: var(--s2); align-items: center; }
  .error { color: var(--crimson); font-size: 0.82rem; text-align: center; }
</style>
```

- [ ] **Step 4: Create AddressInput component**

**src/lib/components/AddressInput.svelte:**
```svelte
<script lang="ts">
  let address = $state('');
  let error = $state('');

  const emit = createEventDispatcher<{ connected: { address: string } }>();

  function handleSubmit(e: Event) {
    e.preventDefault();
    error = '';
    const addr = address.trim();
    if (!/^0x[a-fA-F0-9]{40}$/.test(addr)) {
      error = 'Invalid Ethereum address (must be 0x followed by 40 hex characters)';
      return;
    }
    emit('connected', { address: addr });
  }
</script>

<form onsubmit={handleSubmit} class="address-input">
  <input
    class="input"
    placeholder="0x... paste Ethereum address"
    bind:value={address}
  />
  <button type="submit" class="btn">Import</button>
  {#if error}
    <p class="error">{error}</p>
  {/if}
</form>

<style>
  .address-input { display: flex; gap: var(--s2); flex-wrap: wrap; }
  .address-input .input { flex: 1; min-width: 200px; }
  .error { color: var(--crimson); font-size: 0.82rem; width: 100%; }
</style>
```

- [ ] **Step 5: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 6: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/lib/server/alchemy.ts kaze/src/routes/api/wallet kaze/src/lib/components/WalletConnect.svelte kaze/src/lib/components/AddressInput.svelte
git commit -m "kaze: add wallet integration (Alchemy + MetaMask)"
```

---

### Task 6: Dashboard Data Store

**Files:**
- Create: `kaze/src/lib/stores/portfolio.svelte.ts`

**Interfaces:**
- Consumes: Auth API routes (Task 2), Holdings + Watchlist API (Task 4), Market API (Task 3), Wallet API (Task 5)
- Produces: `portfolio` store with `holdings`, `watchlist`, `marketCoins`, `totalValue`, `totalChange24h`, `fetchAll()`, `addHolding()`, `removeHolding()`, `addToWatchlist()`, `removeFromWatchlist()`, `importWallet()`

- [ ] **Step 1: Create portfolio store**

```ts
// src/lib/stores/portfolio.svelte.ts
class PortfolioStore {
  holdings = $state<any[]>([]);
  watchlist = $state<any[]>([]);
  marketCoins = $state<any[]>([]);
  prices = $state<Record<string, { usd: number; usd_24h_change?: number }>>({});
  loading = $state(false);
  error = $state('');

  totalValue = $derived(
    this.holdings.reduce((sum, h) => {
      const price = this.prices[h.coinId]?.usd || 0;
      return sum + (h.amount || 0) * price;
    }, 0)
  );

  totalChange24h = $derived.by(() => {
    let total = 0;
    let previous = 0;
    for (const h of this.holdings) {
      const p = this.prices[h.coinId];
      if (p && p.usd_24h_change != null) {
        const prevPrice = p.usd / (1 + p.usd_24h_change / 100);
        total += h.amount * p.usd;
        previous += h.amount * prevPrice;
      }
    }
    return previous > 0 ? ((total - previous) / previous) * 100 : 0;
  });

  async fetchPrices(coinIds: string[]) {
    if (coinIds.length === 0) return;
    try {
      const res = await fetch(`/api/market/simple?ids=${coinIds.join(',')}`);
      if (res.ok) {
        this.prices = { ...this.prices, ...(await res.json()) };
      }
    } catch {}
  }

  async fetchHoldings() {
    try {
      const res = await fetch('/api/holdings');
      if (res.ok) {
        this.holdings = await res.json();
        if (this.holdings.length > 0) {
          await this.fetchPrices(this.holdings.map((h: any) => h.coinId));
        }
      }
    } catch {}
  }

  async fetchWatchlist() {
    try {
      const res = await fetch('/api/watchlist');
      if (res.ok) this.watchlist = await res.json();
    } catch {}
  }

  async fetchMarketCoins() {
    try {
      const res = await fetch('/api/market/top?per_page=100');
      if (res.ok) this.marketCoins = await res.json();
    } catch {}
  }

  async addHolding(data: { coinId: string; amount: number; purchasePrice?: number; source?: string }) {
    const res = await fetch('/api/holdings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error((await res.json()).error);
    const holding = await res.json();
    this.holdings = [holding, ...this.holdings];
    await this.fetchPrices([data.coinId]);
    return holding;
  }

  async removeHolding(id: string) {
    await fetch(`/api/holdings/${id}`, { method: 'DELETE' });
    this.holdings = this.holdings.filter((h: any) => h.id !== id);
  }

  async addToWatchlist(coinId: string) {
    const res = await fetch('/api/watchlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ coinId })
    });
    if (!res.ok) throw new Error((await res.json()).error);
    const entry = await res.json();
    this.watchlist = [entry, ...this.watchlist];
  }

  async removeFromWatchlist(id: string) {
    await fetch(`/api/watchlist/${id}`, { method: 'DELETE' });
    this.watchlist = this.watchlist.filter((w: any) => w.id !== id);
  }

  async importWallet(address: string) {
    this.loading = true;
    this.error = '';
    try {
      const res = await fetch('/api/wallet/balances', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address })
      });
      if (!res.ok) throw new Error((await res.json()).error);
      const data = await res.json();
      return data;
    } catch (err: any) {
      this.error = err.message;
      throw err;
    } finally {
      this.loading = false;
    }
  }

  async fetchAll() {
    this.loading = true;
    await Promise.all([
      this.fetchHoldings(),
      this.fetchWatchlist(),
      this.fetchMarketCoins()
    ]);
    this.loading = false;
  }

  /** Refresh prices every 60s */
  startPricePolling() {
    setInterval(() => {
      const coinIds = this.holdings.map((h: any) => h.coinId);
      if (coinIds.length > 0) this.fetchPrices(coinIds);
    }, 60_000);
  }
}

export const portfolio = new PortfolioStore();
```

- [ ] **Step 2: Update root page to redirect to dashboard for authenticated users**

Add a simple price route needed by portfolio:

**src/routes/api/market/simple/+server.ts:**
```ts
import { json } from '@sveltejs/kit';
import { fetchSimplePrice } from '$lib/server/coingecko.js';

export async function GET({ url }: { url: URL }) {
  const ids = url.searchParams.get('ids');
  if (!ids) return json({ error: 'ids parameter required' }, { status: 400 });
  try {
    const prices = await fetchSimplePrice(ids.split(','));
    return json(prices);
  } catch (err: any) {
    return json({ error: err.message }, { status: 502 });
  }
}
```

- [ ] **Step 3: Build**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/lib/stores/portfolio.svelte.ts kaze/src/routes/api/market/simple
git commit -m "kaze: add portfolio data store with price polling"
```

---

### Task 7: Dashboard Page

**Files:**
- Create: `kaze/src/routes/dashboard/+page.svelte`
- Create: `kaze/src/lib/components/PortfolioOverview.svelte`
- Create: `kaze/src/lib/components/HoldingsTable.svelte`
- Create: `kaze/src/lib/components/PortfolioChart.svelte`
- Create: `kaze/src/lib/components/MarketRankings.svelte`
- Create: `kaze/src/lib/components/Watchlist.svelte`
- Create: `kaze/src/lib/components/Sparkline.svelte`
- Create: `kaze/src/lib/components/GreatWaveArt.svelte`
- Create: `kaze/src/lib/components/Nav.svelte`

**Interfaces:**
- Consumes: `portfolio` store (Task 6), `auth` store (Task 2), `WalletConnect`, `AddressInput` (Task 5)
- Produces: Full dashboard page with all 5 sections, navigation

- [ ] **Step 1: Create navigation component**

**src/lib/components/Nav.svelte:**
```svelte
<script lang="ts">
  import { auth } from '$lib/stores/auth.svelte.js';
  import { goto } from '$app/navigation';

  function handleLogout() {
    auth.logout();
    goto('/login');
  }
</script>

<nav>
  <div class="nav-inner">
    <a href="/dashboard" class="brand">🌊 Kaze</a>
    <div class="nav-right">
      {#if auth.user}
        <span class="username">{auth.user.username}</span>
        <button class="btn btn--ghost btn--sm" onclick={handleLogout}>Logout</button>
      {:else}
        <a href="/login" class="btn btn--sm">Sign In</a>
      {/if}
    </div>
  </div>
</nav>

<style>
  nav { background: var(--wave-deep); color: var(--wave-foam); padding: var(--s2) var(--s4); }
  .nav-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
  .brand { font-family: var(--serif); font-size: 1.2rem; color: var(--wave-foam); text-decoration: none; }
  .nav-right { display: flex; align-items: center; gap: var(--s3); }
  .username { font-size: 0.85rem; opacity: 0.8; }
</style>
```

- [ ] **Step 2: Create GreatWaveArt SVG component**

**src/lib/components/GreatWaveArt.svelte:**
```svelte
<svg viewBox="0 0 800 200" preserveAspectRatio="xMidYMid meet" class="wave-banner">
  <defs>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="var(--wave-deep)" />
      <stop offset="50%" stop-color="var(--wave-mid)" />
      <stop offset="100%" stop-color="var(--wave-deep)" />
    </linearGradient>
  </defs>
  <path d="M0 160 Q50 80 100 120 Q150 160 200 100 Q250 40 300 90 Q350 140 400 80 Q450 20 500 70 Q550 120 600 60 Q650 0 700 50 Q750 100 800 60 L800 200 L0 200Z" fill="url(#waveGrad)" opacity="0.15" />
  <path d="M0 180 Q60 120 120 150 Q180 180 240 130 Q300 80 360 120 Q420 160 480 110 Q540 60 600 100 Q660 140 720 90 Q780 40 800 80 L800 200 L0 200Z" fill="url(#waveGrad)" opacity="0.25" />
</svg>

<style>
  .wave-banner { width: 100%; height: auto; display: block; }
</style>
```

- [ ] **Step 3: Create PortfolioOverview component**

**src/lib/components/PortfolioOverview.svelte:**
```svelte
<script lang="ts">
  import { portfolio } from '$lib/stores/portfolio.svelte.js';

  let formattedValue = $derived(
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })
      .format(portfolio.totalValue)
  );

  let changeClass = $derived(portfolio.totalChange24h >= 0 ? 'positive' : 'negative');
  let changeArrow = $derived(portfolio.totalChange24h >= 0 ? '▲' : '▼');
</script>

<div class="overview panel">
  <h2>Portfolio</h2>
  <div class="value">{formattedValue}</div>
  <div class="change {changeClass}">
    {changeArrow} {Math.abs(portfolio.totalChange24h).toFixed(2)}% (24h)
  </div>
  <div class="holdings-count">
    {portfolio.holdings.length} {portfolio.holdings.length === 1 ? 'asset' : 'assets'}
  </div>
</div>

<style>
  .overview { padding: var(--s4); text-align: center; }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); margin-bottom: var(--s2); }
  .value { font-family: var(--serif); font-size: 2.2rem; font-weight: 700; color: var(--ink); }
  .change { font-size: 1rem; font-weight: 700; margin-top: var(--s1); }
  .positive { color: var(--matcha); }
  .negative { color: var(--crimson); }
  .holdings-count { font-size: 0.82rem; color: var(--wave-mid); margin-top: var(--s2); }
</style>
```

- [ ] **Step 4: Create Sparkline component**

**src/lib/components/Sparkline.svelte:**
```svelte
<script lang="ts">
  let { data = [], width = 80, height = 24, color = 'var(--matcha)' }: {
    data?: number[];
    width?: number;
    height?: number;
    color?: string;
  } = $props();

  let path = $derived.by(() => {
    if (data.length < 2) return '';
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;
    const w = width - 2;
    const h = height - 2;
    return data.map((v, i) => {
      const x = 1 + (i / (data.length - 1)) * w;
      const y = 1 + ((max - v) / range) * h;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  });
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" class="sparkline">
  <path d={path} fill="none" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
</svg>

<style>
  .sparkline { display: inline-block; vertical-align: middle; }
</style>
```

- [ ] **Step 5: Create HoldingsTable component**

**src/lib/components/HoldingsTable.svelte:**
```svelte
<script lang="ts">
  import { portfolio } from '$lib/stores/portfolio.svelte.js';
  import { Sparkline } from './Sparkline.svelte';

  let search = $state('');

  let filtered = $derived.by(() => {
    if (!search) return portfolio.holdings;
    const q = search.toLowerCase();
    return portfolio.holdings.filter((h: any) => h.coinId.includes(q));
  });

  function getPrice(coinId: string) {
    return portfolio.prices[coinId]?.usd || 0;
  }

  function getChange(coinId: string) {
    return portfolio.prices[coinId]?.usd_24h_change;
  }

  let showAddForm = $state(false);
  let newCoinId = $state('');
  let newAmount = $state(0);
  let newPrice = $state(0);
  let addError = $state('');

  async function addHolding() {
    addError = '';
    try {
      await portfolio.addHolding({ coinId: newCoinId, amount: newAmount, purchasePrice: newPrice || undefined });
      showAddForm = false;
      newCoinId = '';
      newAmount = 0;
      newPrice = 0;
    } catch (err: any) {
      addError = err.message;
    }
  }

  async function confirmRemove(id: string) {
    if (confirm('Remove this holding?')) {
      await portfolio.removeHolding(id);
    }
  }
</script>

<div class="holdings panel">
  <div class="header">
    <h2>Holdings</h2>
    <button class="btn btn--sm btn--primary" onclick={() => showAddForm = !showAddForm}>
      {showAddForm ? 'Cancel' : '+ Add'}
    </button>
  </div>

  {#if showAddForm}
    <form onsubmit={addHolding} class="add-form">
      <input class="input" placeholder="Coin ID (e.g., bitcoin)" bind:value={newCoinId} required />
      <input class="input" type="number" step="any" placeholder="Amount" bind:value={newAmount} required />
      <input class="input" type="number" step="any" placeholder="Purchase price (USD)" bind:value={newPrice} />
      <button type="submit" class="btn btn--primary btn--sm">Save</button>
      {#if addError}<p class="error">{addError}</p>{/if}
    </form>
  {/if}

  {#if portfolio.holdings.length === 0}
    <p class="empty">No holdings yet. Add coins or import a wallet.</p>
  {:else}
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Coin</th>
            <th>Amount</th>
            <th>Price</th>
            <th>24h</th>
            <th>Value</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {#each filtered as h (h.id)}
            <tr>
              <td class="coin-name">{h.coinId}</td>
              <td>{h.amount}</td>
              <td>${getPrice(h.coinId).toFixed(2)}</td>
              <td class={getChange(h.coinId) >= 0 ? 'positive' : 'negative'}>
                {getChange(h.coinId)?.toFixed(2) ?? '--'}%
              </td>
              <td class="value-cell">${(h.amount * getPrice(h.coinId)).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
              <td><button class="btn btn--ghost btn--sm" onclick={() => confirmRemove(h.id)}>✕</button></td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .holdings { padding: var(--s4); }
  .header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--s3); }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); }
  .add-form { display: flex; gap: var(--s2); flex-wrap: wrap; margin-bottom: var(--s3); padding: var(--s3); background: var(--linen); border-radius: var(--radius); }
  .add-form .input { flex: 1; min-width: 120px; }
  .error { color: var(--crimson); font-size: 0.82rem; width: 100%; }
  .empty { color: var(--wave-mid); text-align: center; padding: var(--s5) 0; font-size: 0.9rem; }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  th { text-align: left; padding: var(--s1) var(--s2); border-bottom: var(--border-thin); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--wave-mid); }
  td { padding: var(--s2); border-bottom: 1px solid var(--linen-2); }
  .coin-name { font-weight: 700; }
  .positive { color: var(--matcha); }
  .negative { color: var(--crimson); }
  .value-cell { font-family: var(--serif); font-weight: 700; }
</style>
```

- [ ] **Step 6: Create PortfolioChart component**

**src/lib/components/PortfolioChart.svelte:**
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { createChart, type IChartApi, type ISeriesApi } from 'lightweight-charts';

  let chartContainer: HTMLDivElement;
  let chart: IChartApi;

  let timeframes = ['1D', '1W', '1M', '3M', '1Y', 'ALL'];
  let activeTF = $state('1W');

  interface DataPoint {
    time: string;
    value: number;
  }

  let series: ISeriesApi<'Line'>;
  let mockData: DataPoint[] = [];

  // Generate mock portfolio data based on timeframe
  $effect(() => {
    const days = activeTF === '1D' ? 1 : activeTF === '1W' ? 7 : activeTF === '1M' ? 30 : activeTF === '3M' ? 90 : activeTF === '1Y' ? 365 : 730;
    mockData = generateMockData(days);
    if (series) {
      series.setData(mockData);
    }
  });

  function generateMockData(days: number): DataPoint[] {
    const data: DataPoint[] = [];
    let val = 10000;
    const now = new Date();
    for (let i = days; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      val *= 1 + (Math.random() - 0.48) * 0.05;
      data.push({
        time: d.toISOString().split('T')[0],
        value: Math.round(val * 100) / 100
      });
    }
    return data;
  }

  function initChart() {
    chart = createChart(chartContainer, {
      width: chartContainer.clientWidth,
      height: 300,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#2c2c2c'
      },
      grid: {
        vertLines: { color: '#ece4d6' },
        horzLines: { color: '#ece4d6' }
      },
      crosshair: {
        vertLine: { color: '#c5a059', width: 1, style: 2 },
        horzLine: { color: '#c5a059', width: 1, style: 2 }
      },
      rightPriceScale: {
        borderColor: '#2c2c2c'
      },
      timeScale: {
        borderColor: '#2c2c2c',
        timeVisible: true
      }
    });

    series = chart.addLineSeries({
      color: '#1a2a3a',
      lineWidth: 2,
      crosshairMarkerVisible: true,
      priceFormat: { type: 'price', precision: 2, minMove: 0.01 }
    });

    series.setData(mockData);
    chart.timeScale().fitContent();

    // Resize observer
    const observer = new ResizeObserver(() => {
      chart.applyOptions({ width: chartContainer.clientWidth });
    });
    observer.observe(chartContainer);

    onMount(() => () => {
      observer.disconnect();
      chart.remove();
    });
  }

  onMount(() => {
    mockData = generateMockData(7);
    initChart();
  });
</script>

<div class="chart-section panel">
  <div class="header">
    <h2>Portfolio Value</h2>
    <div class="timeframes">
      {#each timeframes as tf}
        <button
          class="tf-btn"
          class:active={activeTF === tf}
          onclick={() => activeTF = tf}
        >{tf}</button>
      {/each}
    </div>
  </div>
  <div bind:this={chartContainer} class="chart-container"></div>
</div>

<style>
  .chart-section { padding: var(--s4); }
  .header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--s3); flex-wrap: wrap; gap: var(--s2); }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); }
  .timeframes { display: flex; gap: var(--s1); }
  .tf-btn { font-family: var(--gothic); font-size: 0.75rem; padding: 2px var(--s2); border: 2px solid var(--charcoal); border-radius: 4px; background: var(--paper); cursor: pointer; transition: background var(--ease); }
  .tf-btn.active { background: var(--wave-deep); color: var(--wave-foam); }
  .tf-btn:hover:not(.active) { background: var(--linen-2); }
  .chart-container { width: 100%; }
</style>
```

- [ ] **Step 7: Create MarketRankings component**

**src/lib/components/MarketRankings.svelte:**
```svelte
<script lang="ts">
  import { portfolio } from '$lib/stores/portfolio.svelte.js';
  import { Sparkline } from './Sparkline.svelte';

  let search = $state('');

  let filtered = $derived.by(() => {
    let coins = portfolio.marketCoins;
    if (search) {
      const q = search.toLowerCase();
      coins = coins.filter((c: any) => c.name.toLowerCase().includes(q) || c.symbol.toLowerCase().includes(q));
    }
    return coins;
  });
</script>

<div class="market panel">
  <div class="header">
    <h2>Market Rankings</h2>
    <input class="input" placeholder="Search coins..." bind:value={search} style="max-width:200px;" />
  </div>

  {#if portfolio.marketCoins.length === 0}
    <p class="empty">Loading market data...</p>
  {:else}
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Coin</th>
            <th>Price</th>
            <th>24h</th>
            <th>7d</th>
            <th>Market Cap</th>
          </tr>
        </thead>
        <tbody>
          {#each filtered as coin, i}
            <tr>
              <td class="rank">{coin.market_cap_rank || i + 1}</td>
              <td class="coin-cell">
                <img src={coin.image} alt={coin.name} width="20" height="20" />
                <span class="name">{coin.name}</span>
                <span class="symbol">{coin.symbol?.toUpperCase()}</span>
              </td>
              <td class="price">${coin.current_price?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}</td>
              <td class={coin.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}>
                {coin.price_change_percentage_24h?.toFixed(2)}%
              </td>
              <td>
                <Sparkline data={coin.sparkline_in_7d?.price} color={coin.price_change_percentage_7d_in_currency >= 0 ? 'var(--matcha)' : 'var(--crimson)'} />
              </td>
              <td class="mcap">${(coin.market_cap / 1e9).toFixed(2)}B</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .market { padding: var(--s4); }
  .header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--s3); flex-wrap: wrap; gap: var(--s2); }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); }
  .empty { color: var(--wave-mid); text-align: center; padding: var(--s5) 0; }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: var(--s1) var(--s2); border-bottom: var(--border-thin); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--wave-mid); }
  td { padding: var(--s2); border-bottom: 1px solid var(--linen-2); white-space: nowrap; }
  .rank { color: var(--wave-mid); font-size: 0.8rem; width: 30px; }
  .coin-cell { display: flex; align-items: center; gap: var(--s2); }
  .coin-cell img { border-radius: 50%; }
  .name { font-weight: 700; }
  .symbol { color: var(--wave-mid); font-size: 0.78rem; }
  .positive { color: var(--matcha); font-weight: 600; }
  .negative { color: var(--crimson); font-weight: 600; }
  .price { font-family: var(--serif); }
  .mcap { font-size: 0.82rem; color: var(--wave-mid); }
</style>
```

- [ ] **Step 8: Create Watchlist component**

**src/lib/components/Watchlist.svelte:**
```svelte
<script lang="ts">
  import { portfolio } from '$lib/stores/portfolio.svelte.js';

  let watchedCoins = $derived(
    portfolio.marketCoins.filter((c: any) => portfolio.watchlist.some((w: any) => w.coinId === c.id))
  );

  async function remove(coinId: string) {
    const entry = portfolio.watchlist.find((w: any) => w.coinId === coinId);
    if (entry) await portfolio.removeFromWatchlist(entry.id);
  }
</script>

<div class="watchlist panel">
  <h2>Watchlist</h2>
  {#if portfolio.watchlist.length === 0}
    <p class="empty">No coins watched yet. Add coins from the market rankings.</p>
  {:else}
    <div class="list">
      {#each watchedCoins as coin (coin.id)}
        <div class="item">
          <img src={coin.image} alt={coin.name} width="20" height="20" />
          <span class="name">{coin.name}</span>
          <span class="price">${coin.current_price?.toFixed(2)}</span>
          <span class={coin.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}>
            {coin.price_change_percentage_24h?.toFixed(2)}%
          </span>
          <button class="btn btn--ghost btn--sm" onclick={() => remove(coin.id)}>✕</button>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .watchlist { padding: var(--s4); }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); margin-bottom: var(--s3); }
  .empty { color: var(--wave-mid); text-align: center; padding: var(--s4) 0; font-size: 0.85rem; }
  .list { display: flex; flex-direction: column; gap: var(--s2); }
  .item { display: flex; align-items: center; gap: var(--s2); padding: var(--s1) 0; border-bottom: 1px solid var(--linen-2); font-size: 0.88rem; }
  .item img { border-radius: 50%; }
  .name { flex: 1; font-weight: 600; }
  .price { font-family: var(--serif); min-width: 70px; text-align: right; }
  .positive { color: var(--matcha); font-weight: 600; min-width: 60px; text-align: right; }
  .negative { color: var(--crimson); font-weight: 600; min-width: 60px; text-align: right; }
</style>
```

- [ ] **Step 9: Create dashboard page**

**src/routes/dashboard/+page.svelte:**
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth.svelte.js';
  import { portfolio } from '$lib/stores/portfolio.svelte.js';
  import { goto } from '$app/navigation';
  import Nav from '$lib/components/Nav.svelte';
  import GreatWaveArt from '$lib/components/GreatWaveArt.svelte';
  import WalletConnect from '$lib/components/WalletConnect.svelte';
  import AddressInput from '$lib/components/AddressInput.svelte';
  import PortfolioOverview from '$lib/components/PortfolioOverview.svelte';
  import HoldingsTable from '$lib/components/HoldingsTable.svelte';
  import PortfolioChart from '$lib/components/PortfolioChart.svelte';
  import MarketRankings from '$lib/components/MarketRankings.svelte';
  import Watchlist from '$lib/components/Watchlist.svelte';

  let showWalletImport = $state(false);

  onMount(() => {
    if (!auth.user && !auth.loading) {
      goto('/login');
      return;
    }
    portfolio.fetchAll();
    portfolio.startPricePolling();
  });

  function onWalletConnected(event: CustomEvent<{ address: string }>) {
    const { address } = event.detail;
    portfolio.importWallet(address);
    showWalletImport = false;
  }
</script>

<Nav />
<GreatWaveArt />

<main class="dashboard">
  <div class="top-bar">
    <h1>Dashboard</h1>
    <button class="btn btn--primary btn--sm" onclick={() => showWalletImport = !showWalletImport}>
      {showWalletImport ? 'Cancel' : '+ Import Wallet'}
    </button>
  </div>

  {#if showWalletImport}
    <div class="wallet-section panel">
      <h3>Import Wallet</h3>
      <p class="desc">Connect MetaMask or paste an Ethereum address to automatically import token holdings.</p>
      <WalletConnect on:connected={onWalletConnected} />
      <div class="divider"><span>or</span></div>
      <AddressInput on:connected={onWalletConnected} />
    </div>
  {/if}

  {#if portfolio.loading && portfolio.holdings.length === 0}
    <p class="loading-text">Loading portfolio data...</p>
  {:else}
    <div class="grid">
      <div class="grid-overview">
        <PortfolioOverview />
      </div>
      <div class="grid-chart">
        <PortfolioChart />
      </div>
      <div class="grid-main">
        <HoldingsTable />
      </div>
      <div class="grid-side">
        <Watchlist />
      </div>
      <div class="grid-full">
        <MarketRankings />
      </div>
    </div>
  {/if}
</main>

<style>
  .dashboard { max-width: 1200px; margin: 0 auto; padding: var(--s4); }
  .top-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--s4); }
  .top-bar h1 { font-size: 1.4rem; }
  .wallet-section { padding: var(--s4); margin-bottom: var(--s4); }
  .wallet-section h3 { margin-bottom: var(--s2); }
  .wallet-section .desc { font-size: 0.85rem; color: var(--wave-mid); margin-bottom: var(--s3); }
  .divider { display: flex; align-items: center; gap: var(--s2); margin: var(--s3) 0; color: var(--wave-mid); font-size: 0.82rem; }
  .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--linen-2); }
  .loading-text { text-align: center; padding: var(--s6); color: var(--wave-mid); }

  .grid {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: var(--s4);
  }
  .grid-overview { grid-column: 1; }
  .grid-chart { grid-column: 2; }
  .grid-main { grid-column: 1 / -1; }
  .grid-side { grid-column: 1 / -1; }
  .grid-full { grid-column: 1 / -1; }

  @media (min-width: 900px) {
    .grid { grid-template-columns: 300px 1fr; }
    .grid-overview { grid-column: 1; grid-row: 1; }
    .grid-chart { grid-column: 2; grid-row: 1; }
    .grid-main { grid-column: 1 / -1; }
    .grid-side { grid-column: 1 / -1; }
    .grid-full { grid-column: 1 / -1; }
  }
</style>
```

- [ ] **Step 10: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

Expected: Build succeeds. If any TypeScript errors occur (e.g., from lightweight-charts types), fix them.

- [ ] **Step 11: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/routes/dashboard kaze/src/lib/components
git commit -m "kaze: add dashboard page with all UI components"
```

---

### Task 8: Settings Page + Polish

**Files:**
- Create: `kaze/src/routes/settings/+page.svelte`
- Modify: `kaze/src/routes/dashboard/+page.svelte` (add link to settings)
- Modify: `kaze/src/lib/components/Nav.svelte` (add settings link)

**Interfaces:**
- Consumes: `auth` store (Task 2), `portfolio` store (Task 6)
- Produces: Settings page with user preferences and wallet management

- [ ] **Step 1: Create settings page**

```svelte
<!-- src/routes/settings/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth.svelte.js';
  import { portfolio } from '$lib/stores/portfolio.svelte.js';
  import { goto } from '$app/navigation';
  import Nav from '$lib/components/Nav.svelte';
  import GreatWaveArt from '$lib/components/GreatWaveArt.svelte';
  import WalletConnect from '$lib/components/WalletConnect.svelte';
  import AddressInput from '$lib/components/AddressInput.svelte';

  let currency = $state('usd');
  let walletAddress = $state('');

  onMount(() => {
    if (!auth.user) goto('/login');
    walletAddress = auth.user?.walletAddress || '';
  });

  function onWalletConnected(event: CustomEvent<{ address: string }>) {
    walletAddress = event.detail.address;
  }
</script>

<Nav />
<GreatWaveArt />

<main class="settings">
  <h1>Settings</h1>

  <div class="section panel">
    <h2>Account</h2>
    <p>Username: <strong>{auth.user?.username}</strong></p>
  </div>

  <div class="section panel">
    <h2>Wallet</h2>
    {#if walletAddress}
      <p class="address">Connected: <code>{walletAddress}</code></p>
    {:else}
      <p class="desc">Connect a wallet to auto-import token holdings.</p>
      <WalletConnect on:connected={onWalletConnected} />
      <div class="divider"><span>or</span></div>
      <AddressInput on:connected={onWalletConnected} />
    {/if}
  </div>

  <div class="section panel">
    <h2>Display</h2>
    <div class="field">
      <label for="currency">Currency</label>
      <select id="currency" class="input" bind:value={currency}>
        <option value="usd">USD</option>
        <option value="eur">EUR</option>
        <option value="gbp">GBP</option>
        <option value="jpy">JPY</option>
      </select>
    </div>
  </div>
</main>

<style>
  .settings { max-width: 600px; margin: 0 auto; padding: var(--s4); }
  h1 { font-size: 1.4rem; margin-bottom: var(--s4); }
  .section { padding: var(--s4); margin-bottom: var(--s4); }
  .section h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--wave-mid); margin-bottom: var(--s3); }
  .section .desc { font-size: 0.85rem; color: var(--wave-mid); margin-bottom: var(--s3); }
  .address { font-size: 0.85rem; }
  .address code { background: var(--linen-2); padding: 2px var(--s1); border-radius: 4px; word-break: break-all; font-size: 0.8rem; }
  .divider { display: flex; align-items: center; gap: var(--s2); margin: var(--s3) 0; color: var(--wave-mid); font-size: 0.82rem; }
  .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--linen-2); }
  .field { display: flex; flex-direction: column; gap: var(--s1); }
  .field label { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px; color: var(--wave-mid); }
</style>
```

- [ ] **Step 2: Update Nav to include settings link**

Add settings link to Nav.svelte:
```svelte
<a href="/settings" class="nav-link">Settings</a>
```

- [ ] **Step 3: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/routes/settings kaze/src/lib/components/Nav.svelte
git commit -m "kaze: add settings page with wallet management"
```

---

### Task 9: Landing Page (Hero)

**Files:**
- Modify: `kaze/src/routes/+page.svelte` (replace placeholder with full landing page)

**Interfaces:**
- Consumes: `auth` store (Task 2)
- Produces: Landing page with Great Wave hero, CTA buttons

- [ ] **Step 1: Create landing page**

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth.svelte.js';
  import { goto } from '$app/navigation';

  onMount(() => {
    if (auth.user) goto('/dashboard');
  });
</script>

<div class="landing">
  <!-- Wave background -->
  <div class="wave-bg">
    <svg viewBox="0 0 800 400" preserveAspectRatio="xMidYMid meet" class="hero-wave">
      <defs>
        <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="var(--wave-deep)" />
          <stop offset="50%" stop-color="var(--wave-mid)" />
          <stop offset="100%" stop-color="var(--wave-deep)" />
        </linearGradient>
      </defs>
      <path d="M0 250 Q50 150 100 200 Q150 250 200 180 Q250 110 300 170 Q350 230 400 160 Q450 90 500 150 Q550 210 600 130 Q650 50 700 110 Q750 170 800 120 L800 400 L0 400Z" fill="url(#heroGrad)" opacity="0.3" />
      <path d="M0 300 Q60 220 120 260 Q180 300 240 230 Q300 160 360 210 Q420 260 480 190 Q540 120 600 180 Q660 240 720 170 Q780 100 800 150 L800 400 L0 400Z" fill="url(#heroGrad)" opacity="0.2" />
      <path d="M0 350 Q80 280 160 310 Q240 340 320 270 Q400 200 480 250 Q560 300 640 220 Q720 140 800 190 L800 400 L0 400Z" fill="url(#heroGrad)" opacity="0.15" />
    </svg>
  </div>

  <div class="content">
    <div class="hero">
      <div class="wave-icon">🌊</div>
      <h1>Kaze</h1>
      <p class="tagline">Track your crypto portfolio with the<br/>power of the wind and the wave</p>
      <div class="cta-buttons">
        <a href="/login" class="btn btn--primary">Get Started</a>
        <a href="/login" class="btn btn--ghost">Sign In</a>
      </div>
    </div>

    <div class="features">
      <div class="feature panel">
        <span class="icon">👛</span>
        <h3>Wallet Import</h3>
        <p>Connect MetaMask or paste any Ethereum address to see your holdings instantly.</p>
      </div>
      <div class="feature panel">
        <span class="icon">📊</span>
        <h3>Live Prices</h3>
        <p>Real-time prices from CoinGecko with beautiful charts powered by TradingView.</p>
      </div>
      <div class="feature panel">
        <span class="icon">🌊</span>
        <h3>Japanese Design</h3>
        <p>Ukiyo-e inspired interface with the Great Wave off Kanagawa theme.</p>
      </div>
    </div>
  </div>
</div>

<style>
  .landing { position: relative; min-height: 100vh; overflow: hidden; }
  .wave-bg { position: absolute; inset: 0; z-index: 0; }
  .hero-wave { width: 100%; height: 100%; }
  .content { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: var(--s6) var(--s4); }
  .hero { text-align: center; padding: var(--s6) 0; }
  .wave-icon { font-size: 4rem; margin-bottom: var(--s3); }
  h1 { font-size: 3rem; color: var(--wave-deep); margin-bottom: var(--s2); }
  .tagline { font-size: 1.1rem; color: var(--wave-mid); margin-bottom: var(--s5); line-height: 1.6; }
  .cta-buttons { display: flex; gap: var(--s3); justify-content: center; }
  .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--s4); margin-top: var(--s6); }
  .feature { padding: var(--s5); text-align: center; }
  .feature .icon { font-size: 2.5rem; display: block; margin-bottom: var(--s3); }
  .feature h3 { font-size: 1.1rem; margin-bottom: var(--s2); }
  .feature p { font-size: 0.88rem; color: var(--wave-mid); line-height: 1.5; }
</style>
```

- [ ] **Step 2: Build and verify**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio\kaze && npm run build
```

- [ ] **Step 3: Commit**

```bash
cd C:\Users\nicholo\Documents\Clients\Portfolio && git add kaze/src/routes/+page.svelte
git commit -m "kaze: add landing page with Great Wave hero"
```
