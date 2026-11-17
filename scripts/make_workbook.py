"""Build the Diamond Market Watch Excel workbook for one price edition.

Usage:  python3 scripts/make_workbook.py [YYYY-MM-DD]
        (no date = the latest edition found in prices/)

Reads prices/<date>_<natural|lab>_<band>.csv, fills scripts/workbook-template.xlsx
(Summary sheet + one sample sheet per cell, with live Excel formulas), adds a History
sheet from data/price-history.csv, and saves prices/workbooks/Diamond_Market_Watch_<date>.xlsx.
Run scripts/build.py first so data/price-history.csv is current.
"""
import copy, csv, os, re, sys
from openpyxl import load_workbook
from openpyxl.styles import Font

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "prices")
TEMPLATE = os.path.join(ROOT, "scripts", "workbook-template.xlsx")
SOURCE = "U.S. online jewelry retailers"
SHEETS = [  # sheet name, file kind, file band, title prefix, band label
    ("Natural 0.90-0.99", "natural", "0.90-0.99", "Natural diamonds", "0.90–0.99 ct", (0.90, 0.999)),
    ("Natural 1.00-1.49", "natural", "1.00-1.49", "Natural diamonds", "1.00–1.49 ct", (1.00, 1.499)),
    ("Lab 0.90-0.99", "lab", "0.90-0.99", "Lab-grown diamonds", "0.90–0.99 ct", (0.90, 0.999)),
    ("Lab 1.00-1.49", "lab", "1.00-1.49", "Lab-grown diamonds", "1.00–1.49 ct", (1.00, 1.499)),
]
FIRST = 5  # first data row


def read_rows(path, band):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            line = " ".join(row)
            ct = re.search(r"(\d+(?:\.\d+)?)\s*Carat", line, re.I)
            pr = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", line)
            if not ct or not pr:
                continue
            c, p = float(ct.group(1)), float(pr.group(1).replace(",", ""))
            if not (band[0] - 1e-9 <= c <= band[1] + 1e-9) or p <= 50:
                continue
            title = row[0].strip()
            lab = title.split()[0] if title else ""
            cut = re.search(r"(Ideal|Excellent|Very Good|Good|Fair|Poor)\s+Cut", title, re.I)
            rows.append((title, lab, c, cut.group(1) if cut else "", p))
    return rows


def fill_sheet(ws, rows, title, sub):
    old_last = ws.max_row
    style_row = [copy.copy(ws.cell(FIRST, col)._style) for col in range(1, 7)]
    for r in range(FIRST, max(old_last, FIRST + len(rows)) + 1):
        for col in range(1, 7):
            ws.cell(r, col).value = None
    for i, (t, lab, c, cut, p) in enumerate(rows):
        r = FIRST + i
        for col, v in enumerate([t, lab, c, cut, p, f"=E{r}/C{r}"], start=1):
            cell = ws.cell(r, col, v)
            cell._style = copy.copy(style_row[col - 1])
    last = FIRST + len(rows) - 1
    for r in range(1, ws.max_row + 1):  # point every statistic at the new data range
        v = ws.cell(r, 9).value
        if isinstance(v, str) and v.startswith("="):
            ws.cell(r, 9).value = re.sub(r"\$([CEF])\$5:\$\1\$\d+", lambda m: f"${m.group(1)}$5:${m.group(1)}${last}", v)
    ws["A1"] = title
    ws["A2"] = sub


def main():
    dates = sorted({m.group(1) for n in os.listdir(PDIR) if (m := re.match(r"(\d{4}-\d{2}-\d{2})_.*\.csv$", n))})
    date = sys.argv[1] if len(sys.argv) > 1 else dates[-1]
    wb = load_workbook(TEMPLATE)
    for name, kind, band_file, prefix, band_label, band in SHEETS:
        path = os.path.join(PDIR, f"{date}_{kind}_{band_file}.csv")
        if not os.path.exists(path):
            sys.exit(f"Missing {path}")
        rows = read_rows(path, band)
        fill_sheet(wb[name], rows,
                   f"{prefix} · round · E color · VVS2 · {band_label} · {SOURCE} · {date}",
                   f"Source: online listings from {SOURCE} (asking prices). Carat weight, lab, and cut are read from the listing title.")
    s = wb["Summary"]
    s["A1"] = f"Diamond Market Watch · {date} · round · E color · VVS2 · price per carat ($/ct)"
    s["A2"] = "Click a type in column A to open its sample sheet. CI = 95% confidence interval for the mean asking price per carat."
    for r, (name, *_rest) in zip(range(5, 9), SHEETS):
        s.cell(r, 1).hyperlink = f"#'{name}'!A1"
        s.cell(r, 1).font = Font(color="1D4F91", underline="single")

    if "History" in wb.sheetnames:
        del wb["History"]
    h = wb.create_sheet("History")
    hist = os.path.join(ROOT, "data", "price-history.csv")
    with open(hist, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.reader(f)):
            h.append([row[0], row[1]] + [float(x) if i else x for x in row[2:]] if i else row)
    for cell in h[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = copy.copy(s["A4"].fill)
    for col, w in zip("ABCDEFGHIJK", (12, 24, 6, 13, 12, 12, 14, 12, 12, 15, 11)):
        h.column_dimensions[col].width = w
    for row in h.iter_rows(min_row=2):
        for cell in row[3:10]:
            cell.number_format = "$#,##0"
        row[10].number_format = "0.000"
    h.freeze_panes = "A2"
    h["M1"] = "All editions, from the website's price-history.csv. One row per cell per edition."

    out = os.path.join(PDIR, "workbooks", f"Diamond_Market_Watch_{date}.xlsx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wb.save(out)
    print("Saved", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
