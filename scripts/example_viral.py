#!/usr/bin/env python3
"""Viral drop: OVERTHINKERS CLUB — varsity arch, est. 3AM."""
import os, subprocess

W, H = 4500, 5400
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "designs")
CREAM = "#F5EBDC"; GOLD = "#EAA933"; DUSK = "#8FA6C9"

cx = W/2
body = f'''
<path id="archV" d="M {cx-1810} 2450 A 2050 2050 0 0 1 {cx+1810} 2450" fill="none"/>
<text font-family="Poppins" font-weight="700" font-size="360" fill="{CREAM}" letter-spacing="18">
  <textPath href="#archV" startOffset="50%" text-anchor="middle">OVERTHINKERS</textPath>
</text>
<text font-family="Poppins" font-weight="700" x="{cx}" y="3200" font-size="760" fill="{GOLD}" letter-spacing="80" text-anchor="middle" stroke="{CREAM}" stroke-width="10">CLUB</text>
<g transform="translate({cx},1650)">
  <path d="M 90 -170 A 205 205 0 1 0 90 170 A 165 165 0 1 1 90 -170 Z" fill="{CREAM}"/>
  <circle cx="-215" cy="-95" r="16" fill="{CREAM}"/><circle cx="-300" cy="30" r="11" fill="{CREAM}"/>
  <circle cx="-160" cy="115" r="9" fill="{CREAM}"/><circle cx="255" cy="-40" r="12" fill="{CREAM}"/>
  <circle cx="305" cy="90" r="8" fill="{CREAM}"/>
</g>
<g transform="translate({cx},3620)">
  <line x1="-1300" y1="0" x2="-640" y2="0" stroke="{CREAM}" stroke-width="14"/>
  <line x1="640" y1="0" x2="1300" y2="0" stroke="{CREAM}" stroke-width="14"/>
  <text font-family="Poppins" font-weight="500" x="0" y="52" font-size="150" fill="{CREAM}" letter-spacing="46" text-anchor="middle">EST. 3AM</text>
</g>
<text font-family="Poppins" font-weight="300" font-style="italic" x="{cx}" y="4080" font-size="140" fill="{DUSK}" letter-spacing="4" text-anchor="middle">meetings held nightly &#8226; attendance mandatory</text>
'''
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
p = os.path.join(OUT, "overthinkers-club.svg")
open(p, "w").write(svg)
png = os.path.join(OUT, "overthinkers-club.png")
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--default-background-color=00000000", f"--window-size={W},{H}",
                f"--screenshot={png}", f"file://{p}"], capture_output=True)
print(png, os.path.getsize(png)//1024, "KB")
