from Tkinter import Tk                                  # GUI components
from Tkinter import Text                                # Tkinter elements
from Tkinter import N, S                                # Directions
from Tkinter import END, INSERT                         # Index positions
from ttk import Style, Frame, Button, Scrollbar, Label  # ttk elements
import re


class FinderApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self._init_ui()
        self._pos()

    def _pos(self):
        """
            Sizes window to 80% of the screen size and centres it.
        """
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        w = sw * 0.8
        h = sh * 0.8
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def _init_ui(self):
        Style().configure("TLabel", padding=(15, 5, 0, 5), font='Times 15')
        Style().configure("TFrame", padding=(0, 5, 0, 5), font='Times 15')
        Style().configure("TButton", padding=(0, 5, 0, 5), font='Times 15')
        self.parent.title("Aya's Finder")

        # Define input fields
        to_find_list = Text(self, font="Times 15", height=3)
        to_find_list_scrollbar = Scrollbar(self, command=to_find_list.yview)
        to_find_list.configure(yscrollcommand=to_find_list_scrollbar.set)
        glossary = Text(self, font="Times 15", height=3)
        glossary_scrollbar = Scrollbar(self, command=glossary.yview)
        glossary.configure(yscrollcommand=glossary_scrollbar.set)

        # Define output
        results = Text(self, font="Times 15", height=9)
        results_scrollbar = Scrollbar(self, command=results.yview)
        results.configure(yscrollcommand=results_scrollbar.set)

        # Define not found
        not_found = Text(self, font="Times 15", height=9)
        not_found_scrollbar = Scrollbar(self, command=not_found.yview)
        not_found.configure(yscrollcommand=not_found_scrollbar.set)
        
        # Define button callback
        def _find():
            results.delete(1.0, END)
            not_found.delete(1.0, END)
            l1 = re.split('[, ]+', to_find_list.get(1.0, END).strip())
            l2 = re.split('[, ]+', glossary.get(1.0, END).strip())
            l1 = [x.upper() for x in l1]
            l2 = [x.upper() for x in l2]
            dict2 = {x[1]: x[0] for x in enumerate(l2)}
            for item in l1:
                if item == '':
                    continue
                elif item in l2:
                    results.insert(INSERT, "gene: %s --- index in glossary: %s\n" % (item, dict2[item]))
                else:
                    not_found.insert(INSERT, "gene: %s --- not found\n" % (item,))
            

        # Define button
        find_button = Button(self, text="Find", width=10, command=_find)

        # Define tab behaviour
        def _tab_handler(event):
            switch = {to_find_list: glossary.focus, glossary: find_button.focus,
                      find_button: results.focus, results: to_find_list.focus}
            switch[event.widget]()
            return 'break'  # Won't display the character
        # Bind tabs
        to_find_list.bind("<Tab>", _tab_handler)
        glossary.bind("<Tab>", _tab_handler)
        find_button.bind("<Tab>", _tab_handler)
        results.bind("<Tab>", _tab_handler)

        # Define text labels
        to_find_label = Label(self, width=18, text="List of genes to find: ")
        glossary_label = Label(self, width=18, text="Glossary list: ")
        results_label = Label(self, width=18, text="Results: ")
        not_found_label = Label(self, width=18, text="Not found: ")

        # Display all elements using the grid layout manager
        to_find_label.grid(row=0, column=0)
        to_find_list_scrollbar.grid(row=0, column=15, sticky=S+N)
        to_find_list.grid(row=0, column=2)
        glossary_label.grid(row=3, column=0)
        glossary_scrollbar.grid(row=3, column=15, sticky=S+N)
        glossary.grid(row=3, column=2)
        find_button.grid(row=6, column=2)
        results_label.grid(row=9, column=0)
        results_scrollbar.grid(row=9, column=15, sticky=S+N)
        results.grid(row=9, column=2)
        not_found_label.grid(row=10, column=0)
        not_found_scrollbar.grid(row=10, column=15, sticky=S+N)
        not_found.grid(row=10, column=2)
        self.grid()


def main():
    root = Tk()
    FinderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
