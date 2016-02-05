import sublime
import os
import fnmatch

from collections import deque

server_buffer = deque([])
server_buffer_callback = lambda x: 0

def appendBuffer(text):
    global server_buffer
    global server_buffer_callback
    server_buffer.append(text)
    if len(server_buffer) > 100:
        server_buffer.popleft()
    #server_buffer = server_buffer + text
    server_buffer_callback(text)

def getBuffer(calback):
    global server_buffer
    global server_buffer_callback
    server_buffer_callback = calback
    all = ''
    for elt in server_buffer:
        all += elt
    return all

def is_csharp(view):
    if len(view.sel()) == 0:
        return False
    
    location = view.sel()[0].begin()   
    return view.match_selector(location, 'source.cs')

def get_settings(view, name, default=None):
    settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
    from_plugin = settings.get(name, default)
    return view.settings().get(name, from_plugin)

def active_view():
    return sublime.active_window().active_view()

def project_file_name(view):
    return view.window().project_file_name()

def project_data(view):
    return view.window().project_data()

def current_solution_filepath_or_project_rootpath(view):
    project_file = project_file_name(view)
    if project_file is not None:
        print('project file %s found', project_file)

        data = project_data(view)
        if 'solution_file' not in data:
            raise ValueError('Please specify a path to the solution file in your sublime-project file or delete it')
      
        project_dir = os.path.dirname(project_file)
        solution_file_name = data['solution_file']
        solution_file_path = os.path.join(project_dir, solution_file_name)
        return os.path.abspath(solution_file_path)
    else:
        active_window = sublime.active_window()
        
        if len(active_window.folders()) > 0:
            return active_window.folders()[0] #assume parent folder is opened that contains all project folders eg/Web,ClassLib,Tests

        try:
            return os.path.dirname(active_window.active_view().file_name())
        except Exception:
            print("New file not saved. Can't find path.")
            return None

def save_all_files(window):
    for view in window.views():
        if view.file_name() and view.is_dirty():
            view.run_command("save")

def quote_path(path):
    return '"' + path.strip('"') + '"'