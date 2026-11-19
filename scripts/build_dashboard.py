#!/usr/bin/env python3
"""Builds the self-contained dashboard: injects state.json + design previews as data URLs."""
import base64, json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p):
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

tpl = open(os.path.join(ROOT, "site", "dashboard_template.html")).read()
state = json.load(open(os.path.join(ROOT, "site", "state.json")))
state["updated"] = int(time.time())

D = os.path.join(ROOT, "designs")
out = (tpl
    .replace("{{STATE}}", json.dumps(state))
    .replace("{{IMG_viral}}", b64(os.path.join(D, "preview_overthinkers-club.jpg")))
    .replace("{{IMG_scenic}}", b64(os.path.join(D, "preview_scenic-route.jpg")))
    .replace("{{IMG_battery}}", b64(os.path.join(D, "preview_social-battery.jpg")))
    .replace("{{IMG_coffee}}", b64(os.path.join(D, "preview_emotional-support-coffee.jpg")))
    .replace("{{IMG_dogmama}}", b64(os.path.join(D, "preview_dog-mama.jpg"))))

dest = os.path.join(ROOT, "site", "agent-room.html")
open(dest, "w").write(out)
print(dest, len(out)//1024, "KB")
