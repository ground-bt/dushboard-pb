#!/usr/bin/env python3
"""Copy the HTML files listed in _site/catalog.json from OneDrive into this repo.

Usage (from the repo root, on the company PC):
    python _site/sync_from_onedrive.py [path-to-OneDrive]
Default OneDrive root: %USERPROFILE%/OneDrive (Windows) or ~/OneDrive.
Then run  python _site/build_index.py  and commit.
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), "OneDrive")
cat = json.load(open(os.path.join(ROOT, "_site", "catalog.json"), encoding="utf-8"))

copied, same, missing = 0, 0, []
for g in cat["groups"]:
    for it in g["items"]:
        rel = it["path"]
        src = os.path.join(src_root, *rel.split("/"))
        dst = os.path.join(ROOT, *rel.split("/"))
        if not os.path.isfile(src):
            missing.append(rel); continue
        if os.path.isfile(dst) and os.path.getsize(dst) == os.path.getsize(src) and open(src, "rb").read() == open(dst, "rb").read():
            same += 1; continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst); copied += 1
        print("updated:", rel)

print(f"copied {copied}, unchanged {same}, missing {len(missing)}")
for m in missing:
    print("  MISSING in OneDrive:", m)
