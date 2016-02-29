from cudatext import *
import sys
import os
import webbrowser
import tempfile

sys.path.append(os.path.dirname(__file__))
import markdown

TEMP = 'markdown_preview.html'
INI = 'markdown.cfg'

ext = []
ini = os.path.join(os.path.dirname(__file__), INI)
if os.path.isfile(ini):
    with open(ini) as f:
        d = eval(f.read())
        ext = d['extensions']

md = markdown.Markdown(extensions=ext)

class Command:
    def run(self):
        text = ed.get_text_sel()
        if not text:
            text = ed.get_text_all()
        if not text:
            return

        text = md.convert(text)

        fn = os.path.join(tempfile.gettempdir(), TEMP)
        with open(fn, 'w') as f:
            f.write(text)

        if os.path.isfile(fn):
            msg_status('Opening HTML preview...')
            webbrowser.open_new_tab(fn)
        else:
            msg_status('Cannot convert text to HTML')
