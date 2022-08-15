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
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
section = 'markdown_preview'

LIVE_SCRIPT = """
<script type="text/javascript">
            function refreshPage () {
                document.location.reload(true);
            }
            window.onload = function () {
                setTimeout(refreshPage, 2000);
            }
</script>
"""


class Command:
    live = False
    live_pause = 10

    def __init__(self):

        if not os.path.isdir(dir_temp):
            os.mkdir(dir_temp)
        self.live = ini_read(fn_config, section, 'autoreload', '0')=='1'

    def on_exit(self, ed_self):

        if os.path.isdir(dir_temp):
            for f in os.listdir(dir_temp):
                os.remove(os.path.join(dir_temp, f))
        os.rmdir(dir_temp)

    def run(self):

        text = ed.get_text_all()
        if not text: return

        text = md.convert(text)
        if self.live:
            text = LIVE_SCRIPT+'\n'+text

        fn_ed = ed.get_filename()
        if not fn_ed:
            msg_status('Cannot preview untitled document')
            return

        fn_temp = os.path.join(dir_temp,
            os.path.basename(os.path.dirname(fn_ed))+'_'+
            os.path.basename(fn_ed)+'.html')
        temp_existed = os.path.isfile(fn_temp)

        with open(fn_temp, 'w', encoding='utf-8') as f:
            f.write(text)

        if os.path.isfile(fn_temp):
            if not self.live or not temp_existed:
                msg_status('Opening HTML preview...')
                webbrowser.open_new_tab(fn_temp)
        else:
            msg_status('Cannot convert Markdown to HTML')

    def config_live(self):

        msg = 'Live update is: %s.\nEnable live update (auto-reload of HTML page + converting of Markdown after each editing)?\n\nNote: this works only in Chromium-based browsers.'\
            %('on' if self.live else 'off')
        opt = msg_box(msg, MB_YESNO+MB_ICONQUESTION) == ID_YES
        if self.live != opt:
            self.live = opt
            ini_write(fn_config, section, 'autoreload', '1' if opt else '0')
            msg_box('Restart CudaText to apply this option.', MB_OK)

    def on_change_slow(self, ed_self):

        if self.live:
            self.run()
