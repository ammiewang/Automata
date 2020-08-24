import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MenuWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Options")

        self.set_border_width(10)
        #self.set_default_size(300,300)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        option_store = Gtk.ListStore(int, str)
        option_store.append([1, "1. DFA to RegEx"])
        option_store.append([2, "2. Minimize DFA"])
        option_store.append([3, "3. NFA to DFA"])
        option_store.append([4, "4. RegEx to DFA"])
        option_store.append([5, "5. RegEx Complement"])

        self.name_combo = Gtk.ComboBox.new_with_model(option_store)
        renderer_text = Gtk.CellRendererText()
        self.name_combo.pack_start(renderer_text, True)
        self.name_combo.add_attribute(renderer_text, "text", 1)
        #vbox.pack_start(self.name_combo, False, False, 0)
        self.grid.attach(self.name_combo, 0, 0, 1, 1)

        enter = Gtk.Button(label='Enter')
        self.grid.attach(enter, 0, 1, 1, 1)
        enter.connect("clicked", self.enter_menu)

    def enter_menu(self, button):
        tree_iter = self.name_combo.get_active_iter()
        if tree_iter is not None:
            model = self.name_combo.get_model()
            row_id, name = model[tree_iter][:2]
        self.option = row_id
        Gtk.main_quit()
        self.destroy()

def select_window():
    win = MenuWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return win.option

#print(inp_window())
