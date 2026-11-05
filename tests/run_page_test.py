#!/usr/bin/env python3
"""Headless test of app/index.html against a stand-in database and grader.

Runs three scenarios in Google Chrome (headless): the map, a full level (primer,
answer, grading, skip, summary, checkpoint), and the page with no runtime.
Usage: python3 tests/run_page_test.py   (exit code 0 = all passed)
"""
import html, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "out"

def find_chrome():
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"]:
        if os.path.exists(c):
            return c
    for name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]:
        p = shutil.which(name)
        if p:
            return p
    return None

def build(scenario):
    page = (ROOT / "app" / "index.html").read_text()
    mock = (ROOT / "tests" / "mock_runtime.js").read_text()
    drive = (ROOT / "tests" / "drive.js").read_text()
    pre = f"<script>window.__scenario={json.dumps(scenario)};window.__noRuntime={'true' if scenario=='noruntime' else 'false'};</script>"
    inject = pre + "<script>" + mock + "</script><script>" + drive + "</script>\n<script>\n(()=>{"
    assert page.count("<script>\n(()=>{") == 1, "page script marker not found"
    OUT.mkdir(exist_ok=True)
    f = OUT / f"{scenario}.html"
    f.write_text(page.replace("<script>\n(()=>{", inject, 1))
    return f

def run(chrome, scenario, hash_=""):
    f = build(scenario)
    cmd = [chrome, "--headless=new", "--disable-gpu", "--force-prefers-reduced-motion",
           "--virtual-time-budget=8000", "--window-size=1000,900", "--dump-dom", f.as_uri() + hash_]
    dom = subprocess.run(cmd, capture_output=True, text=True, timeout=90).stdout
    found = re.findall(r'<pre id="test-result">(\{.*?\})</pre>', dom, re.S)
    if not found:
        return {"error": "no result (page script crashed?)"}
    return json.loads(html.unescape(found[-1]))

def main():
    chrome = find_chrome()
    if not chrome:
        print("SKIP: Google Chrome or Chromium not found.")
        return 0
    checks = []
    m = run(chrome, "map")
    checks += [("map: title from meta/path", m.get("h1") == "Test Summit"),
               ("map: one button per trail day (16)", m.get("levels") == 16),
               ("map: 2 levels unlocked", m.get("unlocked") == 2),
               ("map: list shows 2 levels", m.get("listButtons") == 2),
               ("map: climber placed", "translate(" in m.get("climber", "")),
               ("map: subtitle names the course", "Test Course" in m.get("sub", ""))]
    l = run(chrome, "level", "#l-2026-11-03")
    checks += [("level: primer shown first", l.get("primer") is True),
               ("level: graded answer shows verdict", l.get("pill1") == "Partial"),
               ("level: answer saved as partial", l.get("verdict1") == "partial"),
               ("level: grade prompt has course and key", l.get("gradePromptHasCourse") is True),
               ("level: no personal names in prompts", l.get("gradePromptClean") is True),
               ("level: skip saved", l.get("verdict2") == "skipped"),
               ("level: summary after last question", l.get("summary") == "Level complete"),
               ("level: checkpoint written", bool(l.get("checkpoint")))]
    n = run(chrome, "noruntime")
    checks += [("no runtime: explains sign-in", "claude.ai" in n.get("note", ""))]
    for r in (m, l, n):
        if r.get("error"):
            print("ERROR:", r["error"])
    failed = 0
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
        failed += not ok
    print(f"{len(checks) - failed}/{len(checks)} passed")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
