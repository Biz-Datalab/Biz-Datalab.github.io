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

## 3. Experiential learning projects

Each project is one file in **content/projects/** (for example `thrive.md`) and gets its own story page.
Images go in a folder under **projects/** (for example `projects/thrive/`).

**Two page styles**
- **Full story** (long funded projects): copy **content/projects/thrive.md**.
- **Brief** (course and student projects): copy **content/projects/diamond-pricing.md**. It shows a short summary,
  a row of workflow steps, and a gallery of results. Add `- size: wide` to a result to show it full width.

**Label color** (the small banner above the title): set `- badge:` to `funded` (black), `capstone` (greenish grey),
or `student` (grey), and `- label:` to the words shown, e.g. `- label: Capstone project`.

On the home page, projects show as a grid of small cards. The first 6 are shown, with a "Show all" link for the rest,
and the three type boxes above the grid filter the cards.

**Add a new project**
1. Open the project file that matches the style you want (see above), select all the text, and copy it.
2. In **content/projects/**, choose **Add file → Create new file**. Name it with a short word, e.g. `retail-pricing.md`.
3. Paste, then change the text. Set `- type:` to `funded`, `group`, or `individual`, and `- order:` to its position on the page (1 = first).
4. Delete any section you don't need (from its `## ` line to the next `## ` line). Sections you can use:
   `Links`, `Numbers`, `Student work`, `Emerging needs and opportunities`, `Long-term vision`, `Student voices`,
   `Outcomes`, `Team`, `Partners`. Any other `## Section` name shows as a simple list.
5. **Commit changes.**

**Add images:** open **projects/** → **Add file → Upload files**, upload into a project folder, then write the path
in the project file, e.g. `- image: projects/retail-pricing/poster.jpg`. Several images: `- images: a.jpg, b.jpg`.

**Attach a PDF (report, poster, slides):** upload it to the project's folder and add it under `## Links`, e.g.
`- Student report (PDF) | projects/retail-pricing/report.pdf`.

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
