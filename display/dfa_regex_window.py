import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ToRegExWindow(Gtk.Window):
    def __init__(self, d, s1, s2, left_out):
        Gtk.Window.__init__(self, title="Switch Demo")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.ss_box = Gtk.Box(spacing=6)
        self.grid.attach(self.ss_box, 0, 0, 1, 1)
        self.ss_button = Gtk.Button(label="Start state:")
        self.ss_box.pack_start(self.ss_button, True, True, 0)
        self.ss = Gtk.Entry()
        self.ss_box.pack_start(self.ss, False, False, 0)

        self.es_box = Gtk.Box(spacing=6)
        self.grid.attach(self.es_box, 0, 1, 1, 1)
        self.es_button = Gtk.Button(label="End state:")
        self.es_box.pack_start(self.es_button, True, True, 0)
        self.es = Gtk.Entry()
        self.es_box.pack_start(self.es, False, False, 0)

        self.ss.set_text(str(s1.id))
        self.es.set_text(str(s2.id))

        self.rm_box = Gtk.Box(spacing=6)
        self.grid.attach(self.rm_box, 0, 2, 1, 1)
        self.rm_button = Gtk.Button(label="Choose a state to remove:")
        self.rm_box.pack_start(self.rm_button, True, True, 0)
        self.rm = Gtk.ListStore(int, int)
        i = 0
        set_lo = set(left_out)
        for state in d.states:
            if state not in set_lo:
                self.rm.append([state.id, i])
            i += 1
        self.state_combo = Gtk.ComboBox.new_with_model(self.rm)
        self.renderer_text = Gtk.CellRendererText()
        self.state_combo.pack_start(self.renderer_text, True)
        self.state_combo.add_attribute(self.renderer_text, "text", 0)
        self.rm_box.pack_start(self.state_combo, False, False, True)

        self.new_enter = Gtk.Button(label='Remove State')
        self.grid.attach(self.new_enter, 0, 3, 1, 1)
        self.new_enter.connect("clicked", self.new_enter_regex, d)


    def new_enter_regex(self, button, d):
        tree_iter = self.state_combo.get_active_iter()
        if tree_iter is not None:
            model = self.state_combo.get_model()
            name, id = model[tree_iter][:2]
            print('Removed: ', name)
            d.choice = d.states[id]
            Gtk.main_quit()
            self.destroy()

class AnsWindow(Gtk.Window):
    def __init__(self, regex):
        Gtk.Window.__init__(self, title="Regex")

        res_row = Gtk.Box(spacing=6)
        res_button = Gtk.Button(label="RegEx:")
        res_row.pack_start(res_button, True, True, 0)
        res_ent = Gtk.Entry()
        res_ent.set_text(regex)
        res_row.pack_start(res_ent, True, True, 0)
        self.add(res_row)
