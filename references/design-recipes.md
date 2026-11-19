# Design recipes — proven SVG patterns for sellable shirts

All designs are authored as SVG at `viewBox="0 0 4500 5400"` (Printify's print-file
spec for tees: 4500x5400 px, transparent background), then rendered with
`scripts/render_design.py`. Keep artwork inside a ~300px margin on every side.

## Rules that keep designs sellable and safe

- ORIGINAL TEXT ONLY. No trademarks, brand names, celebrities, sports teams,
  song lyrics, or copyrighted characters — these get listings removed and shops
  suspended. Public-domain phrases are fine.
- Design for dark garments by default (cream `#F5EBDC` as the main ink) — most
  POD bestsellers ship on black/navy/pepper. If a design targets light shirts,
  invert the palette.
- 2-4 flat colors beat photo-style art: cheaper-looking mockups, crisper prints.
- Verify every render visually via the preview JPEG before publishing:
  look for text clipped at edges, textPath overflow (arc shorter than the text),
  and elements colliding. Fix and re-render — never publish unverified art.

## Fonts

Use fonts installed on the render machine (`fc-list | grep -i <name>`).
Proven combo: **Poppins** (700 bold display / 500 medium / 300 light italic)
and **Lora** (600 italic for script-ish accents). If missing, fetch OFL fonts
(e.g. from the google/fonts GitHub repo) into `~/.fonts` and run `fc-cache`.

## Pattern library (see scripts/example_designs.py for full working code)

### Arched headline (retro badge, varsity)
```xml
<path id="arch" d="M {cx-1750} 2150 A 1900 1900 0 0 1 {cx+1750} 2150" fill="none"/>
<text font-family="Poppins" font-weight="700" font-size="300" fill="#F5EBDC" letter-spacing="24">
  <textPath href="#arch" startOffset="50%" text-anchor="middle">YOUR TEXT HERE</textPath>
</text>
```
Sizing check: text length ≈ chars x 0.62 x font-size + letter-spacing x (chars-1).
Arc length ≈ 2r x asin(half_width / r). Keep text length < 80% of arc length.

### Circle badge scene (national-park style)
Clip a landscape (sky bands, sun, mountains as triangles, pine trees) inside a
`<clipPath><circle/></clipPath>`, ring it with a thick stroke circle plus a
dotted circle (`stroke-dasharray="4 70"`).

### Varsity club ("X CLUB — est. Y")
Arched all-caps word, huge second word in accent color with thin outline
(`stroke` + `stroke-width≈10`), "EST." line flanked by horizontal rules,
small italic tagline. This format converts extremely well for relatable niches.

### Wavy/groovy stacked words (retro 70s)
Two textPaths on gentle quadratic curves (`M 700 2150 Q 2250 1750 3800 2150`),
alternating warm retro colors (mustard #EAA933, dusty pink #E58F8F), scatter
paws/daisies/stars built from primitive shapes.

### Minimal icon + caption (introvert-battery style)
One big rounded-rect icon built from rects/circles, bold label above, lowercase
italic quip below. High contrast, reads across a room.

## Niches that keep working (rotate, don't repeat)

Role-based (dog mom, teacher, nurse), introvert/overthinker humor, coffee humor,
retro travel/outdoors, seasonal (Q4 holidays, graduation, Mother's/Father's Day).
Research current trends before each batch — search "trending Etsy t-shirt niches
<current month/year>" and pick 3 fresh angles.

## Pricing

Base $22.99-$24.99 (charm prices only: .99). Add $2-3 to 2XL/3XL variants
(their production cost is higher). Target ≥50% margin over the provider's base
cost. 13 tags per listing, every tag a multi-word buyer phrase.
