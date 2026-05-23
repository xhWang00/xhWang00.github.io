# Static Site Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A single-file Python script that converts `mds/*.md` files into a brutalism-themed blog on GitHub Pages.

**Architecture:** Single `generate.py` script reads markdown files with YAML front matter, converts to HTML via `markdown` library with Pygments code highlighting, outputs post pages to `posts/` and paginated index to root/`indices/`. CSS is a separate static file.

**Tech Stack:** Python 3, markdown, pyyaml, pygments, MathJax (CDN)

---

### Task 1: Project Setup & Sample Content

**Files:**
- Create: `requirements.txt`
- Create: `mds/hello-world.md`
- Create: `mds/code-and-math.md`
- Modify: `.gitignore`

- [ ] **Step 1: Create requirements.txt**

```txt
markdown
pyyaml
pygments
```

- [ ] **Step 2: Create sample blog post with front matter**

Create `mds/hello-world.md`:
```markdown
---
title: Hello World
date: 2025-01-15
tags: [meta, introduction]
---

This is my first blog post using the static site generator.

Here's a code example:
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```

And some inline math: $E = mc^2$

Display math:

$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

- [ ] **Step 3: Create second sample post with Chinese content**

Create `mds/中文测试.md`:
```markdown
---
title: 中文测试文章
date: 2025-03-20
tags: [中文, test]
---

这是一篇中文测试文章。

```python
print("你好，世界！")
```

行内公式：$a^2 + b^2 = c^2$
```
```

- [ ] **Step 4: Update .gitignore**

Append to `.gitignore`:
```
# Generated files
index.html
indices/
posts/
```

- [ ] **Step 5: Commit**

```bash
git add requirements.txt mds/hello-world.md mds/中文测试.md .gitignore
git commit -m "chore: add project setup and sample posts"
```

---

### Task 2: Brutalist CSS

**Files:**
- Create: `style.css`

- [ ] **Step 1: Create style.css**

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", "Microsoft YaHei", "PingFang SC", sans-serif;
  color: #000;
  background: #fff;
  line-height: 1.6;
  padding: 2rem 1rem;
}

a {
  color: #000;
  text-decoration: underline;
}

a:hover {
  background: #000;
  color: #fff;
}

img {
  max-width: 100%;
  height: auto;
  border: 2px solid #000;
}

/* Layout */
.site-header {
  max-width: 800px;
  margin: 0 auto 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #000;
}

.site-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
}

.site-title:hover {
  background: #000;
  color: #fff;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}

.site-footer {
  max-width: 800px;
  margin: 2rem auto 0;
  padding-top: 1rem;
  border-top: 2px solid #000;
  font-size: 0.875rem;
}

/* Post card */
.post-card {
  border: 2px solid #000;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.post-card h2 {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.post-card .post-date {
  font-size: 0.8125rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.post-card .post-excerpt {
  font-size: 0.9375rem;
}

.post-card .post-excerpt p {
  display: inline;
}

/* Article post */
.article-header {
  margin-bottom: 1.5rem;
}

.article-header h1 {
  font-size: 1.75rem;
  margin-bottom: 0.25rem;
}

.article-header .post-date {
  font-size: 0.8125rem;
  color: #555;
}

.article-body {
  border: 2px solid #000;
  padding: 1.25rem;
}

.article-body h2 {
  font-size: 1.375rem;
  margin: 1.5rem 0 0.5rem;
}

.article-body h3 {
  font-size: 1.125rem;
  margin: 1.25rem 0 0.5rem;
}

.article-body p {
  margin-bottom: 1rem;
}

.article-body ul, .article-body ol {
  margin: 0 0 1rem 1.5rem;
}

.article-body li {
  margin-bottom: 0.25rem;
}

.article-body blockquote {
  border-left: 4px solid #000;
  padding-left: 1rem;
  margin: 0 0 1rem;
  font-style: italic;
}

.article-body hr {
  border: none;
  border-top: 2px solid #000;
  margin: 1.5rem 0;
}

/* Code */
.article-body code {
  font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", "Courier New", monospace;
  font-size: 0.875em;
  background: #f4f4f4;
  border: 1px solid #000;
  padding: 0.1em 0.3em;
}

.article-body pre {
  border: 2px solid #000;
  background: #f4f4f4;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.article-body pre code {
  border: none;
  background: none;
  padding: 0;
  font-size: 0.8125rem;
}

/* Code highlight overrides */
.codehilite {
  border: 2px solid #000;
  background: #f4f4f4;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.codehilite pre {
  border: none;
  padding: 0;
  margin: 0;
  background: none;
}

.codehilite .hll { background-color: #ffffcc; }
.codehilite .c { color: #3D7B7B; font-style: italic; }
.codehilite .k { color: #000; font-weight: bold; }
.codehilite .o { color: #000; }
.codehilite .cm { color: #3D7B7B; font-style: italic; }
.codehilite .cp { color: #9C6500; }
.codehilite .c1 { color: #3D7B7B; font-style: italic; }
.codehilite .cs { color: #3D7B7B; font-style: italic; }
.codehilite .gd { color: #A00000; }
.codehilite .ge { font-style: italic; }
.codehilite .gr { color: #FF0000; }
.codehilite .gh { color: #000080; font-weight: bold; }
.codehilite .gi { color: #00A000; }
.codehilite .go { color: #888; }
.codehilite .gp { color: #000080; font-weight: bold; }
.codehilite .gs { font-weight: bold; }
.codehilite .gu { color: #800080; font-weight: bold; }
.codehilite .gt { color: #0044DD; }
.codehilite .kc { color: #000; font-weight: bold; }
.codehilite .kd { color: #000; font-weight: bold; }
.codehilite .kn { color: #000; font-weight: bold; }
.codehilite .kp { color: #000; font-weight: bold; }
.codehilite .kr { color: #000; font-weight: bold; }
.codehilite .kt { color: #902000; }
.codehilite .m { color: #177500; }
.codehilite .s { color: #C41A16; }
.codehilite .na { color: #000; }
.codehilite .nb { color: #000; }
.codehilite .nc { color: #000; font-weight: bold; }
.codehilite .no { color: #000; }
.codehilite .nd { color: #000; font-weight: bold; }
.codehilite .ni { color: #000; }
.codehilite .ne { color: #000; font-weight: bold; }
.codehilite .nf { color: #000; }
.codehilite .nl { color: #000; }
.codehilite .nn { color: #000; font-weight: bold; }
.codehilite .nt { color: #000; font-weight: bold; }
.codehilite .nv { color: #000; }
.codehilite .ow { color: #000; font-weight: bold; }
.codehilite .w { color: #bbb; }
.codehilite .mf { color: #177500; }
.codehilite .mh { color: #177500; }
.codehilite .mi { color: #177500; }
.codehilite .mo { color: #177500; }
.codehilite .sb { color: #C41A16; }
.codehilite .sc { color: #C41A16; }
.codehilite .sd { color: #C41A16; }
.codehilite .s2 { color: #C41A16; }
.codehilite .se { color: #C41A16; }
.codehilite .sh { color: #C41A16; }
.codehilite .si { color: #C41A16; }
.codehilite .sx { color: #C41A16; }
.codehilite .sr { color: #C41A16; }
.codehilite .s1 { color: #C41A16; }
.codehilite .ss { color: #C41A16; }

/* Pagination */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid #000;
}

.pagination a {
  font-weight: 700;
}

.pagination .page-info {
  font-size: 0.875rem;
  color: #555;
}

/* Tags */
.tags {
  margin-top: 0.75rem;
}

.tag {
  display: inline-block;
  border: 2px solid #000;
  padding: 0.1rem 0.5rem;
  font-size: 0.75rem;
  margin-right: 0.25rem;
  margin-bottom: 0.25rem;
  text-decoration: none;
}

.tag:hover {
  background: #000;
  color: #fff;
}

/* Responsive */
@media (max-width: 600px) {
  body {
    padding: 1rem 0.5rem;
  }
  .article-body, .post-card {
    padding: 0.75rem;
  }
  .article-header h1 {
    font-size: 1.375rem;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: add brutalist CSS stylesheet"
```

