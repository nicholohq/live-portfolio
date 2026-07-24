# Kaze — Crypto Portfolio Tracker

> **Name:** Kaze (風, "wind" in Japanese) — wind drives the wave, wave shapes the portfolio

## Overview
A Japanese-themed crypto portfolio tracker with wallet integration, built with SvelteKit + TypeScript + Turso. Users connect their wallet or paste a public address to track holdings, view charts, and manage a watchlist.

## Goals
- Showcase Web3 skills (wallet connection, on-chain balance reading)
- Japanese design with Great Wave off Kanagawa motif
- Full-stack SvelteKit app with JWT auth and Turso persistence
- Deploy on Vercel

## Tech Stack
| Layer | Choice |
|-------|--------|
| Framework | SvelteKit + TypeScript |
| Styling | Tailwind CSS + custom design tokens |
| Charts | Lightweight Charts (TradingView) |
| Wallet | WalletConnect v2 + MetaMask |
| On-chain | Alchemy free tier (300M CU/month) |
| Prices | CoinGecko API (free, no key) |
| Database | Turso (libSQL) |
| Auth | JWT (bcrypt + jsonwebtoken) |
| Deploy | Vercel |

## Design Tokens
```css
:root {
  --wave-deep:    #1a2a3a;
  --wave-mid:     #2c4a6a;
  --wave-foam:    #e8f0f8;
  --wave-spray:   #f5f0e8;
  --vermilion:    #c41a1a;
  --gold:         #c5a059;
  --ink:          #1a1a1a;
  --matcha:       #6b8f5e;
  --crimson:      #dc3545;
}
```

## Pages
| Route | Purpose |
|-------|---------|
| `/` | Landing — Great Wave hero, CTA to connect wallet |
| `/dashboard` | Main app — portfolio overview, holdings, chart, market, watchlist |
| `/login` | Login/signup form |
| `/settings` | User preferences |

## Dashboard Sections
1. **Portfolio Overview** — total value, 24h change, total P&L, mini sparkline (7d)
2. **Holdings Table** — coins owned, amounts, current values, P&L per coin, sortable, expandable
3. **Portfolio Chart** — TradingView Lightweight Charts, timeframes: 1H, 1D, 1W, 1M, 3M, 1Y, ALL
4. **Market Rankings** — top 100 coins by market cap, search/filter
5. **Watchlist** — user-saved coins to track

## Database Schema
```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  wallet_address TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE holdings (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  coin_id TEXT NOT NULL,
  contract_address TEXT,
  amount REAL NOT NULL,
  purchase_price REAL,
  purchase_date INTEGER,
  source TEXT DEFAULT 'manual',
  created_at INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE watchlists (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  coin_id TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/login` | POST | Login |
| `/api/auth/signup` | POST | Create account |
| `/api/auth/logout` | POST | Clear session |
| `/api/auth/me` | GET | Current user |
| `/api/holdings` | GET | List user holdings |
| `/api/holdings` | POST | Add holding |
| `/api/holdings/[id]` | PATCH | Update holding |
| `/api/holdings/[id]` | DELETE | Remove holding |
| `/api/watchlist` | GET | List watchlist |
| `/api/watchlist` | POST | Add to watchlist |
| `/api/watchlist/[id]` | DELETE | Remove from watchlist |
| `/api/wallet/balances` | POST | Read on-chain balances via Alchemy |
| `/api/market/top` | GET | Top 100 coins from CoinGecko |
| `/api/market/[coinId]` | GET | Coin detail + price history |

## Component Structure
```
src/
├── lib/
│   ├── stores/
│   │   ├── auth.svelte.js
│   │   ├── portfolio.svelte.js
│   │   └── theme.svelte.js
│   ├── components/
│   │   ├── GreatWaveArt.svelte
│   │   ├── WalletConnect.svelte
│   │   ├── AddressInput.svelte
│   │   ├── PortfolioOverview.svelte
│   │   ├── HoldingsTable.svelte
│   │   ├── PortfolioChart.svelte
│   │   ├── MarketRankings.svelte
│   │   ├── Watchlist.svelte
│   │   └── Sparkline.svelte
│   └── server/
│       ├── db.ts
│       ├── auth.ts
│       ├── coingecko.ts
│       └── alchemy.ts
├── routes/
│   ├── +layout.svelte
│   ├── +page.svelte
│   ├── dashboard/+page.svelte
│   ├── login/+page.svelte
│   └── api/
│       ├── auth/
│       ├── holdings/
│       ├── watchlist/
│       ├── wallet/
│       └── market/
```

## Key Decisions
- Turso DB (not localStorage) for user accounts and cloud sync
- WalletConnect + MetaMask + manual address paste (no seed phrase import)
- Lightweight Charts for professional-grade charting
- All data persisted in Turso (watchlist, holdings, user prefs)
