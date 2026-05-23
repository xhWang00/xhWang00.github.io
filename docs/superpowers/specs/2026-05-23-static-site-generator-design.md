# Static Site Generator for Personal Blog

## Overview
A single-file Python static site generator that reads Markdown files from `mds/`, converts them to HTML, and outputs them to the repo root for GitHub Pages hosting. Brutalist design: cards with borders, no shadows, no fades, system sans-serif fonts.

## Project Layout
```
/
├── generate.py         # Single generator script
├── style.css           # Brutalist CSS stylesheet
├── requirements.txt    # Python dependencies
├── mds/                # Source: Markdown files with YAML front matter
│   └── slug.md
├── index.html          # Generated: page 1 of paginated index
├── indices/            # Generated: paginated index pages 2+
│   ├── index2.html
│   ├── index3.html
│   └── ...
├── posts/              # Generated: per-post HTML files
│   └── slug.html
└── .gitignore
```

## Source Files
- Location: `mds/<slug>.md`
- Required front matter: `title`, `date`
- Optional front matter: `tags`
- Body is standard Markdown with fenced code blocks and LaTeX math

## Output
- Posts: `posts/<slug>.html` — one HTML page per markdown file
- Index: paginated at 10 posts per page
  - Page 1: `/index.html`
  - Pages 2+: `/indices/indexN.html`
- Each index card shows: title, date, first-paragraph excerpt

## Generator Behavior
1. Read all `.md` files from `mds/`
2. Parse YAML front matter (title, date, tags)
3. Convert Markdown body to HTML with:
   - Syntax highlighting via Pygments (`codehilite` extension)
   - MathJax support: `$...$` inline and `$$...$$` display math
4. Wrap in HTML template:
   - `<title>{title}</title>` (no site name suffix)
   - MathJax script loaded from CDN
   - Link to `/style.css`
5. Generate paginated index pages sorted by date descending

## HTML Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="/style.css">
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
  <header class="site-header">
    <a class="site-title" href="/">Back to home</a>
  </header>
  <main class="content">{content}</main>
  <footer class="site-footer"><p>&copy; {year}</p></footer>
</body>
</html>
```

## CSS Design (Brutalism)
- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", "Microsoft YaHei", "PingFang SC", sans-serif`
  (Covers macOS/iOS, Windows, and Linux CJK fonts)
- No external fonts
- Cards bordered with `2px solid #000`
- `border-radius: 0` everywhere
- `box-shadow: none` everywhere
- No transitions, animations, or fades
- Max-width 800px container, auto-centered
- Links: `text-decoration: underline`, `color: #000`
- Code blocks: `background: #f4f4f4`, `border: 2px solid #000`, monospace font
- Responsive: single column, no complex media queries
- Body: white background, black text

## Dependencies
```
markdown
pyyaml
pygments
```

These are specified in `requirements.txt` and installed via `pip install -r requirements.txt`.

## Git
- Generated files (`posts/`, `indices/`, `index.html`) added to `.gitignore`
- Source files (`mds/*.md`, `generate.py`, `style.css`, `requirements.txt`) tracked

## Usage
```sh
pip install -r requirements.txt
python generate.py
```