---

### Task 3: generate.py — Core Logic

**Files:**
- Create: `generate.py`

This task implements the core logic: reading markdown files, parsing front matter, converting to HTML, and building the output.

- [ ] **Step 1: Write generate.py with imports and helpers**

```python
import os
import re
import shutil
from datetime import datetime

import markdown
import yaml


POSTS_PER_PAGE = 10
MDS_DIR = "mds"
POSTS_DIR = "posts"
INDICES_DIR = "indices"


def parse_front_matter(content):
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content.strip()
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        meta = {}
    body = parts[2].strip()
    return meta if isinstance(meta, dict) else {}, body


def slug_from_filename(filename):
    return os.path.splitext(filename)[0]


def extract_excerpt(html):
    match = re.search(r"<p>(.*?)</p>", html, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def read_md_files():
    posts = []
    if not os.path.isdir(MDS_DIR):
        print(f"Error: {MDS_DIR}/ directory not found")
        return posts
    for fname in os.listdir(MDS_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(MDS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            raw = f.read()
        meta, body = parse_front_matter(raw)
        title = meta.get("title", slug_from_filename(fname))
        date_str = meta.get("date", "")
        if isinstance(date_str, datetime):
            date = date_str
        elif isinstance(date_str, str):
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                date = datetime.fromtimestamp(os.path.getmtime(fpath))
        else:
            date = datetime.fromtimestamp(os.path.getmtime(fpath))
        tags = meta.get("tags", [])
        posts.append({
            "slug": slug_from_filename(fname),
            "title": title,
            "date": date,
            "tags": tags if isinstance(tags, list) else [],
            "body": body,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts
```

