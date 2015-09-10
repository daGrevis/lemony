from math import ceil


def align_left(text):
    return "%{l}" + text


def align_center(text):
    return "%{c}" + text


def align_right(text):
    return "%{r}" + text


def draw_line_over(text):
    return "%{+o}" + text + "%{-o}"


def draw_line_under(text):
    return "%{+u}" + text + "%{-u}"


def to_bar_color_format(color):
    """
    From #RRGGBB to #FFRRGGBB if it's hex, otherwise pass-through.
    """
    if color[0] == "#":
        return "#FF" + color[1:]
    else:
        return color


def set_foreground_color(text, hex_color):
    return ("%{F" + to_bar_color_format(hex_color) + "}" +
            text +
            "%{F-}")


def set_background_color(text, hex_color):
    return ("%{B" + to_bar_color_format(hex_color) + "}" +
            text +
            "%{B-}")


def set_font(text, font_index):
    return ("%{T" + str(font_index) + "}" +
            text +
            "%{T-}")


def set_bold_font(text):
    return set_font(text, 2)


def progress_bar(value, parts_total=5, used_char="=", empty_char="-"):
    value = int(value)

    step = 100 / parts_total
    parts_used = ceil(value / step)
    parts_empty = parts_total - parts_used


    empty_parts = [used_char * parts_used]
    used_parts = [empty_char * parts_empty]
    return "".join(empty_parts) + set_bold_font("".join(used_parts))


class BaseWidget(object):

    def is_available(self):
        return True

    def render(self):
        raise NotImplementedError()


def render_widgets(widgets, raise_exceptions=False):
    for w in widgets:
        if not w.is_available():
            continue

        try:
            yield w.render()
        except Exception:
            if raise_exceptions:
                raise