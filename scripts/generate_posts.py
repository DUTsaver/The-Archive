from pathlib import Path
from html.parser import HTMLParser
import json

ARCHIVES = Path("Archives")
OUTPUT = Path("posts.json")


class ArticleMetaParser(HTMLParser):
    """Read article-* meta tags from an article HTML file."""

    def __init__(self):
        super().__init__()
        self.meta = {}
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return

        attrs = dict(attrs)
        name = attrs.get("name")
        content = attrs.get("content")

        if not name or content is None:
            return

        if name == "article-tag":
            self.tags.append(content.strip())
        elif name.startswith("article-"):
            self.meta[name] = content.strip()


def normalize_path(path: Path) -> str:
    """Return a GitHub Pages friendly path using forward slashes."""
    return path.as_posix()


def find_article_html(folder: Path):
    """Find the HTML file representing one article folder.

    Preference order:
      1. article.html
      2. index.html
      3. first .html/.htm file alphabetically
    """
    for candidate in (folder / "article.html", folder / "index.html"):
        if candidate.is_file():
            return candidate

    html_files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in {".html", ".htm"}
    )
    return html_files[0] if html_files else None


def resolve_cover(article_file: Path, cover_value: str) -> str:
    """Resolve a cover path relative to the article HTML.

    Example:
      article HTML:
        Archives/MyArticle/article.html
      meta:
        <meta name="article-cover" content="949258.jpg">

    Result:
        Archives/MyArticle/949258.jpg
    """
    if not cover_value:
        return ""

    cover_value = cover_value.split("#", 1)[0]
    cover_value = cover_value.split("?", 1)[0].strip()

    # Keep external images unchanged.
    if cover_value.startswith(("http://", "https://")):
        return cover_value

    while cover_value.startswith("./"):
        cover_value = cover_value[2:]

    cover_path = article_file.parent / cover_value
    return normalize_path(cover_path)


def make_post(article_file: Path, parser: ArticleMetaParser):
    meta = parser.meta

    title = meta.get("article-title", "").strip()
    date = meta.get("article-date", "").strip()

    if not title:
        print(f"[SKIP] {article_file}: missing article-title")
        return None

    if not date:
        print(f"[SKIP] {article_file}: missing article-date")
        return None

    category = meta.get("article-category", "life").strip() or "life"
    author = meta.get("article-author", "").strip()
    excerpt = meta.get("article-excerpt", "").strip()
    symbol = meta.get("article-symbol", "✦").strip() or "✦"

    cover = resolve_cover(
        article_file,
        meta.get("article-cover", "")
    )

    # Keep the [text, kind] format used by your current index.html.
    tags = [
        [tag, category]
        for tag in parser.tags
        if tag
    ]

    return {
        "title": title,
        "date": date,
        "category": category,
        "author": author,
        "excerpt": excerpt,
        "symbol": symbol,
        "cover": cover,
        "tags": tags,
        "url": normalize_path(article_file)
    }


def generate_posts():
    posts = []

    if not ARCHIVES.exists():
        print("[ERROR] Archives/ folder was not found.")
        OUTPUT.write_text("[]\n", encoding="utf-8")
        return

    if not ARCHIVES.is_dir():
        print("[ERROR] Archives is not a folder.")
        OUTPUT.write_text("[]\n", encoding="utf-8")
        return

    # Every first-level folder inside Archives is treated as one article.
    article_folders = sorted(
        (
            p for p in ARCHIVES.iterdir()
            if p.is_dir()
        ),
        key=lambda p: p.name.lower()
    )

    for folder in article_folders:
        article_file = find_article_html(folder)

        if article_file is None:
            print(f"[SKIP] {folder}: no HTML article found")
            continue

        parser = ArticleMetaParser()

        try:
            html = article_file.read_text(encoding="utf-8")
            parser.feed(html)
        except UnicodeDecodeError:
            print(f"[SKIP] {article_file}: file is not UTF-8")
            continue
        except Exception as exc:
            print(f"[SKIP] {article_file}: read failed: {exc}")
            continue

        post = make_post(article_file, parser)
        if post is not None:
            posts.append(post)

    # Newest article first.
    posts.sort(
        key=lambda post: post.get("date", ""),
        reverse=True
    )

    OUTPUT.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"[OK] Generated {OUTPUT}: {len(posts)} articles.")

    for post in posts:
        print(
            f"  - {post['title']} -> {post['url']}"
            f" | cover: {post['cover'] or '(none)'}"
        )


if __name__ == "__main__":
    generate_posts()
