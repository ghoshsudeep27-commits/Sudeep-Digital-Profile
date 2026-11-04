#!/usr/bin/env python3
"""Rebuild stories/stories.json from the media files in stories/.

Run by .github/workflows/stories.yml whenever something is pushed into
stories/, so dropping an image into that folder is all it takes.

Filename rules (the same ones the old client-side code used):
    Happy-Diwali.webp                        -> visible all the time
    2026-11-01--2026-11-14--Happy-Diwali.webp -> visible between those dates

Existing entries are preserved: if an entry already points at the same file,
its id, headline, message and signature are kept and only the dates are
refreshed from the filename. Entries with no "src" (text-only greetings with an
emoji) are never touched. Delete a file and its entry disappears.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORIES_DIR = os.path.join(ROOT, "stories")
JSON_PATH = os.path.join(STORIES_DIR, "stories.json")

MEDIA = re.compile(r"\.(jpe?g|png|webp|gif|avif|mp4|webm|mov|m4v)$", re.I)
VIDEO = re.compile(r"\.(mp4|webm|mov|m4v)$", re.I)
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:--(\d{4}-\d{2}-\d{2}))?--(.+)$")
THEME = ["#38c8c8", "#d4a73a"]


def load_existing():
    try:
        with open(JSON_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, ValueError):
        return []
    if isinstance(data, dict):
        return data.get("stories") or []
    return data if isinstance(data, list) else []


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "story"


def main():
    old = load_existing()
    by_src = {e.get("src"): e for e in old if e.get("src")}

    entries = []
    for name in sorted(os.listdir(STORIES_DIR)):
        if name == "stories.json" or not MEDIA.search(name):
            continue
        src = "stories/" + name
        base = os.path.splitext(name)[0]
        match = DATED.match(base)
        if match:
            date_from, date_until, title = match.group(1), match.group(2) or match.group(1), match.group(3)
        else:
            date_from, date_until, title = "", "", base
        title = re.sub(r"[-_]+", " ", title).strip()

        entry = dict(by_src.get(src) or {})
        entry.setdefault("id", slug(title or base))
        entry["type"] = "video" if VIDEO.search(name) else "image"
        entry["src"] = src
        entry.setdefault("greet", title)
        entry.setdefault("msg", "")
        entry.setdefault("sign", "\u2014 Sudeep")
        entry.setdefault("theme", THEME)
        if date_from:
            entry["from"], entry["until"] = date_from, date_until
        entries.append(entry)

    # keep hand-written, text-only greetings (no src) and anything not regenerated
    generated_ids = {e["id"] for e in entries}
    for entry in old:
        if entry.get("src") or entry.get("id") in generated_ids:
            continue
        entries.append(entry)

    entries.sort(key=lambda e: (e.get("from") or "9999-99-99", e.get("id") or ""))

    with open(JSON_PATH, "w", encoding="utf-8") as fh:
        json.dump({"stories": entries}, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("stories.json: %d %s" % (len(entries), "entry" if len(entries) == 1 else "entries"))
    for entry in entries:
        print("  - %-24s %-5s %s" % (entry.get("id"), entry.get("type"),
                                     (entry.get("from") or "(always)") + " .. " + (entry.get("until") or "")))


if __name__ == "__main__":
    main()
