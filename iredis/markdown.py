"""
Markdown render.

use https://github.com/lepture/mistune render to html, then print with my style.
"""

import logging
import mistune
import copy, re
from mistune import Renderer, InlineGrammar, BlockLexer, InlineLexer
from prompt_toolkit import HTML


logger = logging.getLogger(__name__)


class TerminalRender(mistune.Renderer):
    def _to_title(self, text):
        return f"{text}\n{'='*len(text)}\n"

    def paragraph(self, text):
        return text + "\n\n"

    def block_code(self, code, language=None):
        code = "\n".join(["  " + line for line in code.splitlines()])
        return super().block_code(code)

    def header(self, text, level, raw=None):
        if level == 2:
            header_text = self._to_title(text)
            return super().header(header_text, 2)

    def at_title(self, text):
        return self._to_title(text)


class RedisDocLexer(BlockLexer):
    def enable_at_title(self):
        self.rules.at_title = re.compile(r"^@(\w+) *(?:\n+|$)")  # @example
        self.default_rules.insert(0, "at_title")

    def parse_at_title(self, m):
        text = m.group(1)
        self.tokens.append({"type": "heading", "level": 2, "text": text})


renderer = TerminalRender()
block_lexer = RedisDocLexer()
block_lexer.enable_at_title()
markdown_render = mistune.Markdown(renderer, block=block_lexer)


def render(text):
    html_text = markdown_render(text)
    logger.debug("[Document] {}".format(html_text))

    return HTML(html_text)
