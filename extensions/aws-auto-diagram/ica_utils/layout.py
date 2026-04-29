class Grid:
    """Lays out cells in rows x columns with variable or uniform sizing."""

    def __init__(self, origin_x, origin_y, col_widths, row_heights,
                 col_gap=10, row_gap=15,
                 padding_top=30, padding_right=15, padding_bottom=15, padding_left=15):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.col_gap = col_gap
        self.row_gap = row_gap
        self.padding_top = padding_top
        self.padding_right = padding_right
        self.padding_bottom = padding_bottom
        self.padding_left = padding_left

        # Accept int (uniform) or list (per-column)
        if isinstance(col_widths, (int, float)):
            self._col_widths = None
            self._uniform_width = col_widths
        else:
            self._col_widths = list(col_widths)
            self._uniform_width = None

        # Accept int (uniform) or list (per-row)
        if isinstance(row_heights, (int, float)):
            self._row_heights = None
            self._uniform_height = row_heights
        else:
            self._row_heights = list(row_heights)
            self._uniform_height = None

    def col_width(self, col):
        """Width of a specific column."""
        if self._col_widths is not None:
            return self._col_widths[col]
        return self._uniform_width

    def row_height(self, row):
        """Height of a specific row."""
        if self._row_heights is not None:
            return self._row_heights[row]
        return self._uniform_height

    def cell_position(self, row, col):
        """Absolute position (x, y) for the cell at (row, col)."""
        x = self.origin_x + self.padding_left
        for c in range(col):
            x += self.col_width(c) + self.col_gap
        y = self.origin_y + self.padding_top
        for r in range(row):
            y += self.row_height(r) + self.row_gap
        return (x, y)

    def bounds(self, num_rows, num_cols):
        """Total (width, height) of the grid including padding."""
        content_width = sum(self.col_width(c) for c in range(num_cols))
        content_width += max(0, num_cols - 1) * self.col_gap
        content_height = sum(self.row_height(r) for r in range(num_rows))
        content_height += max(0, num_rows - 1) * self.row_gap
        width = self.padding_left + content_width + self.padding_right
        height = self.padding_top + content_height + self.padding_bottom
        return (width, height)


class Stack:
    """Stacks containers vertically with spacing."""

    def __init__(self, x, y, gap=25):
        self.x = x
        self.y = y
        self.gap = gap
        self.cursor_y = y

    def next_position(self):
        """Position (x, y) for the next container."""
        return (self.x, self.cursor_y)

    def advance(self, height):
        """Move cursor down by height + gap."""
        self.cursor_y += height + self.gap

    @property
    def max_width(self):
        """Maximum width seen so far (tracks widest item)."""
        return getattr(self, '_max_width', 0)

    @max_width.setter
    def max_width(self, value):
        self._max_width = value

    def track_width(self, width):
        """Track the widest item added to the stack."""
        if width > self.max_width:
            self.max_width = width


class Row:
    """Lays out containers horizontally with spacing."""

    def __init__(self, x, y, gap=20):
        self.x = x
        self.y = y
        self.gap = gap
        self.cursor_x = x
        self._max_height = 0

    def next_position(self):
        """Position (x, y) for the next container."""
        return (self.cursor_x, self.y)

    def advance(self, width, height):
        """Move cursor right by width + gap, track max height."""
        self.cursor_x += width + self.gap
        if height > self._max_height:
            self._max_height = height

    @property
    def max_height(self):
        """Tallest item added to the row."""
        return self._max_height

    def bounds(self):
        """Total (width, max_height) of all items placed so far."""
        total_width = self.cursor_x - self.x - self.gap  # subtract trailing gap
        if total_width < 0:
            total_width = 0
        return (total_width, self._max_height)
