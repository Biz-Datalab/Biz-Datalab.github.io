"""Build data/site.json (and data/price-history.csv) from the editable files.

Inputs
  content/profile.md, content/projects/*.md, content/ai-resources.md, content/news.md
  prices/YYYY-MM-DD_*.csv          Blue Nile exports (title column + price column)
  prices/YYYY-MM-DD_comment.txt    optional comment for that edition

Each price row is classified by its listing title: "Lab-Grown" -> lab-grown, otherwise natural;
carat weight is read from "<number> Carat". Stones outside 0.90-0.99 ct and 1.00-1.49 ct are skipped.
95% CI = mean +/- t(0.975, n-1) * SE  (same as Excel Descriptive Statistics "Confidence Level").
"""
import csv, json, math, os, re, statistics, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDS = {"090": (0.90, 0.999), "100": (1.00, 1.499)}
LABELS = {"n090": "Natural 0.90-0.99 ct", "n100": "Natural 1.00-1.49 ct",
          "l090": "Lab-grown 0.90-0.99 ct", "l100": "Lab-grown 1.00-1.49 ct"}
warnings = []


def read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def parse_md(path):
    """Blocks start with '## Title'; fields are '- key: value' lines. HTML comments are ignored."""
    text = re.sub(r"<!--.*?-->", "", read(path), flags=re.S)
    items, cur = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = {"title": line[3:].strip()}
            items.append(cur)
            continue
        m = re.match(r"\s*[-*]\s*([A-Za-z0-9 _]+?)\s*:\s?(.*)$", line)
        if m and cur is not None:
            cur[m.group(1).strip().lower()] = m.group(2).strip()
    return items


def parse_fields(path):
    text = re.sub(r"<!--.*?-->", "", read(path), flags=re.S)
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*[-*]\s*([A-Za-z0-9_]+)\s*:\s?(.*)$", line)
        if m:
            out[m.group(1).lower()] = m.group(2).strip()
    return out


FIELD_KEYS = {"text", "image", "images", "link", "caption", "size", "linktext"}


def parse_project(path):
    """A project file: '# Title', top '- key: value' fields, then '## Section' blocks.
    A section holds '- item' lines, or '### Subsection' blocks with their own '- key: value' fields."""
    text = re.sub(r"<!--.*?-->", "", read(path), flags=re.S)
    proj = {"slug": os.path.splitext(os.path.basename(path))[0], "title": "", "sections": {}, "section_order": []}
    sec = sub = None
    for line in text.splitlines():
        if line.startswith("# ") and not proj["title"]:
            proj["title"] = line[2:].strip()
            continue
        if line.startswith("## "):
            sec = {"name": line[3:].strip(), "items": [], "subs": []}
            proj["sections"][sec["name"].lower()] = sec
            proj["section_order"].append(sec["name"].lower())
            sub = None
            continue
        if line.startswith("### ") and sec is not None:
            sub = {"title": line[4:].strip(), "bullets": []}
            sec["subs"].append(sub)
            continue
        m = re.match(r"\s*[-*]\s+(.*)$", line)
        if not m:
            continue
        item = m.group(1).strip()
        kv = re.match(r"([A-Za-z_]+)\s*:\s?(.*)$", item)
        if sec is None:
            if kv:
                proj[kv.group(1).lower()] = kv.group(2).strip()
        elif sub is not None:
            if kv and kv.group(1).lower() in FIELD_KEYS:
                sub[kv.group(1).lower()] = kv.group(2).strip()
            else:
                sub["bullets"].append(item)
        elif kv and kv.group(1).lower() in ("intro", "photo", "caption"):
            sec[kv.group(1).lower()] = kv.group(2).strip()
        else:
            sec["items"].append([p.strip() for p in item.split(" | ")])
    for s in proj["sections"].values():
        for sb in s["subs"]:
            if "images" in sb:
                sb["images"] = [x.strip() for x in sb["images"].split(",") if x.strip()]
            elif "image" in sb:
                sb["images"] = [sb.pop("image")]
            for img in sb.get("images", []):
                if not os.path.exists(os.path.join(ROOT, img)):
                    warnings.append(f"{os.path.basename(path)}: image '{img}' not found")
    try:
        proj["order_num"] = float(proj.get("order", 99))
    except ValueError:
        proj["order_num"] = 99
    return proj


