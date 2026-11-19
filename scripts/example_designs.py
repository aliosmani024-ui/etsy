#!/usr/bin/env python3
"""Design Agent: generates print-ready t-shirt design SVGs -> 4500x5400 transparent PNGs."""
import os, subprocess, textwrap

W, H = 4500, 5400
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "designs")
os.makedirs(OUT, exist_ok=True)

CREAM = "#F5EBDC"; TERRA = "#E2725B"; RUST = "#B23A48"; PEACH = "#F2B880"
TEAL = "#4E8098"; DARKBROWN = "#2E2420"; MUSTARD = "#EAA933"; PINK = "#E58F8F"
COCOA = "#C89F7B"; GRAY = "#B9B9B9"; RED = "#E4572E"

def svg(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <style>
    .pb {{ font-family: "Poppins"; font-weight: 700; }}
    .pm {{ font-family: "Poppins"; font-weight: 500; }}
    .pl {{ font-family: "Poppins"; font-weight: 300; }}
    .li {{ font-family: "Lora"; font-style: italic; font-weight: 600; }}
  </style>
</defs>
{body}
</svg>'''

# ---------------- Design 1: Take The Scenic Route (retro park badge) ----------------
cx, cy, r = 2250, 2780, 1400
scene = f'''
<path id="archTop" d="M {cx-1720} {cy} A 1720 1720 0 0 1 {cx+1720} {cy}" fill="none"/>
<text class="pb" font-size="290" fill="{CREAM}" letter-spacing="26">
  <textPath href="#archTop" startOffset="50%" text-anchor="middle">TAKE THE SCENIC ROUTE</textPath>
</text>
<clipPath id="circ"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
<g clip-path="url(#circ)">
  <rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="900" fill="{CREAM}"/>
  <rect x="{cx-r}" y="{cy-r+900}" width="{2*r}" height="420" fill="{PEACH}"/>
  <rect x="{cx-r}" y="{cy-r+1320}" width="{2*r}" height="360" fill="{TERRA}"/>
  <rect x="{cx-r}" y="{cy-r+1680}" width="{2*r}" height="{2*r-1680}" fill="{RUST}"/>
  <circle cx="{cx}" cy="{cy-260}" r="430" fill="{MUSTARD}"/>
  <path d="M {cx-r} {cy+330} L {cx-800} {cy-560} L {cx-180} {cy+330} Z" fill="{TEAL}"/>
  <path d="M {cx-320} {cy+330} L {cx+340} {cy-760} L {cx+1020} {cy+330} Z" fill="{DARKBROWN}"/>
  <path d="M {cx+210} {cy-545} L {cx+340} {cy-760} L {cx+470} {cy-545} L {cx+380} {cy-545} L {cx+340} {cy-480} L {cx+300} {cy-545} Z" fill="{CREAM}"/>
  <path d="M {cx+520} {cy+330} L {cx+1120} {cy-360} L {cx+r} {cy+330} Z" fill="{TEAL}"/>
  <rect x="{cx-r}" y="{cy+330}" width="{2*r}" height="{r}" fill="{DARKBROWN}"/>
  <path d="M {cx-r} {cy+470} Q {cx} {cy+330} {cx+r} {cy+470} L {cx+r} {cy+r} L {cx-r} {cy+r} Z" fill="#241C19"/>
'''
# pine trees
for tx, ts in [(cx-1050, 1.0), (cx-820, .7), (cx+780, .9), (cx+1080, .65), (cx-90, .55)]:
    th = int(360*ts)
    scene += f'<path d="M {tx} {cy+430} l {int(-120*ts)} 0 l {int(120*ts)} {-th} l {int(120*ts)} {th} Z" fill="#1B2E23"/><rect x="{tx-int(18*ts)}" y="{cy+430}" width="{int(36*ts)}" height="{int(90*ts)}" fill="#141210"/>'
scene += f'''</g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CREAM}" stroke-width="70"/>
<circle cx="{cx}" cy="{cy}" r="{r+140}" fill="none" stroke="{CREAM}" stroke-width="16" stroke-dasharray="4 70" stroke-linecap="round"/>
<text class="pm" x="{cx}" y="{cy+r+540}" font-size="150" fill="{CREAM}" letter-spacing="26" text-anchor="middle">MOUNTAINS &#8226; FRESH AIR &#8226; GOOD VIBES</text>
'''
D1 = svg(scene)

# ---------------- Design 2: Social Battery Low ----------------
bw, bh, bx, by = 2600, 1150, (W-2600)//2, 2280
seg_w = (bw-160-100)//5
body2 = f'''
<text class="pb" x="{W/2}" y="1900" font-size="430" fill="{CREAM}" letter-spacing="40" text-anchor="middle">SOCIAL BATTERY</text>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="130" fill="none" stroke="{CREAM}" stroke-width="60"/>
<rect x="{bx+bw+40}" y="{by+bh/2-190}" width="150" height="380" rx="60" fill="{CREAM}"/>
<rect x="{bx+110}" y="{by+110}" width="{seg_w}" height="{bh-220}" rx="60" fill="{RED}"/>
'''
for i in range(1,5):
    body2 += f'<rect x="{bx+110+i*(seg_w+25)}" y="{by+110}" width="{seg_w}" height="{bh-220}" rx="60" fill="none" stroke="{GRAY}" stroke-width="14" stroke-dasharray="30 30" opacity="0.55"/>'
body2 += f'''
<text class="pl" x="{W/2}" y="4050" font-size="260" font-style="italic" fill="{GRAY}" letter-spacing="14" text-anchor="middle">please recharge later</text>
'''
D2 = svg(body2)

# ---------------- Design 3: Emotional Support Coffee ----------------
ccx = W/2
cup = f'''
<path id="arch3" d="M {ccx-1750} 2150 A 1900 1900 0 0 1 {ccx+1750} 2150" fill="none"/>
<text class="pb" font-size="300" fill="{CREAM}" letter-spacing="24">
  <textPath href="#arch3" startOffset="50%" text-anchor="middle">EMOTIONAL SUPPORT</textPath>
