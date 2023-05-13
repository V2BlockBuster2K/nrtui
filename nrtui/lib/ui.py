import urwid


class CustomButton(urwid.Button):
    # Create custom button without '< >'
    def __init__(self, t, fn, d=''):
        super().__init__('', fn, d)
        self._w = urwid.SelectableIcon(t, 0)


def button(t, fn, d=''):
    w = urwid.Button(t, fn, d)
    return w


def checkbox(t, fn):
    w = urwid.CheckBox(t, on_state_change=fn)
    return w