def t975(df):
    small = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}
    if df in small:
        return small[df]
    z = 1.959963985
    return (z + (z**3 + z) / (4 * df) + (5 * z**5 + 16 * z**3 + 3 * z) / (96 * df**2)
            + (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / (384 * df**3)
            + (79 * z**9 + 776 * z**7 + 1482 * z**5 - 1920 * z**3 - 945 * z) / (92160 * df**4))


def stats(stones):
    v = [p / c for p, c in stones]
    n = len(v)
    if n < 2:
        return None
    mean = statistics.mean(v)
    half = t975(n - 1) * statistics.stdev(v) / math.sqrt(n)
    r = lambda x: round(x, 1)
    return {"n": n, "mean": r(mean), "lo": r(mean - half), "hi": r(mean + half),
            "median": r(statistics.median(v)), "min": r(min(v)), "max": r(max(v)),
            "avg_stone": r(statistics.mean(p for p, _ in stones)),
            "avg_carat": round(statistics.mean(c for _, c in stones), 3)}


def parse_price_file(path, cells):
    lab_hint = "lab" in os.path.basename(path).lower()
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    used = skipped = 0
    for row in rows:
        line = " ".join(row)
        ct = re.search(r"(\d+(?:\.\d+)?)\s*Carat", line, re.I)
        pr = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", line)
        if not ct or not pr:
            continue  # header or blank
        c, p = float(ct.group(1)), float(pr.group(1).replace(",", ""))
        lab = bool(re.search(r"lab[\s-]*grown", line, re.I)) or (lab_hint and not re.search(r"natural", line, re.I))
        band = next((k for k, (lo, hi) in BANDS.items() if lo - 1e-9 <= c <= hi + 1e-9), None)
        if band is None or p <= 50:
            skipped += 1
            continue
        cells[("l" if lab else "n") + band].append((p, c))
        used += 1
    if skipped:
        warnings.append(f"{os.path.basename(path)}: {skipped} row(s) outside the carat bands were skipped")
    if not used:
        warnings.append(f"{os.path.basename(path)}: no usable rows found")


def pct(a, b):
    return 100 * (a / b - 1)


def auto_comment(c, prev):
    parts = []
    r = []
    if c.get("n090") and c.get("l090"):
        r.append(round(100 * c["l090"]["mean"] / c["n090"]["mean"]))
    if c.get("n100") and c.get("l100"):
        r.append(round(100 * c["l100"]["mean"] / c["n100"]["mean"]))
    if c.get("n090") and c.get("n100"):
        parts.append(f"Natural stones carry a {round(pct(c['n100']['mean'], c['n090']['mean']))}% per-carat premium above 1 carat.")
    if prev:
        ch = []
        for k, lab in (("n100", "natural 1.00-1.49 ct"), ("l100", "lab-grown 1.00-1.49 ct")):
            a, b = c.get(k), prev["cells"].get(k)
            if not a or not b:
                continue
            d = pct(a["mean"], b["mean"])
            overlap = a["lo"] <= b["hi"] and b["lo"] <= a["hi"]
            word = "unchanged" if abs(d) < 0.05 else f"{'up' if d > 0 else 'down'} {abs(d):.1f}%"
            ch.append(f"{lab} is {word}" + (" (within the confidence interval)" if overlap else ""))
        if ch:
            parts.append(f"Since {prev['date']}, " + ", and ".join(ch) + ".")
    return " ".join(parts)


def build_prices():
    groups = defaultdict(list)
    pdir = os.path.join(ROOT, "prices")
    for name in sorted(os.listdir(pdir)):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", name)
        if m and name.lower().endswith(".csv"):
            groups[m.group(1)].append(os.path.join(pdir, name))
        elif name.lower().endswith(".csv"):
            warnings.append(f"prices/{name}: file name must start with the date, e.g. 2026-11-13_natural.csv")
    editions = []
    for date in sorted(groups):
        cells = defaultdict(list)
        for path in groups[date]:
            parse_price_file(path, cells)
        st = {k: stats(cells[k]) for k in LABELS if len(cells[k]) >= 2}
        if not st:
            continue
        cpath = os.path.join(pdir, f"{date}_comment.txt")
        comment = read(cpath).strip() if os.path.exists(cpath) else auto_comment(st, editions[-1] if editions else None)
        editions.append({"date": date, "source": "Blue Nile listings", "comment": comment, "cells": st})
    return editions


def main():
    cdir = os.path.join(ROOT, "content")
    profile = parse_fields(os.path.join(cdir, "profile.md"))
    pdir = os.path.join(cdir, "projects")
    projects = sorted((parse_project(os.path.join(pdir, f)) for f in os.listdir(pdir) if f.endswith(".md")),
                      key=lambda p: (p["order_num"], p["title"])) if os.path.isdir(pdir) else []
    resources = [{"title": r["title"], "url": r.get("link", ""), "type": r.get("type", "Article"),
                  "source": r.get("source", ""), "date": r.get("date", ""), "comment": r.get("comment", "")}
                 for r in parse_md(os.path.join(cdir, "ai-resources.md")) if r.get("link")]
    news = [{"title": n["title"], "url": n.get("link", ""), "source": n.get("source", ""),
             "date": n.get("date", ""), "category": n.get("category", "market").lower()}
            for n in parse_md(os.path.join(cdir, "news.md")) if n.get("link")]
    editions = build_prices()

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    site = {"profile": profile, "projects": projects, "resources": resources, "news": news, "editions": editions}
    with open(os.path.join(ROOT, "data", "site.json"), "w", encoding="utf-8") as f:
        json.dump(site, f, ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "data", "price-history.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "indicator", "n", "mean_per_ct", "ci95_low", "ci95_high", "median_per_ct",
                    "min_per_ct", "max_per_ct", "avg_stone_price", "avg_carat"])
        for e in editions:
            for k, label in LABELS.items():
                s = e["cells"].get(k)
                if s:
                    w.writerow([e["date"], label, s["n"], s["mean"], s["lo"], s["hi"], s["median"],
                                s["min"], s["max"], s["avg_stone"], s["avg_carat"]])
    stamp_assets()
    for wmsg in warnings:
        print("WARNING:", wmsg)
    print(f"Built site.json: {len(editions)} price edition(s), {len(projects)} project(s), "
          f"{len(resources)} AI resource(s), {len(news)} news item(s).")


def stamp_assets():
    """Add a content hash to the stylesheet link so browsers load the new version after each change."""
    import hashlib
    css = os.path.join(ROOT, "assets", "site.css")
    if not os.path.exists(css):
        return
    v = hashlib.md5(open(css, "rb").read()).hexdigest()[:8]
    for page in ("index.html", "project.html"):
        path = os.path.join(ROOT, page)
        if os.path.exists(path):
            html = read(path)
            new = re.sub(r'assets/site\.css(\?v=[0-9a-f]+)?"', f'assets/site.css?v={v}"', html)
            if new != html:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)


if __name__ == "__main__":
    sys.exit(main())
