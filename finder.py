from Tkinter import Tk                                  # GUI components
from Tkinter import Text, Toplevel                      # Tkinter elements
from Tkinter import StringVar, IntVar                   # Tkinter variables
from Tkinter import BOTH, N, S                          # Directions
from Tkinter import INSERT, END                              # Index positions
from Tkinter import FLAT                                # Reliefs
from ttk import Style, Frame, Button, Scrollbar, Label, Radiobutton, Entry # ttk elements
from PIL import Image, ImageTk
from rounded_corners import config_round_corners
from logic import find
from impot_window import excel_popup


class TextField(object):
    SCROLLBAR_COLUMN = 15

    def __init__(self, row, column, height, label, parent):
        self._row = row
        self._column = column
        self._height = height
        self._parent = parent
        self._label = label
        self._frame = Frame(parent, style="RoundedFrame", padding=10)
        self._define()
        self._display()

    @property
    def frame(self):
        return self._frame

    @property
    def field(self):
        return self._field

    def _define(self):
        self._field = Text(self._frame, font="Times 15", height=self._height, relief=FLAT)
        self._scrollbar = Scrollbar(self._frame, command=self._field.yview)
        self._field.configure(yscrollcommand=self._scrollbar.set)
        self._label = Label(self._parent, width=18, text=self._label)

    def _display(self):
        self._frame.grid(row=self._row, column=self._column)
        self._scrollbar.grid(row=0, column=self.SCROLLBAR_COLUMN, sticky=S+N)
        self._field.grid(row=0, column=0)
        self._label.grid(row=self._row, column=0)
        
    def focus(self):
        self._field.focus()


class FinderApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self._widgets = {}
        self._pos()
        self._bindings()
        self._init_ui()

    def _select_all(self, event):
        """
            Selects all the content of a text field
        """
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return 'break'  # Won't display the character

    def _tab_handler(self, event):
        """
            Pressing tab would fucos the next field.
            The \t char would not be displayed (when jumping from text fields).
        """
        switch = {self._widgets['to_find'].field: self._widgets['glossary'].focus,
                  self._widgets['glossary'].field: self._widgets['button'].focus,
                  self._widgets['button']:  self._widgets['results'].focus,
                  self._widgets['results'].field: self._widgets['not_found'].focus,
                  self._widgets['not_found'].field: self._widgets['to_find'].focus}
        e = switch.get(event.widget)
        if e:
            e()
        return 'break'  # Won't display the character

    def _bindings(self):
        """
            Bind tab behaviour for text fields and buttons
            Binds select all action for text fields
        """
        self.bind_class("Text", "<Control-a>", self._select_all)
        self.bind_class("Text", "<FocusIn>", lambda e: e.widget.master.state(["focus"]))
        self.bind_class("Text", "<FocusOut>", lambda e: e.widget.master.state(["!focus"]))
        self.bind_class("Text", "<Tab>", self._tab_handler)
        self.bind_class("TButton", "<Tab>", self._tab_handler)

    def _pos(self):
        """
            Sizes window to 80% of the screen size and centres it.
        """
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        w = max(sw * 0.8, 1240)
        h = max(sh * 0.8, 655)
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def _input_fields(self):
        self._widgets['to_find'] = TextField(0, 2, 3,  "List of genes to find: ", self)
        self._widgets['glossary'] = TextField(3, 2, 3, "Glossary list: ", self)
        self._widgets['to_find'].focus()

    def _output_fields(self):
        self._widgets['results'] = TextField(9, 2, 7, "Results: ", self)
        self._widgets['not_found'] = TextField(15, 2, 5, "Not found: ", self)

    def _button(self):
        # Define button callback
        def _find():
            source = self._widgets['to_find'].field
            glossary = self._widgets['glossary'].field
            found = self._widgets['results'].field
            not_found = self._widgets['not_found'].field
            find(source, glossary, found, not_found)

        # Define button
        dna_icon = ImageTk.PhotoImage(Image.open("images\dna.png"))
        find_button = Button(self, image=dna_icon, text=" Find", width=10, command=_find,  compound="left")
        find_button.image = dna_icon
        #Display button
        find_button.grid(row=6, column=2)
        # Keep field instances
        self._widgets['button'] = find_button

        #TODO Cleanup and refactor here
        def excel_imp_glossary():
            excel_popup(self._widgets['glossary'].field)
        def excel_imp_tofind():
            excel_popup(self._widgets['to_find'].field)

        xl = Button(self, text="Import Excel", command=excel_imp_tofind)
        xl.grid(row=0, column=10)

        xl2 = Button(self, text="Import Excel", command=excel_imp_glossary)
        xl2.grid(row=3, column=10)

    def _init_ui(self):
        self.parent.title("Aya's Finder")
        self.parent.wm_iconbitmap(r'images\Dna-Helix.ico')
        # Configure style
        Style().configure("TLabel", padding=(15, 5, 0, 5), font='Times 15', background="#333", foreground="#BADA55")
        Style().configure("TRadiobutton", padding=(15, 5, 0, 5), font='Times 15', background="#333", foreground="#BADA55")
        Style().configure("TButton", padding=(0, 0, 0, 1), font='Times 15')
        Style().configure("TFrame", padding=(0, 5, 0, 5), font='Times 15', background="#333")

        images = config_round_corners()     # Assigned to avoid garbage collection
        # Define widgets
        self._input_fields()
        self._output_fields()
        self._button()
        self.pack(fill=BOTH, expand=1)
        # Enter event loop
        self.parent.mainloop()


def main():
    root = Tk()
    root.wm_state(newstate="zoomed")
    FinderApp(root)     # Will enter root's event loop after initialising the UI.

    
if __name__ == '__main__':
    main()
