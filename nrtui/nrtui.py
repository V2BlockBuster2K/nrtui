from threading import Thread

import urwid
import urwid.numedit

from .lib.helpers import check_dir, run_as_root
from .lib.jsonparser import JsonConfig
from .lib.loop import Loop
from .lib.ui import CustomButton, button, checkbox


class SaveOverlay(urwid.WidgetWrap):
    def __init__(self, fn):
        self.edit = urwid.Edit(caption='Save as: ', wrap='clip')
        self.save = button('save', fn, 'save')
        self.back = button('back', fn, 'back')
        self.columns = urwid.Columns([self.save, self.back])

        self.pile = urwid.Pile([self.edit, urwid.Divider(), self.columns])

        self._w = urwid.ListBox([urwid.LineBox(self.pile)])

    def get_text(self):
        if self.edit.get_edit_text() == '':
            return 'unnamed'
        else:
            return self.edit.get_edit_text()


class DeleteOverlay(urwid.WidgetWrap):
    def __init__(self, fn):
        self.text = urwid.Text('')
        self.yes = button('yes', fn, 'yes')
        self.no = button('no', fn, 'no')
        self.columns = urwid.Columns([self.yes, self.no])

        self.pile = urwid.Pile([self.text, urwid.Divider(), self.columns])

        self._w = urwid.ListBox([urwid.LineBox(self.pile)])

    def update(self, t):
        self.text.set_text('Delete: ' + t)


class LeftSide(urwid.WidgetWrap):
    def __init__(self, save, save_as, delete):
        self.loop = Loop()

        self.activate = checkbox("enable no recoil", self.activate_l)
        self.ads = checkbox("require ads", self.ads_l)
        self.delay = urwid.numedit.FloatEdit('delay: ', '2')
        self.offset = urwid.numedit.IntegerEdit('offset: ', '2')

        self.save = button('save', save)
        self.save_as = button('save as', save_as)
        self.delete = button('delete', delete)
        self.columns = urwid.Columns([self.save, self.save_as, self.delete])

        self.listbox = urwid.ListBox(
            [self.activate, self.ads, self.delay, self.offset, urwid.Divider(), self.columns])

        self._w = self.listbox

        urwid.connect_signal(self.delay, 'change', self.delay_l)
        urwid.connect_signal(self.offset, 'change', self.offset_l)

        self.thread = Thread(target=self.loop.start,
                             daemon=False, name='nrtui-loop')
        self.thread.start()

    def load(self, d):
        self.ads.set_state(d['ads'])
        self.delay.set_edit_text(d['delay'])
        self.offset.set_edit_text(d['offset'])

    def get_current(self):
        ads = self.ads.get_state()
        delay = self.delay.get_edit_text()
        offset = self.offset.get_edit_text()
        return ads, delay, offset

    # Loop
    def activate_l(self, _, s):
        self.loop.active = s

    def ads_l(self, _, s):
        self.loop.ads = s

    def delay_l(self, _, i):
        if i != '':
            self.loop.delay = i

    def offset_l(self, _, i):
        if i != '':
            self.loop.offset = i


class RightSide(urwid.WidgetWrap):
    def __init__(self, fn):
        self.fn = fn
        self.listbox = urwid.ListBox([])

        self._w = self.listbox

    def update(self, json):
        self.listbox = urwid.ListBox(
            [CustomButton(v, self.fn, v)for k, v in enumerate(json.conf)])

        self._w = self.listbox


class MainWindow(urwid.WidgetWrap):
    def __init__(self):
        self.loaded = None

        self.json = JsonConfig()
        self.json.load()

        self.left = LeftSide(self.save, self.save_as, self.delete)
        self.right = RightSide(self.click)

        self.columns = urwid.Columns(
            [('fixed', 35, urwid.LineBox(self.left)), urwid.LineBox(self.right)])

        self._w = self.columns

        self.saveoverlay = SaveOverlay(self.exit_save_overlay)
        self.deleteoverlay = DeleteOverlay(self.exit_delete_overlay)

        self.initialize()

    def save(self, _, __):
        a, d, o = self.left.get_current()
        self.json.add(self.loaded, a, d, o)

    def save_as(self, _, __):
        self._w = urwid.Overlay(
            self.saveoverlay, self.columns, 'center', 35, 'middle', 5)

    def delete(self, _, __):
        if self.loaded != 'default':
            self.deleteoverlay.update(self.loaded)
            self._w = urwid.Overlay(
                self.deleteoverlay, self.columns, 'center', 35, 'middle', 5)

    def exit_save_overlay(self, _, t):
        if t == 'save':
            a, d, o = self.left.get_current()
            self.json.add(self.saveoverlay.get_text(), a, d, o)
            self.right.update(self.json)
            self._w = self.columns
            self.saveoverlay.edit.set_edit_text('')
        else:
            self._w = self.columns

    def exit_delete_overlay(self, _, t):
        if t == 'yes':
            self.json.delete(self.loaded)
            self.right.update(self.json)
            self._w = self.columns
        else:
            self._w = self.columns

    def click(self, _, d):
        self.loaded = d
        self.left.load(self.json.conf[d])

    def initialize(self):
        self.loaded = 'default'
        self.left.load(self.json.conf['default'])
        self.right.update(self.json)


class App(object):
    def __init__(self):
        self.widget = MainWindow()

        self.loop = urwid.MainLoop(
            self.widget, unhandled_input=self.unhandled_input)

    def unhandled_input(self, key):
        if key == 'ctrl x':
            self.widget.left.loop.stop = True
            raise urwid.ExitMainLoop()

    def start(self):
        self.loop.run()


def main():
    if check_dir():
        run_as_root()
        app = App()
        app.start()


if __name__ == '__main__':
    main()
