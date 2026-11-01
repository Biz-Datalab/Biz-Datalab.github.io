# How to update your website

Your site: **https://biz-datalab.github.io**

You update everything here on github.com, in your browser. After each change, the site
rebuilds itself automatically. It is usually live in **1–2 minutes**. To watch it, open the
**Actions** tab: a green check means done, a red cross means something needs fixing (see the end).

---

## 1. Diamond prices (every two weeks)

1. Export your four Blue Nile CSV files as usual.
2. Rename each file so it **starts with the date**, for example:
   - `2026-11-13_natural_0.90-0.99.csv`
   - `2026-11-13_natural_1.00-1.49.csv`
   - `2026-11-13_lab_0.90-0.99.csv`
   - `2026-11-13_lab_1.00-1.49.csv`
3. Open the **prices** folder → **Add file** → **Upload files** → drag in the four files →
   **Commit changes**.

That's it. The site reads the carat weight and "Natural" / "Lab-Grown" from each listing title,
calculates the mean price per carat and the 95% confidence interval, and adds a new edition.
A comment is written automatically.

**Optional, your own comment:** in the prices folder choose **Add file → Create new file**,
name it `2026-11-13_comment.txt`, type your paragraph, and commit. It replaces the automatic comment.

---

## 2. AI Watch (videos, articles, papers)

**Use the form (easiest).** Bookmark this link:
https://github.com/Biz-Datalab/Biz-Datalab.github.io/issues/new?template=ai-watch.yml

1. Open the link (you must be signed in to GitHub as Biz-Datalab).
2. In the title box, replace `AI Watch: ` with the title of the video, article, or paper.
3. Paste the **Link**, choose the **Type** (Video, Article, or Paper), optionally add the **Source** and **Your comment**.
4. Click **Create**.

Within about 2 minutes the item is on the website, and the form closes itself with the note
"Added to AI Watch". Only forms you submit are added; anyone else's are ignored.

**To edit or remove an item:** open **content/ai-resources.md** → pencil icon → change or delete
its block → **Commit changes**.

---

## 3. Experiential learning projects and PDFs

**Attach a PDF to a project**
1. Open the **projects** folder → **Add file → Upload files** → upload the PDF
   (e.g. `ai-skills-gap.pdf`; avoid spaces in the name) → **Commit changes**.
2. Open **content/projects.md** → pencil icon → find the project and type the file name after `- pdf:`
   ```
   - pdf: ai-skills-gap.pdf
   ```
3. **Commit changes.** A "Project brief & student work (PDF)" link appears on the site.

**Add a new project:** copy any block in projects.md (from `## Title` down to `- pdf:`), paste it,
and change the text. Projects show in the order they appear in the file.

---

## 4. Your name, bio, and teaching statement

Open **content/profile.md** → pencil icon → change the text after each colon → **Commit changes**.

---

## 5. Industry news

Claude maintains **content/news.md** weekly. You don't need to do anything.

---

## If something goes wrong

- **Red cross in the Actions tab:** click it, then click "build" to see the message.
  The most common causes are a price file whose name doesn't start with a date (`YYYY-MM-DD`)
  or a PDF name in projects.md that doesn't match the uploaded file exactly.
- **Undo a change:** open the file → **History** → choose an earlier version, or ask Claude.
- Everything in this repository is **public**. Only upload files you are happy to share.
