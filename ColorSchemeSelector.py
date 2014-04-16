import sublime, sublime_plugin
import os, fnmatch
from glob import iglob
from random import choice

class SelectColorSchemeCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        if int(sublime.version()) > 3000:
            color_schemes = sublime.find_resources("*.tmTheme")
        else:
            color_schemes = list(self.find_color_schemes(sublime.packages_path(), '*.tmTheme'))

        current_scheme_index = self.current_scheme_index(color_schemes)

        def on_done(index):
            if index >= 0:
                self.set_color_scheme(color_schemes[index])
            else:
                self.set_color_scheme(color_schemes[current_scheme_index])

        if 'random' in kwargs:
            self.set_color_scheme(choice(color_schemes))
        elif 'direction' in kwargs:
            self.move_color_scheme(color_schemes, kwargs['direction'])
        else:
            items = [[os.path.basename(_), _] for _ in color_schemes]
            if int(sublime.version()) > 3000:
                self.window.show_quick_panel(items, on_done, 0, current_scheme_index, on_done)
            else:
                self.window.show_quick_panel(items, on_done, 0, current_scheme_index)

    def find_color_schemes(self, directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(os.path.basename(sublime.packages_path()), os.path.relpath(os.path.join(root, basename), sublime.packages_path()))
                    yield filename.replace(os.path.sep, os.path.altsep)

    def move_color_scheme(self, color_schemes, direction):
        current_index = self.current_scheme_index(color_schemes)

        if direction == 'previous':
            current_index -= 1
        elif direction == 'next':
            current_index += 1
        else:
            raise ValueError

        if current_index < 0:
            current_index = len(color_schemes) - 1
        elif current_index >= len(color_schemes):
            current_index = 0

        self.set_color_scheme(color_schemes[current_index])

    def current_scheme_index(self, color_schemes):
        current_scheme = self.load_settings().get('color_scheme')
        return color_schemes.index(current_scheme)

    def set_color_scheme(self, color_scheme_path):
        self.load_settings().set('color_scheme', color_scheme_path)
        sublime.save_settings('Preferences.sublime-settings')
        sublime.status_message('SelectColorScheme: ' + color_scheme_path)

    def load_settings(self):
        return sublime.load_settings('Preferences.sublime-settings')
