# Cristiano Saltori — research website

A lightweight Hugo website for [Cristiano Saltori](https://saltoricristiano.github.io/). The design takes inspiration from [Benjamin Missaoui's website](https://www.benjamin-missaoui.me/) and the visual publication rows on [Shengyu Huang's website](https://shengyuh.github.io/).

The content is stored in Markdown and JSON. There is no Node.js dependency, database, or paid hosting requirement. Hugo builds a static website, and GitHub Actions publishes changes pushed to `main`.

[Source repository](https://github.com/saltoricristiano/saltoricristiano.github.io) · [Deployment status](https://github.com/saltoricristiano/saltoricristiano.github.io/actions/workflows/pages.yml) · [Website](https://saltoricristiano.github.io/)

## Preview locally

Use [Hugo 0.122.0](https://github.com/gohugoio/hugo/releases/tag/v0.122.0), matching the deployment workflow, and Python 3.11 or newer for the helper scripts. The standard Hugo binary is sufficient.

From this directory:

```sh
hugo server --disableFastRender
```

Open the local address printed by Hugo, usually `http://localhost:1313`. Saving a content or style change refreshes the preview.

Build and check the production website:

```sh
hugo --gc --minify
python3 scripts/validate.py
```

`public/` contains the generated website and is deliberately excluded from Git. The validation script checks publication metadata, local links, image files, anchors, and basic HTML accessibility. It does not crawl external websites or guarantee citation accuracy.

In a restricted environment such as Codex, add `--cacheDir /tmp/cristiano-hugo-cache` to Hugo commands if the default user cache directory is not writable. Starting a local server may require the environment's network approval.

## Update the website

| Change | Edit |
| --- | --- |
| Biography | `content/_index.md` |
| Name, role, lab, topic line, research interests, social links, education, experience and institution logo paths | `data/profile.json` |
| News | `data/news.json` |
| One publication | `content/publications/<paper-slug>/index.md` |
| Photos and publication teasers | `static/images/` |
| Robot head in the header and browser tab | `static/images/favicon.svg` |
| Site URL and general configuration | `hugo.toml` |
| Footer's last-updated date | `updated` under `[params]` in `hugo.toml` |
| Layout and styling | `layouts/` and `static/` |

The footer date is manual: set `[params].updated` to the date of your latest content update in `YYYY-MM-DD` format.

To add contact email, fill `email` in `data/profile.json` with your address, without a `mailto:` prefix. To add a CV, put the PDF in `static/files/cv.pdf` and set `cv` to `files/cv.pdf`. Both fields start empty and their links appear only when filled.

News starts as an empty array, so its section stays hidden until you have an update. Add objects to `data/news.json` using the structure `{"date": "YYYY-MM-DD", "text": "Your update in Markdown."}`. Dates must be real ISO dates; the website displays month and year, with newest entries first. Standard Markdown links work inside `text`.

Keep factual dates tied to the event or publication itself. When only a publication's year is known, use January 1 of that year for `date` and put the same year in `year`; the site displays the year rather than implying an exact publication day. Use the actual date when it is verified. Do not change old publication dates to make a recent website edit appear newer.

The initial bibliography is a verified selection, not a complete Google Scholar import. Review it against your [Scholar profile](https://scholar.google.com/citations?user=PID7Z4oAAAAJ) when adding papers. The website does not scrape Scholar or update itself when another profile changes. Future updates are explicit edits committed to this repository.

Hugo automatically creates smaller versions of publication images for the homepage. Keep the original figure in `static/images/publications/`; you do not need to resize it by hand. Original figures are retained for individual publication pages.

### Add a paper

Create an unpublished draft:

```sh
python3 scripts/new-publication.py \
  --title "Your paper title" \
  --year 2026 \
  --venue "Conference or journal"
```

The command creates `content/publications/your-paper-title/index.md`. Use `--slug short-name` if you prefer a shorter directory name. Existing entries are never overwritten.

Fill in the TOML block at the top of the file:

- `authors`: all verified author names, in paper order; the website highlights Cristiano's name.
- `paper_url`: the paper's publisher, arXiv, or PDF link.
- `code_url` and `project_url`: optional links; omit them if unavailable.
- `bibtex`: optional exact citation from the publisher or author project page, inside triple single quotes. Leave empty or omit it when unavailable; the BibTeX control appears only when a citation is supplied.
- `image`: optional path such as `images/publications/short-name.webp`; put the file in `static/images/publications/`.
- `image_alt`: a short description of the teaser's content.
- `animation` and `animation_alt`: optional local GIF path and demo description. Keep `image` as the static fallback. Demos start automatically when they enter the viewport and pause offscreen, in a hidden tab, or when filtered out. A visitor's explicit pause is preserved until they choose to play again. Visitors requesting reduced motion can start demos manually. The initial per-paper repository checks are in `PUBLICATION_GIF_AUDIT.md`.
- `featured`: whether the entry belongs in the selected-publications view.

Preview drafts with `hugo server --buildDrafts`. After checking the title, authors, venue, links, and any citation or image supplied, change `draft = true` to `draft = false`. Normal builds and deployment exclude drafts. A future `date` is also excluded by normal Hugo builds until that date is reached.

Run the production build and validation commands before committing. For an accepted paper without a final publisher citation, accurately label its current status and use the verified preprint citation until the final one is available.

### Keep updates manageable

After a new paper, role, talk, or award, edit the relevant content file, preview it, and commit the change. A brief monthly review is enough to catch stale links and missing publications. There is no scheduled task or automated content editing configured.

## Deploy updates

Work on `main`, which contains the current Hugo source. The previous website's history is preserved, and its historical `master` and `gh-pages` branches are retained for reference. New website edits and deployments use `main`.

After editing the content and checking the local preview, update the footer date in `hugo.toml`, then build, validate, review, and publish:

```sh
hugo --gc --minify
python3 scripts/validate.py
git diff
git status
git add .
git commit -m "Update research profile"
git push origin main
```

Use a commit message that describes the actual update. A push starts **Build and deploy website** in [Actions](https://github.com/saltoricristiano/saltoricristiano.github.io/actions/workflows/pages.yml). Wait for both build and deployment to succeed, then check the [website](https://saltoricristiano.github.io/). A successful local build alone does not confirm publication.

The included workflow downloads Hugo 0.122.0, builds the site, runs validation, uploads `public/`, and deploys that artifact using GitHub's official Pages actions. It uses the repository's built-in token; no personal access token needs to be stored in the website. Keep the `main` branch and the `github-pages` environment as the intended publishing destinations.

The repository's **Settings → Pages → Source** should be **GitHub Actions**. To retry a deployment without a new commit, open the workflow in Actions, select **Run workflow**, and choose `main`. Do not upload generated files or push them to `gh-pages`; the workflow deploys the build artifact directly.

For a project repository such as `research-website`, GitHub Pages uses `https://saltoricristiano.github.io/research-website/`. The workflow supplies GitHub's base URL automatically. Test this form locally before changing repositories:

```sh
hugo --gc --minify --baseURL https://saltoricristiano.github.io/research-website/ --destination /tmp/research-website-build
python3 scripts/validate.py --public-dir /tmp/research-website-build --base-url https://saltoricristiano.github.io/research-website/
```

A custom domain is optional and can be connected later. Follow [GitHub's custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages) and update `baseURL` to the final HTTPS URL after DNS is configured.

## Sources and maintenance notes

The biography uses Cristiano's approved wording, including his current [NVIDIA Spatial Intelligence Lab (SIL)](https://research.nvidia.com/labs/sil/) affiliation. `CONTENT_SOURCES.md` records supporting sources, historical CV details, and Cristiano's corrections to dates and experience. Publication provenance is recorded in `PUBLICATION_SOURCES.md`. Keep metadata and images aligned with the corresponding paper or project sources, and retain source attribution when updating the assets.

Official deployment references: [Hugo on GitHub Pages](https://gohugo.io/host-and-deploy/host-on-github-pages/) and [GitHub custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Action versions were checked against their official release pages when preparing this website. Review and test tool-version upgrades before changing the pinned versions in `.github/workflows/pages.yml`.
