# Repeat Hint
A repeat lines(a line that appears multiple times in the file) reporter for Sublime Text.

This plugin is mainly used to detect duplicate data in the data file (one item per line) and will not be used very often.


## Features（功能）
- Show repeat lines in palette, to copy or goto the first arise line.
- Mark repeat lines in gutter bar
- Clean repeat lines marks
- Select repeat lines
- Remove repeat lines


## Commands （命令）
- RepeatHint: Show Repeat Lines
- RepeatHint: Mark Repeat Lines
- RepeatHint: Mark Repeat Lines (Ignore Empty Lines)
- RepeatHint: Unmark Repeat Lines
- RepeatHint: Select Repeat Lines
- RepeatHint: Remove Repeat Lines


## Method to bind hotkeys.
These commands can be bound to hotkeys
- `remove_repeat_lines`
- `show_repeat_lines`
- `mark_repeat_lines`
- `unmark_repeat_lines`
- `select_repeat_lines`

The only argument for these commands is `ignore_empty_line`, which is a boolean value.
