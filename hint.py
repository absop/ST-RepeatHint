import re

import sublime
import sublime_plugin


repear_hint_regions_key = "RepeatHint"

foldl = lambda f, b, l: foldl(f, f(b, l[0]), l[1:]) if l else b
concat = lambda ls: foldl(lambda x, y: x + y, [], ls)

def get_view_repeat(lines, start_linenum, ignore_empty_line):
    unique_linestrs = []
    repeat_linenums = {}
    first_linenum_by_linestr = {}

    for linenum, linestr in enumerate(lines, start_linenum):
        if (not ignore_empty_line or
            ignore_empty_line and len(linestr) > 0):
            if linestr not in first_linenum_by_linestr:
                first_linenum_by_linestr[linestr] = linenum
                unique_linestrs.append(linestr)
            else:
                first_linenum = first_linenum_by_linestr[linestr]
                if first_linenum not in repeat_linenums:
                    repeat_linenums[first_linenum] = []
                repeat_linenums[first_linenum].append(linenum)
    return unique_linestrs, repeat_linenums

def get_view_lines(view):
    if view.has_non_empty_selection_region():
        region = view.sel()[0]
        start_linenum = view.rowcol(region.begin())[0] + 1
    else:
        region = sublime.Region(0, view.size())
        start_linenum = 1
    lines = view.substr(region).rstrip('\n').split('\n')
    return lines, region, start_linenum

def get_view_data(view, ignore_empty_line):
    lines, region, start_linenum = get_view_lines(view)
    firsts, repeat_linenums = get_view_repeat(
        lines, start_linenum, ignore_empty_line)
    return region, start_linenum, firsts, repeat_linenums

def get_view_repeat_lines(view, ignore_empty_line):
    region, start_linenum, _, repeat_linenums = get_view_data(
        view, ignore_empty_line)
    lines = view.lines(region)
    repeat_lines = []
    for linenums in repeat_linenums.values():
        for linenum in linenums:
            repeat_lines.append(lines[linenum - start_linenum])
    return repeat_lines


class RemoveRepeatLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, ignore_empty_line=False):
        region, _, firsts, _ = get_view_data(self.view, ignore_empty_line)

        self.view.replace(edit, region, '\n'.join(firsts))
        self.view.erase_regions(repear_hint_regions_key)


class ShowRepeatLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, ignore_empty_line=True):
        repeat_linenums = get_view_data(self.view, ignore_empty_line)[3]
        if len(repeat_linenums) > 0:
            first_linenums = sorted(repeat_linenums)[:30]
            width = len(str(first_linenums[-1]))
            hint_text = "Format: First Arise Line: Repeat Arise Lines\n"
            hint_text += '\n'.join("%*d: %s" %
                (width, k, str(repeat_linenums[k])) for k in first_linenums)
            if len(repeat_linenums) > 30:
                hint_text += '\n...'
        else:
            hint_text = '***********There are no repeat lines***********'
        sublime.message_dialog(
            "***************Repeat Lines Hint***************\n" + hint_text)


class MarkRepeatLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, ignore_empty_line=False):
        opts = sublime.load_settings("RepeatHint.sublime-settings")
        icon_color = opts.get("icon_color", "red")
        icon_shape = opts.get("icon_shape", "dot")
        icon_scope = {
            "red": "region.redish",
            "pink": "region.pinkish",
            "blue": "region.bluish",
            "green": "region.greenish",
            "orange": "region.orangish",
            "purple": "region.purplish",
            "yellow": "region.yellowish"
        }.get(icon_color, icon_color)

        self.view.erase_regions(repear_hint_regions_key)
        self.view.add_regions(
            repear_hint_regions_key,
            get_view_repeat_lines(self.view, ignore_empty_line),
            scope=icon_scope,
            icon=icon_shape,
            flags=(sublime.DRAW_EMPTY|
                   sublime.DRAW_NO_OUTLINE|sublime.DRAW_NO_FILL))


class UnmarkRepeatLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_regions(repear_hint_regions_key)


class SelectRepeatLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, ignore_empty_line=False):
        regions = get_view_repeat_lines(self.view, ignore_empty_line)
        self.view.sel().add_all(regions)