</text>
<g stroke="{CREAM}" stroke-width="48" stroke-linecap="round" fill="none">
  <path d="M {ccx-300} 2250 q -70 -140 30 -240 q 85 -85 25 -190" />
  <path d="M {ccx+30} 2210 q -70 -140 30 -240 q 85 -85 25 -190" />
  <path d="M {ccx+360} 2250 q -70 -140 30 -240 q 85 -85 25 -190" />
</g>
<g>
  <path d="M {ccx-560} 2620 L {ccx+560} 2620 L {ccx+470} 4000 L {ccx-470} 4000 Z" fill="{COCOA}" stroke="{CREAM}" stroke-width="46"/>
  <rect x="{ccx-640}" y="2450" width="1280" height="190" rx="70" fill="{CREAM}"/>
  <rect x="{ccx-520}" y="2320" width="1040" height="150" rx="60" fill="{COCOA}" stroke="{CREAM}" stroke-width="40"/>
  <path d="M {ccx-535} 2980 L {ccx+535} 2980 L {ccx+498} 3540 L {ccx-498} 3540 Z" fill="#8A6248" stroke="{CREAM}" stroke-width="42"/>
  <path d="M {ccx-330} 3210 q -80 -95 0 -172 q 77 -77 154 0 q 77 -77 154 0 q 80 77 0 172 l -154 150 Z" fill="{CREAM}" transform="translate(176,0)"/>
</g>
<text class="li" x="{ccx}" y="4700" font-size="640" fill="{CREAM}" text-anchor="middle">coffee</text>
'''
D3 = svg(cup)

# ---------------- Design 4: Dog Mama (retro groovy) ----------------
body4 = f'''
<path id="wave1" d="M 700 2150 Q 2250 1750 3800 2150" fill="none"/>
<path id="wave2" d="M 700 3450 Q 2250 3050 3800 3450" fill="none"/>
<text class="pb" font-size="1050" fill="{MUSTARD}" letter-spacing="60" stroke="{CREAM}" stroke-width="14">
  <textPath href="#wave1" startOffset="50%" text-anchor="middle">DOG</textPath>
</text>
<text class="pb" font-size="1050" fill="{PINK}" letter-spacing="10" stroke="{CREAM}" stroke-width="14">
  <textPath href="#wave2" startOffset="50%" text-anchor="middle">MAMA</textPath>
</text>
'''
def paw(px, py, s, col):
    p = f'<g fill="{col}" transform="translate({px},{py}) scale({s})">'
    p += '<ellipse cx="0" cy="55" rx="95" ry="80"/>'
    for ox, oy in [(-95,-45),(-33,-85),(33,-85),(95,-45)]:
        p += f'<circle cx="{ox}" cy="{oy}" r="36"/>'
    return p + '</g>'
def daisy(px, py, s):
    d = f'<g transform="translate({px},{py}) scale({s})">'
    for ang in range(0,360,45):
        d += f'<ellipse cx="0" cy="-70" rx="30" ry="62" fill="{CREAM}" transform="rotate({ang})"/>'
    return d + f'<circle r="42" fill="{MUSTARD}"/></g>'
body4 += paw(950, 3980, 1.6, MUSTARD) + paw(3560, 4000, 1.3, CREAM) + paw(2260, 4180, 1.9, PINK)
body4 += daisy(820, 1420, 1.5) + daisy(3700, 1350, 1.2) + daisy(2950, 4380, 1.0) + daisy(1500, 4470, 0.8)
D4 = svg(body4)

designs = {"scenic-route": D1, "social-battery": D2, "emotional-support-coffee": D3, "dog-mama": D4}
for name, content in designs.items():
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(content)
    png = os.path.join(OUT, name + ".png")
    subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                    "--default-background-color=00000000", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{p}"], capture_output=True)
    print(name, os.path.getsize(png)//1024, "KB")
