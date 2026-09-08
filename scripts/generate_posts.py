from pathlib import Path
from html.parser import HTMLParser
import json


ARCHIVES = Path("Archives")
OUTPUT = Path("posts.json")


class MetaParser(HTMLParser):
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
            self.tags.append(content)
        else:
            self.meta[name] = content


def find_article_html(folder: Path):
    html_files = list(folder.glob("*.html"))

    if not html_files:
        return None

    # 默认使用第一个 HTML 文件
    return html_files[0]


posts = []

if ARCHIVES.exists():

    for folder in sorted(ARCHIVES.iterdir(), reverse=True):

        if not folder.is_dir():
            continue

        article_file = find_article_html(folder)

        if not article_file:
            continue

        parser = MetaParser()

        try:
            parser.feed(
                article_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as e:
            print(f"Failed to read {article_file}: {e}")
            continue

        meta = parser.meta

        title = meta.get("article-title")
        date = meta.get("article-date")

        if not title or not date:
            print(f"Skipped {article_file}: missing title/date")
            continue

        post = {
            "title": title,
            "date": date,
            "category": meta.get(
                "article-category",
                "life"
            ),
            "author": meta.get(
                "article-author",
                ""
            ),
            "excerpt": meta.get(
                "article-excerpt",
                ""
            ),
            "symbol": meta.get(
                "article-symbol",
                "✦"
            ),
            "cover": meta.get(
                "article-cover",
                ""
            ),
            "tags": [
                [tag, meta.get("article-category", "life")]
                for tag in parser.tags
            ],
            "url": str(
                article_file.as_posix()
            )
        }

        posts.append(post)


posts.sort(
    key=lambda x: x["date"],
    reverse=True
)


OUTPUT.write_text(
    json.dumps(
        posts,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print(
    f"Generated {len(posts)} articles."
)