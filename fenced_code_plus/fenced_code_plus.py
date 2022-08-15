from __future__ import absolute_import
from __future__ import unicode_literals

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
import re
from collections import OrderedDict as odict

class FencedCodePlusExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add FencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('fenced_code_block',
                             FencedBlockPreprocessor(md),
                             ">normalize_whitespace")

#To add an argument,
#Add a regex to recognise that argument and it will get passed into kwargs within run(self, lines)
PARAM_DEFAULTS = {'number': '0'}
PARAM_REGEXES = odict(( #Ordered so that 'data-' attrs of html are in deterministic order.
    ('hl_lines', re.compile(r'''hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)''')),
    ('number', re.compile(r'''number=?(?P<number>\d*)?''')),
    ('path', re.compile(r'''path=(?P<quot>"|')(?P<path>.*?)(?P=quot)''')),
))


DATA_TAG = ' data-{key}="{value}"'
class FencedBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*))?[ ]*  # Optional {, and lang
}?[^\n]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
    CODE_WRAP = '<pre><code{lang}{data}>{code}</code></pre>'
    LANG_TAG = ' class="{lang}"'

    def __init__(self, md):
        super(FencedBlockPreprocessor, self).__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                first_line = text[m.start():].split('\n')[0]
                kwargs = {}
                data_tags = []
                for param, regex in PARAM_REGEXES.items():
                    param_m = regex.search(first_line)
                    if param_m:
                        if param_m.group(param):
                            kwargs[param] = param_m.group(param)
                        elif (not param_m.group(param) is None) and param in PARAM_DEFAULTS:
                            kwargs[param] = PARAM_DEFAULTS[param]
                        else:
                            raise Exception("{} needs an argument within \n{}".format(param, first_line))
                        data_tags.append(DATA_TAG.format(key=param, value=kwargs[param]))
                lang = ''
                if m.group('lang') and m.group('lang') not in PARAM_REGEXES:
                    lang = self.LANG_TAG.format(lang=m.group('lang'))

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlight the code
                if self.codehilite_conf:
                    highliter = CodeHilite(
                        m.group('code'),
                        linenums=self.codehilite_conf['linenums'][0],
                        guess_lang=self.codehilite_conf['guess_lang'][0],
                        css_class=self.codehilite_conf['css_class'][0],
                        style=self.codehilite_conf['pygments_style'][0],
                        lang=(m.group('lang') or None),
                        noclasses=self.codehilite_conf['noclasses'][0],
                        hl_lines=parse_hl_lines(kwargs.get('hl_lines'))
                    )

                    code = highliter.hilite()
                else:
                    code = self.CODE_WRAP.format(lang=lang,
                                             data=''.join(data_tags),
                                             code=self._escape(m.group('code')))

                placeholder = self.markdown.htmlStash.store(code, safe=True)
                text = "{}\n{}\n{}".format(text[:m.start()],
                                       placeholder,
                                       text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt

def makeExtension(*args, **kwargs):
    return FencedCodePlusExtension(*args, **kwargs)
