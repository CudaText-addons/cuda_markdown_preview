import markdown
import re
from fenced_code_plus import FencedCodePlusExtension
import unittest
import pytest

unadorned_code_block_md = """\
```
def foo():
    bar = 4
    return 8
```
"""

unadorned_code_block_html = """\
<pre><code>def foo():
    bar = 4
    return 8
</code></pre>"""

only_language_md = """\
``` python

def foo():
    bar = 4
    return 8
```
"""

only_language_html = """\
<pre><code class="python">
def foo():
    bar = 4
    return 8
</code></pre>"""

only_filename_md = """\
``` path="arbitrary string here"

def foo():
    bar = 4
    return 8
```
"""

only_filename_html = """\
<pre><code data-path="arbitrary string here">
def foo():
    bar = 4
    return 8
</code></pre>"""

only_numbering_md = """\
``` number=3

def foo():
    bar = 4
    return 8
```
"""

only_numbering_html = """\
<pre><code data-number="3">
def foo():
    bar = 4
    return 8
</code></pre>"""

only_numbering_default_md = """\
``` number

def foo():
    bar = 4
    return 8
```
"""

only_numbering_default_html = """\
<pre><code data-number="0">
def foo():
    bar = 4
    return 8
</code></pre>"""

language_hl_lines_md = """\
``` python hl_lines="4 5"

def foo():
    bar = 4
    return 8
```
"""

language_hl_lines_html = """\
<pre><code class="python" data-hl_lines="4 5">
def foo():
    bar = 4
    return 8
</code></pre>"""

language_hl_lines_numbering_md = """\
``` python number hl_lines="4 5"

def foo():
    bar = 4
    return 8
```
"""

language_hl_lines_numbering_html = """\
<pre><code class="python" data-hl_lines="4 5" data-number="0">
def foo():
    bar = 4
    return 8
</code></pre>"""

hl_lines_numbering_filename_md = """\
``` number path="another arbitrary string" hl_lines="4 5"

def foo():
    bar = 4
    return 8
```
"""

hl_lines_numbering_filename_html = """\
<pre><code data-hl_lines="4 5" data-number="0" data-path="another arbitrary string">
def foo():
    bar = 4
    return 8
</code></pre>"""

language_hl_lines_numbering_filename_md = """\
``` python number path="another arbitrary string" hl_lines="4 5"

def foo():
    bar = 4
    return 8
```
"""

language_hl_lines_numbering_filename_html = """\
<pre><code class="python" data-hl_lines="4 5" data-number="0" data-path="another arbitrary string">
def foo():
    bar = 4
    return 8
</code></pre>"""

class TestFencedCodePlus(unittest.TestCase):
    def test_unadorned_code_block(self):
        assert markdown.markdown(unadorned_code_block_md, extensions=[FencedCodePlusExtension()]) ==\
            unadorned_code_block_html

    def test_only_language(self):
        assert markdown.markdown(only_language_md, extensions=[FencedCodePlusExtension()]) ==\
            only_language_html

    def test_only_filename(self):
        assert markdown.markdown(only_filename_md, extensions=[FencedCodePlusExtension()]) ==\
            only_filename_html

    def test_only_numbering(self):
        assert markdown.markdown(only_numbering_md, extensions=[FencedCodePlusExtension()]) ==\
            only_numbering_html

    def test_only_numbering_default(self):
        assert markdown.markdown(only_numbering_default_md, extensions=[FencedCodePlusExtension()]) ==\
            only_numbering_default_html

    def test_language_hl_lines(self):
        assert markdown.markdown(language_hl_lines_md, extensions=[FencedCodePlusExtension()]) ==\
            language_hl_lines_html

    def test_language_hl_lines_numbering_filename(self):
        assert markdown.markdown(language_hl_lines_numbering_filename_md, extensions=[FencedCodePlusExtension()]) ==\
            language_hl_lines_numbering_filename_html


if __name__ == '__main__':
    pytest.main()
