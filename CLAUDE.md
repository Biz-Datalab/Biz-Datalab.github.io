# Biz Data Lab website: guide for Claude

Read this first in every session about the website. The repo is the source of truth: if this
guide and the repo disagree, trust the repo and update this guide.

## What the site is
- https://biz-datalab.github.io is the personal website of Dr. Chong Huang (Eberhardt School of Business,
  University of the Pacific), linked from the official faculty page. Audience: academics and students.
- It is framed around two research areas: diamonds/jewelry, and AI in business practice.
- Sections: About · Experiential Learning (student projects) · Diamond Market Watch (prices, AI design
  showcase, paper citation, Industry News) · AI Watch (curated videos, articles, papers).
- Footer: "© YEAR Chong Huang · Personal website featuring my research, curated resources, and student projects."
- Not yet officially announced. The owner approved one email link (2026-11-07): "contact me" in the Experiential
  Learning statement links to chuang@pacific.edu. Do not add the email anywhere else unless the owner asks.
- Visitor analytics: GoatCounter (biz-datalab.goatcounter.com).

## Access and publishing
- GitHub repo: Biz-Datalab/Biz-Datalab.github.io, branch main. Claude's access must stay limited to this
  one repo. Never ask for or attach any other repository.
- Attach with add_repo (access "push"), clone, and run `git pull --rebase` before editing.
- Edit the content files, then run `python3 scripts/build.py`. It must print "Built site.json" with no new WARNING lines.
- Commit and push to main. The workflow `.github/workflows/build-site.yml` rebuilds `data/`, then requests a
  Pages build. Pages uses "Deploy from a branch" (main, / root).
- Confirm the publish: `gh run list -R Biz-Datalab/Biz-Datalab.github.io -L 3` shows "pages build and
  deployment" as completed/success, usually within 1 to 2 minutes. A "cancelled" run right after a push is normal
  (it is superseded by the next one). Do not say a change is live until this check passes.

## Where things live
- `content/profile.md`: headline, bio, statement.
- `content/projects/*.md`: one file per project. Full story layout: copy `thrive.md`. Brief layout: copy `diamond-pricing.md`.
  Images go in `projects/<slug>/`. In prose and captions, `[text](url)` becomes a link.
  An `## Acknowledgments` section renders as "Thank you".
- `content/news.md`: Industry News. Fields: link, source, date, category (prices | market | ai), takeaway.
- `content/ai-resources.md`: AI Watch. Fields: link, type (Video | Article | Paper), source, date, comment.
  The owner also adds items through the GitHub issue form (`.github/ISSUE_TEMPLATE/ai-watch.yml`).
- `prices/`: the owner uploads four CSVs every two weeks, named `YYYY-MM-DD_<natural|lab>_<carat range>.csv`.
  The benchmark is E color, VVS2, 0.90–0.99 ct and 1.00–1.49 ct. An optional `YYYY-MM-DD_comment.txt` replaces the
  automatic comment.
- `index.html`: `renderNews()` and `renderRes()`. `project.html`: project page renderer. `assets/site.css`: styles.
- `HOW-TO-UPDATE.md`: the owner's own step-by-step guide. Keep it in sync when workflows change.

## House rules (always)
- Verify every fact. Leave out anything uncertain rather than guessing.
- When the owner asks to see wording first, show it and wait for approval before publishing.
- Never name specific AI tools or models when comparing AI output (say "two leading commercial AI models").
- Never name a single data vendor. Price data source is "U.S. online jewelry retailers".
- No copyrighted posters, logos, or characters in images.
- Credit students by full name, and each name only once per project page.
- Keep wording plain, neutral and factual. No hype.

## Industry News and AI Watch rules (standing)
- Title = the exact original headline from the linked page, character for character. Never use a finding as the title.
- Date = the date shown on the page: the publication date; if there is none, the "last updated" date or, for an event,
  the event date (say which in the takeaway).
- The finding goes only in the separate takeaway line (news) or comment (AI Watch), one neutral sentence with figures.
- Open each page to confirm the headline and date before publishing. If a site is blocked, find the page with WebSearch.
  If the headline or date still cannot be confirmed, do not publish it; ask the owner.
- No duplicates: also skip syndicated copies of the same article on another site.
- Jewelry news must always cover lab-grown diamond progress (technology, crystal size, capacity, prices, industrial or
  semiconductor uses, market share). Start those takeaways with "Lab-grown progress:".
- A weekly scheduled task, "Weekly diamond & jewelry news" (Mondays 1:17 pm Pacific), adds 2 to 4 items following
  these rules. It belongs to the owner's account, not to any Project. Change it with update_trigger.

## Open items
- AI Watch: "Andrej Karpathy: 'Delete Everything, Keep Attention' (Stanford lecture)" has an unverified title and date
  (2026-09-03). Confirm with the owner or remove it.
