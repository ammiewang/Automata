import gi
from automata.dfa import state, path, DFA

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DNFAWindow(Gtk.Window):
    def __init__(self, d, opt, inp=False):
        Gtk.Window.__init__(self, title="DFA")
        self.opt = opt

        grid = Gtk.Grid()
        self.add(grid)

        alph_buttons = []
        for sym in d.alphabet:
            alph_buttons.append(Gtk.Button(label=sym))

        for i in range(len(alph_buttons)):
            if i == 0:
                grid.attach(alph_buttons[i], 1, 0, 1, 1)
            else:
                grid.attach_next_to(alph_buttons[i], alph_buttons[i-1], Gtk.PositionType.RIGHT, 1, 1)

        state_buttons = []
        for state in d.states:
            if state in d.accept_states:
                if self.opt == 'dfa' and state.id == d.start_state.id or \
                self.opt == 'nfa' and state in d.start_states:
                    state_buttons.append(Gtk.Button(label='=> ' + str(state.id)+' F'))
                else:
                    state_buttons.append(Gtk.Button(label= str(state.id)+' F'))
            else:
                if self.opt == 'dfa' and state.id == d.start_state.id or \
                self.opt == 'nfa' and state in d.start_states:
                    state_buttons.append(Gtk.Button(label='=> ' + str(state.id)))
                else:
                    state_buttons.append(Gtk.Button(label= str(state.id)))

        for i in range(len(state_buttons)):
            if i == 0:
                grid.attach(state_buttons[i], 0, 1, 1, 1)
            else:
                grid.attach_next_to(state_buttons[i], state_buttons[i-1], Gtk.PositionType.BOTTOM, 1, 1)

        ops = []
        ents = {}
        for i in range(len(state_buttons)):
            op = []
            ents[i] = []
            for j in range(len(alph_buttons)):
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                ent = Gtk.Entry()
                if inp and d.alphabet[j] in d.states[i].outpaths:
                    ent.set_text(str(d.states[i].outpaths[d.alphabet[j]].id))
                ents[i].append(ent)
                vbox.pack_start(ent, True, True, 0)
                op.append(vbox)
                if j == 0:
                    grid.attach(op[j], 1, i+1, 1, 1)
                else:
                    grid.attach_next_to(op[j], op[j-1], Gtk.PositionType.RIGHT, 1, 1)
            ops.append(op)

        self.alph_buttons = alph_buttons
        self.state_buttons = state_buttons
        self.ops = ops
        self.ents = ents
        enter_button = Gtk.Button(label='Enter')
        grid.attach(enter_button, 0, len(state_buttons)+1, len(alph_buttons)+1, 1)
        enter_button.connect("clicked", self.enter_dfa, d.states, d.alphabet)

    def enter_dfa(self, button, states, alphabet):
        for key in self.ents:
            count = 0
            for ent in self.ents[key]:
                if len(ent.get_text()) != 0:
                    if self.opt == 'dfa':
                        inp = int(ent.get_text())
                        states[key].outpaths[alphabet[count]] = states[inp]
                    elif self.opt == 'nfa':
                        inps = ent.get_text().split()
                        inps = [states[int(i)] for i in inps]
                        states[key].outpaths[alphabet[count]] = inps
                count += 1

        for s in states:
            if self.opt == 'dfa':
                print('state: ', s.id, ', outpaths: ', [(k, s.outpaths[k].id) for k in s.outpaths])
            elif self.opt == 'nfa':
                print('state: ', s.id, ', outpaths: ', [(k, [x.id for x in v]) for k,v in s.outpaths.items()])
        print('\n')

        Gtk.main_quit()


def dnfa_window(d, opt, inp=False):
    win = DNFAWindow(d, opt, inp)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
