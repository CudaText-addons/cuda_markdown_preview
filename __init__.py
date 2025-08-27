import sys
import os
import tempfile
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

sys.path.insert(0, os.path.dirname(__file__)) # insert, so OS's module won't be used
sys.path.append(os.path.join(os.path.dirname(__file__), 'markdown', 'extensions'))

import markdown
from .cuda_markdown_options import ext
md = markdown.Markdown(extensions=ext)

# avoid /tmp because Firefox cannot open HTML-file from there on Alexey's Ubuntu
if os.name != 'nt':
    tempfile.tempdir = os.path.expanduser('~/tmp')
    os.makedirs(tempfile.tempdir, exist_ok=True)

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

def safe_open_url(url):
    '''
    On Windows 10, app crashes when webbrowser.open* is called with running LSP server.
    '''
    if os.name=='nt':
        import subprocess
        subprocess.Popen(['start', '', url], shell=True)
    else:
        import webbrowser
        webbrowser.open_new_tab(url)


class Command:
    live = False
    live_pause = 10
    live_files = []

    def __init__(self):

        if not os.path.isdir(dir_temp):
            os.mkdir(dir_temp)
        self.live = ini_read(fn_config, section, 'autoreload', '0')=='1'

    def on_exit(self, ed_self):

        if os.path.isdir(dir_temp):
            for f in os.listdir(dir_temp):
                os.remove(os.path.join(dir_temp, f))
        os.rmdir(dir_temp)

    def run(self, only_reload=False):

        text = ed.get_text_all()
        if not text: return

        text = md.convert(text)
        if self.live:
            text = LIVE_SCRIPT+'\n'+text

        fn_ed = ed.get_filename()
        if not fn_ed:
            msg_status(_('Cannot preview untitled document'))
            return
        self.live_files.append(fn_ed)

        fn_temp = os.path.join(dir_temp,
            os.path.basename(os.path.dirname(fn_ed))+'@'+
            os.path.basename(fn_ed)+'.html')
        temp_existed = os.path.isfile(fn_temp)

        with open(fn_temp, 'w', encoding='utf-8') as f:
            f.write(text)

        if os.path.isfile(fn_temp):
            if not only_reload:
                if self.live:
                    app_proc(PROC_SET_EVENTS, 'cuda_markdown_preview;on_exit,on_change_slow;Markdown;') 
                msg_status(_('Opening HTML preview...'))
                safe_open_url('file://'+fn_temp)
        else:
            msg_status(_('Cannot convert Markdown to HTML'))

    def config_live(self):

        msg = _('Live update is: %s.\nEnable live update (auto-reload of HTML page + converting of Markdown after each editing)?')\
            %(_('on') if self.live else _('off'))
        opt = msg_box(msg, MB_YESNO+MB_ICONQUESTION) == ID_YES
        if self.live != opt:
            self.live = opt
            ini_write(fn_config, section, 'autoreload', '1' if opt else '0')
            msg_box(_('Restart CudaText to apply this option.'), MB_OK)

    def on_change_slow(self, ed_self):

        if self.live:
            fn = ed_self.get_filename()
            if fn and (fn in self.live_files):
                self.run(True)
