import html
import os
import re
from datetime import date, datetime

import markdown
import yaml


POSTS_PER_PAGE = 10
MDS_DIR = "mds"
POSTS_DIR = "posts"
INDICES_DIR = "indices"

MD = markdown.Markdown(extensions=[
    "extra",
    "codehilite",
    "toc",
    "sane_lists",
], output_format="html5")


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
    return os.path.splitext(os.path.basename(filename))[0]


def extract_excerpt(html):
    match = re.search(r"<p>(.*?)</p>", html, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def md_to_html(md_text):
    MD.reset()
    return MD.convert(md_text)


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
            post_date = date_str
        elif isinstance(date_str, date):
            post_date = datetime(date_str.year, date_str.month, date_str.day)
        elif isinstance(date_str, str):
            try:
                post_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                post_date = datetime.fromtimestamp(os.path.getmtime(fpath))
        else:
            post_date = datetime.fromtimestamp(os.path.getmtime(fpath))
        posts.append({
            "slug": slug_from_filename(fname),
            "title": title,
            "date": post_date,
            "body": body,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_post_html(post, html_body, css_path):
    date_str = post["date"].strftime("%B %d, %Y")

    content = f"""
<article class="article-header">
  <h1>{html.escape(post["title"])}</h1>
  <p class="post-date">{date_str}</p>
</article>
<div class="article-body">
{html_body}
</div>"""
    return wrap_html(post["title"], content.strip(), css_path)


def render_index_page(posts, page_num, total_pages, css_path):
    cards = []
    for p in posts:
        html_body = md_to_html(p["body"])
        excerpt = extract_excerpt(html_body)
        date_str = p["date"].strftime("%B %d, %Y")
        safe_title = html.escape(p["title"])
        cards.append(f"""<div class="post-card">
  <h2><a href="/posts/{p["slug"]}.html">{safe_title}</a></h2>
  <p class="post-date">{date_str}</p>
  <div class="post-excerpt"><p>{excerpt}</p></div>
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
{"".join(cards)}
{pagination}"""
    return wrap_html("xhWang00's Blog", content.strip(), css_path)


def wrap_html(title, body, css_path):
    safe_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="{css_path}">
  <script>
    MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
      }}
    }};
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
  <header class="site-header">
    <a class="site-title" href="/">xhWang00's Blog</a>
  </header>
  <main class="content">
{body}
  </main>
  <footer class="site-footer">
    <p>&copy; {datetime.now().year} - xhWang00</p>
  </footer>
</body>
</html>"""


def build():
    posts = read_md_files()
    if not posts:
        print("No posts found. Add .md files to mds/ directory.")
        return

    os.makedirs(POSTS_DIR, exist_ok=True)

    for p in posts:
        html_body = md_to_html(p["body"])
        html = render_post_html(p, html_body, "../style.css")
        out_path = os.path.join(POSTS_DIR, f"{p['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Generated: {out_path}")

    total_pages = max(1, (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE)
    for page in range(1, total_pages + 1):
        start = (page - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]
        if page == 1:
            css_path = "style.css"
            out_path = "index.html"
        else:
            css_path = "../style.css"
            os.makedirs(INDICES_DIR, exist_ok=True)
            out_path = os.path.join(INDICES_DIR, f"index{page}.html")
        html = render_index_page(page_posts, page, total_pages, css_path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Generated: {out_path}")

    print(f"Done. Generated {len(posts)} post(s) across {total_pages} page(s).")


if __name__ == "__main__":
    build()
