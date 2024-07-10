
import curses
from pycurses.window import Window
from pycurses.utils.general import log

class ListView(Window):

    def __init__(self, headers=None, row_height=1, parent=None, colors=None, defaultchar=' ', defaultattr=0):
        super().__init__(parent=parent, colors=colors, defaultchar=' ', defaultattr=defaultattr)
        self.row_height = row_height
        self.current_top_index = 0
        self.current_index = 0
        self.horizontal_line = '-'
        self.vertical_line = '|'
        self.header_mod = curses.A_UNDERLINE
        self.set_header_style("Green", "Black")
        if not headers:
            self.headers = []
        else:
            self.headers = headers

    def set_header_style(self, background, foreground):
        self.header_mod = self.colors.get_color_id(background, foreground)

    def get_row_data(self, row_index):
        if row_index % 3 == 0:
            return ['dog', 2, 3920, ' dsf', 2131]
        elif row_index %3 == 1:
            return ['tacos', 99, 20, ' somdsf', 213123423]
        else:
            return ['burger', 98, 201, 'wordup', 3423]


    def get_current_rows(self):
        #TODO Optimize this
        data_rows = []
        if self.headers:
            data_rows.append([''for d in self.headers])
            data_rows.append([str(d).strip() for d in self.headers])
            #raise Exception('asdf')
        upper_lim = self.height - 1 if self.headers else self.height
        for i in range(upper_lim):
            ind = self.current_top_index + i
            data = self.get_row_data(i)
            if data:
                data_rows.append([str(d).strip() if d is not None else '' for d in data])
        return data_rows

    def get_maxs(self, row_data):
        if self.headers:
            row_data.append(self.headers)
        maxs = []
        num_fields = max([len(r) for r in row_data])
        maxs = [1 for i in range(num_fields)]
        for i in range(num_fields):
            for row in row_data:
                if i < len(row):
                    length = len(str(row[i]))
                    if length > maxs[i]:
                        maxs[i] = length
        log("Maxes: {}".format(maxs))
        return maxs

    def refresh(self, stdscr, force=False, seen_dict=None):
        rows = self.get_current_rows()
        if not rows:
            super().refresh(stdscr, force=force, seen_dict=seen_dict)
            return

        maxs = self.get_maxs(rows)

        min_width = sum(maxs)
        bonus_pieces = self.width - min_width - (len(maxs) - 1)

        for i in range(bonus_pieces):
            ind = i % len(maxs)
            maxs[ind] += 1

        str_rows = []
        for row in rows:
            line = ''
            for i in range(len(row)):
                item = row[i]
                diff = maxs[i] - len(item)
                if diff > 0:
                    line += ' ' * diff
                line += item
                if i != len(row) - 1:
                    line += '|'
            str_rows.append(line)

        for i in range(len(str_rows)):
            row = str_rows[i]

            for j in range(self.width):
                if j >= len(row):
                    self.update_value(i, j, ' ', curses.A_UNDERLINE)
                else:
                    mod = curses.A_UNDERLINE
                    if i == 1 if self.title else 0 and len(self.headers) > 0:
                        mod = self.header_mod
                    self.update_value(i, j, row[j], mod)
        #log('\n'.join([''.join([c[0] for c in r]) for r in self.data]))
        super().refresh(stdscr, force=force, seen_dict=seen_dict)



