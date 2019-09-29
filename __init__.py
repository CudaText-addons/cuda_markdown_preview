import sys
import os
import webbrowser
import tempfile
from cudatext import *

sys.path.insert(0, os.path.dirname(__file__)) # insert, so OS's module won't be used
import markdown
from .cuda_markdown_options import ext
md = markdown.Markdown(extensions=ext)

dir_temp = os.path.join(tempfile.gettempdir(), 'cuda_markdown_preview')


class Command:

    def __init__(self):

        if not os.path.isdir(dir_temp):
            os.mkdir(dir_temp)

    def on_exit(self, ed_self):

        if os.path.isdir(dir_temp):
            for f in os.listdir(dir_temp):
                os.remove(os.path.join(dir_temp, f))
        os.rmdir(dir_temp)


    def run(self):

        text = ed.get_text_all()
        if not text: return

        text = md.convert(text)
        fn_ed = ed.get_filename()
        if not fn_ed:
            msg_status('Cannot preview untitled document')
            return
        fn_temp = os.path.join(dir_temp, os.path.basename(fn_ed+'.html'))

        with open(fn_temp, 'w') as f:
            f.write(text)

        if os.path.isfile(fn_temp):
            msg_status('Opening HTML preview...')
            webbrowser.open_new_tab(fn_temp)
        else:
            msg_status('Cannot convert document to HTML')
