# Shirt Factory — handoff for Claude Code

Ali's automated print-on-demand t-shirt business. Designs are generated as code,
listed on Ali's Etsy shop through Printify, and printed and shipped by Printify
when a customer orders. Ali is a beginner; explain things in plain language and
step by step.

## How it works

- **Pipeline** (full instructions in the `shirt-factory` skill, installed on Ali's account):
  research trending niches → write SVG designs (4500x5400, transparent) →
  `scripts/render_design.py` → **look at every preview JPEG before publishing** →
  listings in `listings/listings.json` → `scripts/publish_printify.py` → update
  `site/state.json` → `scripts/build_dashboard.py` → `site/agent-room.html`.
- **Agents** are role names in the dashboard: DENNIS (research), MATT (approval),
  BUNC (publishing). The dashboard is an animated pixel-art office with a War Room
  that lights up when `state.json` has `alert.active: true`.
- **Printify token**: in `.env` (gitignored, never commit it). If `.env` is missing,
  ask Ali to paste the token again, or regenerate it at Printify → Settings → Connections.
- **Daily automation**: a scheduled task, "Daily Etsy shirt drop — full auto", runs at
  9 AM Pacific. Its prompt carries the token and publishes 3 new shirts a day. It
  needs api.printify.com reachable too.

## Current status (2026-11-19, Claude Code)

- Printify works from Claude Code cloud sessions. Shop: **TheMajestyShop** (id 28245173).
- **5 shirts LIVE on Etsy** (published 2026-11-19, verified: each Printify product has
  an Etsy listing id): Overthinkers Club 4620818139, Take The Scenic Route 4620824240,
  Social Battery 4620824320, Emotional Support Coffee 4620818327, Dog Mama 4620824446.
- Do NOT re-run the publisher on listings/listings.json as-is: it would create duplicates.
  New drops need a fresh listings.json containing only the new shirts.
- Publishing is async: right after publish, products show is_locked=true; poll
  GET /v1/shops/28245173/products.json until is_locked=false and external.id is set.

## Setup gotchas (learned the hard way)

- `.env` is gitignored and is NOT in the repo. A fresh session needs the token again:
  ask Ali, or regenerate it at Printify → My profile → Connections.
- Fonts: install Poppins + Lora before rendering, or the designs fall back to a serif:
  download from github.com/google/fonts (ofl/poppins, ofl/lora) into ~/.fonts, then run `fc-cache -f`.
- Printify's firewall returns 403 to Python's default user-agent. The publisher sets one.
- `images.printify.com` (mockups) is blocked here; api.printify.com is fine.
- Shirts are dark colors only (Black, Navy, Dark Grey Heather, Forest, Maroon; override
  with SHIRT_COLORS) because every design uses light ink.
- Pricing: base $22.99–$24.99, 2XL +$4, 3XL +$6. Printify costs on 2026-11-19 were
  $11.29 (S–XL), $13.85 (2XL), $16.21 (3XL).

## Rules

- Original text only: no trademarks, brands, celebrities, lyrics or characters.
- Never claim a publish worked without checking. Never invent sales or revenue.
- Dashboard money figures stay $0.00 until real sales exist.
- Printify settings Ali chose: order routing ON (max +$3), submit orders 24h after
  received, default margin 55%, shipping profiles auto-match.