- [ ] **Step 2: Add markdown conversion function**

```python
MD = markdown.Markdown(extensions=[
    "extra",
    "codehilite",
    "toc",
    "sane_lists",
], output_format="html5")


def md_to_html(md_text):
    MD.reset()
    return MD.convert(md_text)
```

- [ ] **Step 3: Add HTML template rendering**

```python
def render_post_html(post, html_body):
    date_str = post["date"].strftime("%B %d, %Y")
    tags_html = ""
    if post["tags"]:
        tag_links = "".join(
            f'<a class="tag" href="/">{t}</a>'
            for t in post["tags"]
        )
        tags_html = f'<div class="tags">{tag_links}</div>'

    content = f"""
<article class="article-header">
  <h1>{post["title"]}</h1>
  <p class="post-date">{date_str}</p>
  {tags_html}
</article>
<div class="article-body">
{html_body}
</div>"""
    return wrap_html(post["title"], content)


def render_index_page(posts, page_num, total_pages):
    cards = []
    for p in posts:
        html_body = md_to_html(p["body"])
        excerpt = extract_excerpt(html_body)
        date_str = p["date"].strftime("%B %d, %Y")
        tags_html = ""
        if p["tags"]:
            tag_links = "".join(
                f'<a class="tag" href="/">{t}</a>'
                for t in p["tags"]
            )
            tags_html = f'<div class="tags">{tag_links}</div>'
        cards.append(f"""<div class="post-card">
  <h2><a href="/posts/{p["slug"]}.html">{p["title"]}</a></h2>
  <p class="post-date">{date_str}</p>
  <div class="post-excerpt"><p>{excerpt}</p></div>
  {tags_html}
</div>""")

    pagination = ""
    if total_pages > 1:
        prev_link = ""
        next_link = ""
        if page_num > 1:
            if page_num == 2:
                prev_link = '<a href="/index.html">&larr; Newer</a>'
            else:
                prev_link = f'<a href="/{INDICES_DIR}/index{page_num - 1}.html">&larr; Newer</a>'
        if page_num < total_pages:
            next_link = f'<a href="/{INDICES_DIR}/index{page_num + 1}.html">Older &rarr;</a>'
        pagination = f"""<div class="pagination">
  <span>{prev_link}</span>
  <span class="page-info">Page {page_num} of {total_pages}</span>
  <span>{next_link}</span>
</div>"""

    content = f"""
<h1>My Blog</h1>
{"".join(cards)}
{pagination}"""
    return wrap_html("My Blog", content)


def wrap_html(title, body):
    return f"""<!DOCTYPE html>
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
    <a class="site-title" href="/">My Blog</a>
  </header>
  <main class="content">
{body}
  </main>
  <footer class="site-footer">
    <p>&copy; {datetime.now().year}</p>
  </footer>
</body>
</html>"""
```

