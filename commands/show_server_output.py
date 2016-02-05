import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp
from ..lib.view import OutputPanel

class OmniSharpShowServerOutput(sublime_plugin.TextCommand):
    
    def run(self, edit, testtype='all'):
        output_panel = OutputPanel(sublime.active_window(), "omnisharp_server")
        output_panel.write(helpers.getBuffer(lambda x: output_panel.write(x)))
        sublime.active_window().run_command("show_panel", {"panel": "output.omnisharp_server"})

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())
