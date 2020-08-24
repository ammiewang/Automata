from automata.dfa import state, path, DFA
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AutomatonWindow(Gtk.Window):
    def __init__(self, d, inp_type):
        Gtk.Window.__init__(self, title="Inputs")

        self.set_border_width(10)
        self.automaton_type = inp_type

        self.grid = Gtk.Grid()
        self.add(self.grid)

        label_box = Gtk.Box(spacing=6)
        self.grid.attach(label_box, 0, 0, 1, 1)
        label = Gtk.Label()
        label.set_markup(
            "<b>Instructions</b> \n"
            "States in the resulting DFA/NFA are numbered "
            "from 0 to the number of states -1. "
            "Label the start and accept states as well as "
            "the transitions in the following window "
            "accordingly. Separate start/accept states "
            "and alphabet characters by space. \n"
        )
        label.set_line_wrap(True)
        label.set_max_width_chars(48)
        label.set_justify(Gtk.Justification.LEFT)
        label_box.pack_start(label, True, True, 0)

        self.num_state_box = Gtk.Box(spacing=6)
        self.num_state_button = Gtk.Button(label='Number of states: ')
        self.num_states = Gtk.Entry()
        self.num_state_box.pack_start(self.num_state_button, True, True, 0)
        self.num_state_box.pack_start(self.num_states, False, False, 0)
        self.grid.attach(self.num_state_box, 0, 1, 1, 1)

        self.ss_box = Gtk.Box(spacing=6)
        self.grid.attach(self.ss_box, 0, 2, 1, 1)
        self.ss_button = Gtk.Button(label="Start state(s): ")
        self.ss_box.pack_start(self.ss_button, True, True, 0)
        self.ss = Gtk.Entry()
        self.ss_box.pack_start(self.ss, False, False, 0)

        self.acc_box = Gtk.Box(spacing=6)
        self.grid.attach(self.acc_box, 0, 3, 1, 1)
        self.acc_button = Gtk.Button(label="Accept states: ")
        self.acc_box.pack_start(self.acc_button, True, True, 0)
        self.accs = Gtk.Entry()
        self.acc_box.pack_start(self.accs, False, False, 0)

        self.alph_box = Gtk.Box(spacing=6)
        self.grid.attach(self.alph_box, 0, 4, 1, 1)
        self.alph_button = Gtk.Button(label="Alphabet: ")
        self.alph_box.pack_start(self.alph_button, True, True, 0)
        self.alph = Gtk.Entry()
        self.alph_box.pack_start(self.alph, False, False, 0)

        enter = Gtk.Button(label='Enter')
        self.grid.attach(enter, 0, 5, 1, 1)
        enter.connect("clicked", self.enter_menu, d)

    def enter_menu(self, button, d):
        self.num_states = int(self.num_states.get_text())
        d.states = [state(i) for i in range(self.num_states)]

        if self.automaton_type == 'dfa':
            self.ss = int(self.ss.get_text())
            for s in d.states:
                if s.id == self.ss:
                    d.start_state = s
                    break
        elif self.automaton_type == 'nfa':
            self.ss = self.ss.get_text().split()
            self.ss = {int(s) for s in self.ss}
            for s in d.states:
                if s.id in self.ss:
                    d.start_states.append(s)

        self.accs = self.accs.get_text().split()
        self.accs = {int(acc) for acc in self.accs}
        for s in d.states:
            if s.id in self.accs:
                d.accept_states.append(s)
        d.alphabet = self.alph.get_text().split()
        Gtk.main_quit()
        self.destroy()

class RegExWindow(Gtk.Window):
    def __init__(self, d):
        Gtk.Window.__init__(self, title="Inputs")

        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.exp_box = Gtk.Box(spacing=6)
        self.exp_button = Gtk.Button(label='RegEx: ')
        self.exps = Gtk.Entry()
        self.exp_box.pack_start(self.exp_button, True, True, 0)
        self.exp_box.pack_start(self.exps, False, False, 0)
        self.grid.attach(self.exp_box, 0, 0, 1, 1)

        enter = Gtk.Button(label='Enter')
        self.grid.attach(enter, 0, 6, 1, 1)
        enter.connect("clicked", self.enter_menu, d)

    def enter_menu(self, button, d):
        inp = self.exps.get_text()
        new_inp = inp.replace(' ', '')
        d.regex = new_inp
        Gtk.main_quit()
        self.destroy()

def inp_window(d, inp_type):
    if inp_type == 'dfa' or inp_type == 'nfa':
        win = AutomatonWindow(d, inp_type)
    elif inp_type == 'regex':
        win = RegExWindow(d)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

#inp_window(DFA([]))