- [ ] **Step 4: Add build orchestration**

```python
def build():
    posts = read_md_files()
    if not posts:
        print("No posts found. Add .md files to mds/ directory.")
        return

    os.makedirs(POSTS_DIR, exist_ok=True)

    for p in posts:
        html_body = md_to_html(p["body"])
        html = render_post_html(p, html_body)
        out_path = os.path.join(POSTS_DIR, f"{p['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Generated: {out_path}")

    total_pages = max(1, (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE)
    for page in range(1, total_pages + 1):
        start = (page - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]
        html = render_index_page(page_posts, page, total_pages)
        if page == 1:
            out_path = "index.html"
        else:
            os.makedirs(INDICES_DIR, exist_ok=True)
            out_path = os.path.join(INDICES_DIR, f"index{page}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Generated: {out_path}")

    print(f"Done. Generated {len(posts)} post(s) across {total_pages} page(s).")


if __name__ == "__main__":
    build()
```

- [ ] **Step 5: Run the generator and verify output**

```bash
pip install -r requirements.txt
python generate.py
```

Expected output:
```
  Generated: posts/hello-world.html
  Generated: posts/中文测试.html
  Generated: index.html
Done. Generated 2 post(s) across 1 page(s).
```

- [ ] **Step 6: Commit**

```bash
git add generate.py
git commit -m "feat: add static site generator"
```

---

### Task 4: Verify Generated Output

- [ ] **Step 1: Check generated files exist**

```bash
ls -la index.html posts/ indices/
```

Expected: `index.html`, `posts/hello-world.html`, `posts/中文测试.html` exist. `indices/` may be empty (only 2 posts, no pagination needed).

- [ ] **Step 2: Check HTML validity of index**

```bash
python3 -c "
with open('index.html') as f:
    html = f.read()
assert '<!DOCTYPE html>' in html
assert '<title>My Blog</title>' in html
assert '/style.css' in html
assert 'mathjax' in html
assert 'hello-world.html' in html
assert '中文测试.html' in html
print('index.html looks valid')
"
```

- [ ] **Step 3: Check HTML validity of a post**

```bash
python3 -c "
with open('posts/hello-world.html') as f:
    html = f.read()
assert '<!DOCTYPE html>' in html
assert '<title>Hello World</title>' in html
assert '/style.css' in html
assert 'mathjax' in html
assert 'codehilite' in html
print('hello-world.html looks valid')
"
```

- [ ] **Step 4: Check Chinese post**

```bash
python3 -c "
with open('posts/中文测试.html') as f:
    html = f.read()
assert '<title>中文测试文章</title>' in html
print('中文测试.html looks valid')
"
```

- [ ] **Step 5: Verify git status shows generated files as expected**

```bash
git status
```

Expected: `index.html` and `posts/` shown as untracked (since they're in .gitignore they shouldn't appear — verify .gitignore is working). If they show up, confirm .gitignore is correct.
