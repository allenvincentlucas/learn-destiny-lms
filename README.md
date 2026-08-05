# Follett Destiny LMS Training Curriculum — Website

A free, independent, 9-module training curriculum for Follett Destiny, published as a static website. Built from the companion Word document (`Follett_Destiny_LMS_-_Module_1_Training___Orientation.docx`), updated for Destiny 24.0/23.5.

**Not affiliated with or endorsed by Follett Software.** Trademarks (Follett Destiny®, Destiny Discover®, etc.) belong to their respective owners.

## Structure

```
/
├── index.html              Homepage — hero, 9-module grid, "what's included," "who it's for"
├── glossary.html           Glossary of key terms (MARC, SIS, FERPA, WCAG, etc.)
├── modules/
│   ├── module-1.html       Orientation & System Navigation
│   ├── module-2.html       System Structure, Hierarchy & Access Levels
│   ├── module-3.html       Patron Management & Class Schedules
│   ├── module-4.html       Cataloging, Resource Records & Collection Management
│   ├── module-5.html       Daily Circulation & Resource Tracking
│   ├── module-6.html       Inventory Management
│   ├── module-7.html       Reporting, Dashboards & Data Analytics
│   ├── module-8.html       Destiny Discover, Collections & Digital Integration
│   └── module-9.html       System Updates & Ongoing Professional Learning
├── assets/
│   └── css/style.css       Shared stylesheet (single file, no build step)
└── .nojekyll               Tells GitHub Pages to serve files as-is (required)
```

Each module page includes: learning objectives, prerequisites/time estimate, one or two embedded YouTube video walkthroughs, the full written content, an interactive self-check knowledge check (click to reveal answers — no JavaScript required, pure `<details>/<summary>`), a full Works Cited list, and Previous/Next navigation.

## Publishing to GitHub Pages

1. Push this folder's contents to a repository (e.g., `main` branch, root or a `/docs` folder).
2. In the repo, go to **Settings → Pages**.
3. Under **Source**, choose the branch and folder you pushed to (e.g., `main` / `/root` or `main` / `/docs`).
4. Save. GitHub will publish at `https://<username>.github.io/<repo-name>/`.
5. The included `.nojekyll` file is required — without it, GitHub's Jekyll build step may ignore the `assets/` folder.

No build step, no dependencies, no npm/node required — it's plain HTML/CSS. Google Fonts (Space Grotesk, Inter, JetBrains Mono) load from a CDN `<link>` in each page's `<head>`, and videos embed via YouTube's privacy-enhanced `youtube-nocookie.com` player.

## Editing content

- **Wording/text changes**: edit the relevant `modules/module-N.html` file directly, or regenerate from the source docx using the scripts in `build-scripts/` (requires the original docx's extracted paragraph data; see `build-scripts/generate_site.py`).
- **Site-wide styling**: edit `assets/css/style.css` — it's shared by every page.
- **Adding/changing videos**: each module page has one or two `<iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID">` blocks — swap the `VIDEO_ID` and the caption text next to it.
- **Glossary terms**: edit `glossary.html` directly.

## Content note

This curriculum's factual claims about Destiny 24.0/23.5 features have been checked against Follett's own current release documentation. Citations throughout point to official Follett Help Center pages, Follett Community resources, and named third-party tutorial videos.
