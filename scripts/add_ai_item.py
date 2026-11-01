"""Turn an "Add to AI Watch" form submission (a GitHub issue) into an entry in content/ai-resources.md.
Reads ISSUE_TITLE and ISSUE_BODY from the environment. Prints the added title."""
import datetime, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
title = re.sub(r"^\s*AI Watch:\s*", "", os.environ.get("ISSUE_TITLE", ""), flags=re.I).strip()
body = os.environ.get("ISSUE_BODY", "")

fields = {}
for m in re.finditer(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|\Z)", body, flags=re.M | re.S):
    val = m.group(2).strip()
    fields[m.group(1).strip().lower()] = "" if val == "_No response_" else " ".join(val.split())

link = fields.get("link", "")
if not title or not re.match(r"https?://\S+", link):
    sys.exit("The form needs a title and a link starting with https://")

block = [f"## {title}", f"- link: {link}", f"- type: {fields.get('type', 'Article') or 'Article'}"]
if fields.get("source"):
    block.append(f"- source: {fields['source']}")
block.append(f"- date: {datetime.date.today().isoformat()}")
if fields.get("your comment"):
    block.append(f"- comment: {fields['your comment']}")

path = os.path.join(ROOT, "content", "ai-resources.md")
with open(path, "a", encoding="utf-8") as f:
    f.write("\n" + "\n".join(block) + "\n")
print(title)
