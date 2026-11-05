#!/usr/bin/env python3
"""Check a Summit level JSON file before it's written to the page.

Usage: python3 tests/check_level.py my-course/levels/2026-11-05.json
Prints each problem and exits 1 if there are any.
"""
import json, re, sys

def check(level):
    p = []
    if not isinstance(level, dict):
        return ["level must be a JSON object"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(level.get("date", ""))):
        p.append("date must be YYYY-MM-DD")
    if not isinstance(level.get("target"), str) or not level["target"].strip():
        p.append("target (e.g. 'Quiz 3') is required")
    if "daysLeft" in level and not isinstance(level["daysLeft"], int):
        p.append("daysLeft must be a whole number")
    for i, pr in enumerate(level.get("primer") or []):
        if not (isinstance(pr, dict) and str(pr.get("h", "")).strip() and str(pr.get("body", "")).strip()):
            p.append(f"primer[{i}] needs h and body")
    qs = level.get("questions")
    if not isinstance(qs, list) or not qs:
        return p + ["questions must be a non-empty list"]
    if len(qs) > 12:
        p.append(f"{len(qs)} questions is too many for one day (max 12)")
    ids = set()
    for i, q in enumerate(qs):
        w = f"questions[{i}]"
        if not isinstance(q, dict):
            p.append(f"{w} must be an object"); continue
        qid = q.get("id")
        if not re.fullmatch(r"q\d+", str(qid)):
            p.append(f"{w}.id must look like q1, q2, ...")
        elif qid in ids:
            p.append(f"{w}.id {qid} is repeated")
        ids.add(qid)
        if len(str(q.get("text", "")).strip()) < 10:
            p.append(f"{w}.text is missing or too short")
        k = q.get("key")
        if not isinstance(k, dict):
            p.append(f"{w}.key is required (the page grades from it)"); continue
        if len(str(k.get("mechanism", "")).split()) < 12:
            p.append(f"{w}.key.mechanism should be the full answer (12+ words)")
        mh = k.get("mustHave")
        if not (isinstance(mh, list) and mh and all(isinstance(x, str) and x.strip() for x in mh)):
            p.append(f"{w}.key.mustHave needs at least one point")
        if "traps" in k and not isinstance(k["traps"], list):
            p.append(f"{w}.key.traps must be a list")
        if not str(k.get("slides", "")).strip():
            p.append(f"{w}.key.slides should say where this is in the materials")
    try:
        if len(json.dumps(level).encode()) > 200_000:
            p.append("level is over 200 KB; the page's documents max out at 256 KB")
    except (TypeError, ValueError):
        p.append("level must be plain JSON")
    return p

def main(argv):
    if len(argv) != 2:
        print(__doc__.strip()); return 2
    with open(argv[1]) as f:
        level = json.load(f)
    problems = check(level)
    for x in problems:
        print("PROBLEM:", x)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
