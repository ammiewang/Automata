import gi
from automata.dfa import state, path, DFA
from display.dfa_regex_window import AnsWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RandWindow(Gtk.Window):
    def __init__(self, d):
        Gtk.Window.__init__(self, title="Randomized Regex?")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        hbox = Gtk.Box(spacing=6)
        self.grid.attach(hbox, 0, 0, 1, 1)

        rand_button = Gtk.Button(label="Randomized RegEx?")
        hbox.pack_start(rand_button, True, True, 0)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        hbox.pack_start(self.switch, True, True, 0)

        self.enter = Gtk.Button(label='Enter')
        self.grid.attach(self.enter, 0, 1, 1, 1)
        self.enter.connect("clicked", self.enter_regex, d)

    def enter_regex(self, button, d):
        if self.switch.get_active():
            d.randomized = True
            res = d.all_regex()
            self.grid.remove_row(1)
            self.res_row = Gtk.Box(spacing=6)
            self.res_button = Gtk.Button(label="RegEx:")
            self.res_row.pack_start(self.res_button, True, True, 0)
            self.res_ent = Gtk.Entry()
            self.res_ent.set_text(res)
            self.res_row.pack_start(self.res_ent, True, True, 0)
            self.grid.attach(self.res_row, 0, 1, 1, 1)
            self.grid.show_all()
        else:
            d.randomized = False
            Gtk.main_quit()

def rand_window(d):
    win = RandWindow(d)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    if not d.randomized:
        d.all_regex(randomized_left_out=False, window=True)
        win = AnsWindow(d.regex)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    print('RegEx: ', d.regex)
