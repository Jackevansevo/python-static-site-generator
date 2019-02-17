import pathlib
from operator import itemgetter
from typing import Sequence
from pygments.formatters import HtmlFormatter

import logging
import shutil
import os
import cmarkgfm
import frontmatter
import jinja2


from blog import ROOT, highlight

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(ROOT, "templates"))
)


def parse_source(source: pathlib.Path) -> frontmatter.Post:
    return frontmatter.load(str(source))


def render_markdown(content: str) -> str:
    content = cmarkgfm.markdown_to_html_with_extensions(
        content, extensions=["table", "autolink", "strikethrough"]
    )
    content = highlight.highlight(content)
    return content


def write_post(post: frontmatter.Post, content: str) -> None:
    target = os.path.join(ROOT, "public/posts/{}/index.html")
    path = pathlib.Path(target.format(post["stem"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    template = jinja_env.get_template("post.html")
    rendered = template.render(post=post, content=content)
    path.write_text(rendered)


def write_posts(build_drafts=False) -> Sequence[frontmatter.Post]:
    posts = []
    for source in pathlib.Path(".").glob("posts/*.md"):
        post = parse_source(source)
        if post.get('draft') and not build_drafts:
            logging.debug(f"Skipped - {post.metadata.get('title')!r}")
            # Skip draft posts
            continue
        content = render_markdown(post.content)
        post["stem"] = source.stem
        write_post(post, content)
        logging.debug(f"Built - {post.metadata.get('title')!r}")
        posts.append(post)
    return posts


def write_index(posts: Sequence[frontmatter.Post]) -> None:
    posts = sorted(posts, key=itemgetter("date"), reverse=True)
    path = pathlib.Path(os.path.join(ROOT, "public/index.html"))
    template = jinja_env.get_template("index.html")
    rendered = template.render(posts=posts)
    path.write_text(rendered)


def write_pygments_style_sheet() -> None:
    """Returns the CSS for the given Pygments style."""
    formatter = HtmlFormatter(style="vs")
    css = formatter.get_style_defs("pre")
    pathlib.Path("./public/static/pygments.css").write_text(css)


def build(build_drafts=False) -> Sequence[frontmatter.Post]:
    # If the public/ exists, we need to wipe everything inside it but
    # avoid deleting the folder itself as it may be a submodule
    shutil.rmtree("public/posts", ignore_errors=True)
    shutil.rmtree("public/static", ignore_errors=True)
    shutil.copytree("static", "public/static")
    write_pygments_style_sheet()
    posts = write_posts(build_drafts)
    write_index(posts)
    return posts
