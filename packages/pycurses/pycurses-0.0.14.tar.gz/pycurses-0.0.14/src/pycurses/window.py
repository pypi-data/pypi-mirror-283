import curses

from pycurses.utils.general import fix_text_to_width, log
from pycurses.colors import CursesColors

class Window:

    """
        col, row = coordinates of the top left position of the window
        height, width = self explanatory
        parent = parent window
    """

    def __init__(self, parent=None, stdscr=None, colors=None, defaultchar=' ', defaultattr=0):
        self.parent = parent
        self.stdscr = stdscr
        if self.parent:
            self.stdscr = self.parent.stdscr
        self.changed = []
        self.children = []
        self.colors = colors
        self.col = 0
        self.row = 0
        self.height = 1
        self.width = 1
        self.default_char = (defaultchar, defaultattr)
        self.data = [[self.default_char for i in range(self.width)] for j in range(self.height)]
        self.set_all_changed()
        self.to_delete = False
        self.mn_width = None
        self.mn_height = None
        self.mx_width = None
        self.mx_height = None
        self.does_need_loop = False
        self.name = str(self.__class__)
        self.title = ''

    def set_title(self, title):
        self.title = title

    def set_name(self, new_name):
        self.name = new_name

    def set_max_height(self, h:int):
        self.mx_height = h

    def set_min_height(self, h:int):
        self.mn_height = h

    def set_max_width(self, w:int):
        self.mx_width = w

    def set_min_width(self, w:int):
        self.mn_width = w

    def max_height(self):
        return self.mx_height

    def max_width(self):
        return self.mx_width

    def min_height(self):
        return self.mn_height

    def min_width(self):
        return self.mn_width

    def set_needs_loop(self, loops:bool):
        self.does_need_loop = loops

    def needs_loop(self) -> bool:
        return self.does_need_loop

    def set_pos(self, col, row):
        self.col = col
        self.row = row
        self.set_all_changed()

    def resize(self, width, height):
        self.changed = []

        width_diff = width - self.width
        height_diff = height - self.height

        if width_diff != 0:
            if width_diff > 0:
                new_row = [self.default_char for i in range(width_diff)]
                self.data = [r + new_row for r in self.data]
            else:
                self.data = [r[:width_diff] for r in self.data]
        if height_diff != 0:
            if height_diff > 0:
                new_row = [self.default_char for i in range(width)]
                self.data = self.data + [new_row for r in range(height_diff)]
            else:
                self.data = self.data[:height_diff]

        self.width = width
        self.height = height

        '''
        if self.title:
            title_len = len(self.title)
            diff = self.width - title_len
            new_row = []
            title_string = ' '*(diff // 2) + self.title + ' '*((diff % 2) + (diff // 2))
            assert len(title_string) == self.width
            self.data[0] = [(i, curses.A_UNDERLINE) for i in title_string]
        '''

        self.refresh(self.stdscr, force=True)

    def delete(self):
        self.to_delete = True

    def set_changed(self, row, col):
        self.changed.append((row, col))

    def get_changed(self):
        return self.changed

    def update_value(self, row, col, value, modifier):
        if row < len(self.data):
            if col < len(self.data[row]):
                new_tup = (value, modifier)
                if self.data[row][col] != new_tup:
                    self.data[row][col] = new_tup
                    self.set_changed(row, col)


    def draw_box(self, col, row, height, width, modifier=0,
                    topline='-', bottomline='-', rightline='|', leftline='|',
                    tl='+', tr='+', bl='+', br='+', fill=''):
        for i in range(1, width-1):
            self.update_value(row , col + i, topline, modifier)
            self.update_value(row + height - 1, col + i, bottomline, modifier)

        for i in range(1, height-1):
            self.update_value(row + i, col, leftline, modifier)
            self.update_value(row + i, col + width - 1, rightline, modifier)

        self.update_value(row, col, tl, modifier)
        self.update_value(row, col + width - 1, tr, modifier)
        self.update_value(row + height - 1, col, bl, modifier)
        self.update_value(row + height - 1, col + width - 1, br, modifier)

        if fill:
            for r in range(row+1, row+height - 1):
                for c in range(col+1, col + width - 1):
                    self.update_value(r, c, fill, modifier)

    def draw_button(self, col, row, content, **kwargs):
        body = ' {} '.format(content)
        self.draw_box(col, row, 3, len(body) + 2)
        for i in range(len(body)):
            self.update_value(row+1, col + i + 1, body[i], kwargs.get('modifier', 0))

    def draw_border(self, modifier=0, title="",
                    topline='-', bottomline='-', rightline='|', leftline='|',
                    tl='+', tr='+', bl='+', br='+'):
        self.draw_box(0, 0, self.height, self.width, modifier=modifier,
                        topline=topline, bottomline=bottomline, rightline=rightline,
                        leftline=leftline, tl=tl, tr=tr, bl=bl, br=br)
        if title:
            t = " {} ".format(title)
            for i in range(len(t)):
                self.update_value(0, i + 2, t[i], modifier | curses.A_REVERSE)

    def draw_text(self, text, row, col, mod):
        for i in range(len(text)):
            self.update_value(row, col+i, text[i], mod)

    def draw_text_box(self, text, row, col, height, width, alignment='l', mod=0):
        lines = fix_text_to_width(text, width, alignment=alignment)
        for r in range(min(height, len(lines))):
            line = lines[r]
            for i in range(len(line)):
                self.update_value(row + r, col + i, line[i], mod)

    def set_all_changed(self):
        for r in range(self.height):
            for c in range(self.width):
                self.set_changed(r, c)

    def remove_child(self, child):
        row = child.row
        col = child.col
        width = child.width
        height = child.height
        for r in range(height):
            for c in range(width):
                self.set_changed(row + r, col + c)
        self.children.remove(child)
        self.set_active(self)

    def prerefresh(self):
        pass

    def refresh(self, stdscr, force=False, seen_dict=None):
        self.prerefresh()

        for child in self.children:
            if child.to_delete:
                self.remove_child(child)

        if force:
            self.set_all_changed()

        if not seen_dict:
            seen_dict = {}

        for child in reversed(self.children):
            child.refresh(stdscr, force=force, seen_dict=seen_dict)
            child.update_parent_indices(seen_dict)

        for coords in self.get_changed():
            if not seen_dict.get(coords, False):
                val, mod = self.get_value(*coords)
                row, col = self.get_scr_indices(*coords)
                try:
                    stdscr.addch(row, col, ord(val), mod)
                except:
                    pass
        self.changed = []

    def get_scr_indices(self, row, col):
        outRow = self.row + row
        outCol = self.col + col
        if self.parent:
            pr, pc = self.parent.get_scr_indices(0, 0)
            outRow += pr
            outCol += pc
        return (outRow, outCol)

    def update_parent_indices(self, seen):
        for row in range(self.height):
            for col in range(self.width):
                ind = self.get_scr_indices(row, col)
                if ind  not in seen:
                    seen[ind] = True

    def get_value(self, row, col):
        # Needs to include more information; color + modifiers
        return self.data[row][col]

    def add_child(self, window, **kwargs):
        if not window.parent:
            window.parent = self
        if not window.colors:
            window.colors = self.colors
        self.children.append(window)

    def process_char(self, char):
        pass

    def set_active(self, window):
        self.parent.set_active(window)

    def set_cursor(self, row, col):
        self.parent.set_cursor(row, col)

    def has_title(self):
        return bool(self.title)

    def get_title_str(self):
        if self.title:
            half_width = self.width // 2
            return ' ' * half_width + self.title + ' ' * (half_width + self.width % 2)
        else:
            return ''

