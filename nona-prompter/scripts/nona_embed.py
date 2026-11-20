#!/usr/bin/env python3
"""Nona board without Claude: build a single-file HTML, or pull data back out of one.

  python3 nona_embed.py build   <project folder>   # index.html + data.json -> <slug>.html (opens by double-click)
  python3 nona_embed.py extract <board.html> [<project folder>]   # downloaded HTML -> data.json (+ snaps/*.png)

The page reads data from <script type="application/json" id="nona-data">, so a file opened
straight from disk works without a server. Snapshots (microdrama) live in id="nona-snaps".
"""
import base64, json, pathlib, re, sys

SLOT = r'(<script type="application/json" id="{id}">)(.*?)(</script>)'


def read_slot(html, slot_id):
    m = re.search(SLOT.format(id=slot_id), html, re.S)
    return m.group(2).strip() if m else ""


def write_slot(html, slot_id, obj):
    body = json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")
    pat = re.compile(SLOT.format(id=slot_id), re.S)
    if not pat.search(html):
        raise SystemExit(f'no <script id="{slot_id}"> slot in the page — template is older than the standalone mode')
    return pat.sub(lambda m: m.group(1) + body + m.group(3), html, count=1)


def slug(title):
    s = re.sub(r"[^\w]+", "-", (title or "nona").lower(), flags=re.U).strip("-")
    return s or "nona"


def build(folder):
    folder = pathlib.Path(folder)
    html = (folder / "index.html").read_text(encoding="utf-8")
    data = json.loads((folder / "data.json").read_text(encoding="utf-8"))
    html = write_slot(html, "nona-data", data)
    if 'id="nona-snaps"' in html:
        snaps = {}
        for s in data.get("shots", []):
            p = folder / (s.get("snap") or "")
            if s.get("snap") and p.is_file():
                snaps[s["id"]] = "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
        html = write_slot(html, "nona-snaps", snaps)
    out = folder / (slug(data.get("title")) + ".html")
    out.write_text(html, encoding="utf-8")
    print(out)


def extract(page, folder=None):
    page = pathlib.Path(page)
    folder = pathlib.Path(folder) if folder else page.parent
    html = page.read_text(encoding="utf-8")
    raw = read_slot(html, "nona-data")
    if not raw:
        raise SystemExit("the page has no embedded data")
    data = json.loads(raw)
    folder.mkdir(parents=True, exist_ok=True)
    snaps = json.loads(read_slot(html, "nona-snaps") or "{}")
    for sid, url in snaps.items():
        if not url.startswith("data:image/png;base64,"):
            continue
        p = folder / "snaps" / f"{sid}.png"
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(base64.b64decode(url.split(",", 1)[1]))
        for s in data.get("shots", []):
            if s.get("id") == sid:
                s["snap"] = f"snaps/{sid}.png"
    (folder / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(folder / "data.json", f"({len(snaps)} snaps)" if snaps else "")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("build", "extract"):
        raise SystemExit(__doc__)
    (build if sys.argv[1] == "build" else extract)(*sys.argv[2:])
