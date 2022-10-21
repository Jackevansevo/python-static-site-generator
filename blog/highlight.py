"""Highlights code blocks using Pygments."""

import html.parser
import re

import pygments.formatters
import pygments.lexers

# Make code fences with `python` as the language default to highlighting as
# Python 3.
_LANG_ALIASES = {"python": "python3"}


def highlight(content: str) -> str:
    """Syntax-highlights HTML-rendered Markdown.

    Plucks sections to highlight that conform the the GitHub fenced code info
    string as defined at https://github.github.com/gfm/#info-string.
    """

    formatter = pygments.formatters.HtmlFormatter(nowrap=True)

    code_expr = re.compile(
        r'<pre><code class="language-(?P<lang>.+?)">(?P<code>.+?)' r"</code></pre>",
        re.DOTALL,
    )

    def replacer(match):
        try:
            lang = match.group("lang")
            lang = _LANG_ALIASES.get(lang, lang)
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except ValueError:
            lexer = pygments.lexers.TextLexer()

        code = match.group("code")

        highlighted = pygments.highlight(html.unescape(code), lexer, formatter)

        return "<pre>{}</pre>".format(highlighted)

    result = code_expr.sub(replacer, content)

    return result
