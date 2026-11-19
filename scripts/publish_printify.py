#!/usr/bin/env python3
"""
BUNC — the Etsy Executor.
Uploads generated designs to Printify, creates t-shirt products, and publishes
them to your connected Etsy shop. This is the module that turns designs into
live listings (and therefore revenue).

SETUP (one time, ~15 minutes):
  1. Open an Etsy shop (etsy.com/sell) if you don't have one.
  2. Create a free Printify account (printify.com) and connect it to your
     Etsy shop:  Printify > Manage stores > Connect Etsy.
  3. Get an API token: Printify > My profile > Connections > API tokens.
  4. Run with:  PRINTIFY_TOKEN=xxxx python3 etsy_executor.py
     (or put PRINTIFY_TOKEN=xxxx in ~/etsy-agents/.env)

Safety rails:
  - DRY_RUN=1 (default) prints exactly what it WOULD do without posting.
    Set DRY_RUN=0 to post for real.
  - Publishes as DRAFT listings on Etsy by default (REVIEW_FIRST=1), so you
    approve each shirt before it goes live. Set REVIEW_FIRST=0 for full auto.
  - Etsy charges $0.20 per published listing. 4 designs = $0.80.
"""
import json, os, sys, time, base64, urllib.request

BASE = "https://api.printify.com/v1"
# Work from the project directory (where listings/ and designs/ live), not the
# skill folder: prefer CWD, fall back to the script's parent.
_CAND = [os.getcwd(), os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
ROOT = next((c for c in _CAND if os.path.exists(os.path.join(c, "listings", "listings.json"))), _CAND[0])

# Bella+Canvas 3001 via a large US print provider; swap blueprint/provider if desired.
BLUEPRINT_ID = 12        # Unisex Jersey Short Sleeve Tee (Bella+Canvas 3001)
PRINT_PROVIDER_ID = 99   # Printify Choice (auto-routes to a good provider)

def env(name, default=None):
    # A value set on the command line always wins over .env, so
    # `DRY_RUN=1 python3 publish_printify.py` is a real rehearsal.
    if name in os.environ:
        return os.environ[name]
    if os.path.exists(os.path.join(ROOT, ".env")):
        for line in open(os.path.join(ROOT, ".env")):
            if line.strip().startswith(name + "="):
                return line.strip().split("=", 1)[1]
    return default

TOKEN = env("PRINTIFY_TOKEN")
DRY_RUN = env("DRY_RUN", "1") != "0"
REVIEW_FIRST = env("REVIEW_FIRST", "1") != "0"

def api(method, path, payload=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    # Printify's firewall rejects Python's default user-agent with a 403.
    req.add_header("User-Agent", "shirt-factory/1.0")
    data = json.dumps(payload).encode() if payload is not None else None
    with urllib.request.urlopen(req, data) as r:
        return json.loads(r.read().decode())

def log_event(kind, message):
    state_path = os.path.join(ROOT, "site", "state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {"events": []}
    state.setdefault("events", []).insert(0, {"ts": int(time.time()), "kind": kind, "message": message})
    json.dump(state, open(state_path, "w"), indent=2)

def main():
    lp = os.path.join(ROOT, "listings", "listings.json")
    if not os.path.exists(lp):
        print(f"No listings file at {lp} — create it first (see assets/listings.example.json in the skill).")
        sys.exit(1)
    listings = json.load(open(lp))["listings"]

    if not TOKEN:
        print("PRINTIFY_TOKEN is not set. Running in PLAN mode.\n")
        print("Once your Etsy shop + Printify are connected and the token is in")
        print("~/etsy-agents/.env, this script will do the following for real:\n")
        for l in listings:
            print(f"  -> upload {l['design_file']}")
            print(f"     create '{l['title'][:60]}...' at ${l['price_usd']}")
            print(f"     publish to Etsy as {'DRAFT' if REVIEW_FIRST else 'LIVE'} listing\n")
        log_event("blocked", "etsy executor waiting for PRINTIFY_TOKEN — listings ready to post")
        sys.exit(0)

    shops = api("GET", "/shops.json")
    etsy = next((s for s in shops if s.get("sales_channel", "").lower() == "etsy"), None)
    if not etsy:
        print("No Etsy shop connected to this Printify account yet.")
        print("Connect it at Printify > Manage stores > Connect Etsy, then re-run.")
        log_event("failed", "printify account has no connected etsy shop")
        sys.exit(1)
    shop_id = etsy["id"]
    print(f"Connected Etsy shop: {etsy.get('title')} (id {shop_id})")

    # pick a valid print provider for the blueprint (fall back to first available)
    global PRINT_PROVIDER_ID
    try:
        providers = api("GET", f"/catalog/blueprints/{BLUEPRINT_ID}/print_providers.json")
        ids = [p["id"] for p in providers]
        if PRINT_PROVIDER_ID not in ids and ids:
            PRINT_PROVIDER_ID = ids[0]
            print(f"provider 99 unavailable; using provider {PRINT_PROVIDER_ID} ({providers[0].get('title')})")
    except Exception as e:
        print("provider lookup failed, keeping default:", e)

    # variants: fetch available variants for blueprint/provider, enable S-3XL dark colors
    variants = api("GET", f"/catalog/blueprints/{BLUEPRINT_ID}/print_providers/{PRINT_PROVIDER_ID}/variants.json")["variants"]
    wanted_sizes = {"S", "M", "L", "XL", "2XL", "3XL"}
    # The designs use cream/light ink, so only offer dark shirt colors.
    dark_colors = [c.strip() for c in env("SHIRT_COLORS", "Black,Navy,Dark Grey Heather,Forest,Maroon").split(",")]
    chosen = [v for v in variants
              if v["options"].get("size") in wanted_sizes and v["options"].get("color") in dark_colors]
    missing = set(dark_colors) - {v["options"]["color"] for v in chosen}
    if missing:
        print("note: colors not offered by this provider:", ", ".join(sorted(missing)))
    print(f"{len(chosen)} variants: {', '.join(c for c in dark_colors if c not in missing)} x S-3XL")
    upcharge = {"2XL": 400, "3XL": 600}  # cents added to the base listing price

    for l in listings:
        design_path = os.path.join(ROOT, l["design_file"])
        name = os.path.basename(design_path)
        print(f"\n=== {name} ===")
        if DRY_RUN:
            print(f"[dry-run] would upload {name}, create product '{l['title'][:50]}...', publish {'draft' if REVIEW_FIRST else 'live'}")
            continue

        b64 = base64.b64encode(open(design_path, "rb").read()).decode()
        up = api("POST", "/uploads/images.json", {"file_name": name, "contents": b64})
        print(f"uploaded image id {up['id']}")

        price_cents = int(round(l["price_usd"] * 100))
        product = api("POST", f"/shops/{shop_id}/products.json", {
            "title": l["title"][:140],
            "description": l["description"],
            "tags": l["tags"][:13],
            "blueprint_id": BLUEPRINT_ID,
            "print_provider_id": PRINT_PROVIDER_ID,
            "variants": [{"id": v["id"], "price": price_cents + upcharge.get(v["options"]["size"], 0),
                          "is_enabled": True} for v in chosen],
            "print_areas": [{
                "variant_ids": [v["id"] for v in chosen],
                "placeholders": [{"position": "front", "images": [
                    {"id": up["id"], "x": 0.5, "y": 0.5, "scale": 0.95, "angle": 0}]}]
            }]
        })
        print(f"created product {product['id']}")
        costs = [(pv["price"] - pv["cost"]) / pv["price"] for pv in product.get("variants", [])
                 if pv.get("is_enabled") and pv.get("cost")]
        if costs:
            print(f"margin before Etsy fees: {min(costs):.0%} (worst size) to {max(costs):.0%}")
        if env("CREATE_ONLY", "0") == "1":
            print("CREATE_ONLY=1: product created in Printify but NOT published to Etsy")
            continue

        api("POST", f"/shops/{shop_id}/products/{product['id']}/publish.json", {
            "title": True, "description": True, "images": True,
            "variants": True, "tags": True,
            "shipping_template": True, "key_features": True
        })
        state = "draft (review in Etsy)" if REVIEW_FIRST else "live"
        print(f"published to Etsy: {state}")
        log_event("posted", f"published '{l['title'][:40]}...' to etsy ({state})")
        time.sleep(2)

    print("\nDone. Check Etsy > Shop Manager > Listings.")

if __name__ == "__main__":
    main()
