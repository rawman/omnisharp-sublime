import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp        
from ..lib.view import OutputPanel

class AppendToServerOutput(sublime_plugin.TextCommand):
    
    def run(self, edit, text):
        output_panel = sublime.active_window().create_output_panel("omnisharp_server")
        output_panel.insert(edit, output_panel.size(), helpers.getBuffer())
        
    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())