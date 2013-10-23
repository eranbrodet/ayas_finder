"""
    Based on code from: http://svn.python.org/projects/python/branches/pep-0384/Demo/tkinter/ttk/roundframe.py
"""
import Tkinter
import ttk


def _create_images():
    img1 = Tkinter.PhotoImage("frameFocusBorder", file="f2.gif")
    img2 = Tkinter.PhotoImage("frameBorder",  file="f1.gif")
    return img1, img2


def _config_style():
    style = ttk.Style()

    style.element_create("RoundedFrame", "image", "frameBorder",
        ("focus", "frameFocusBorder"), border=16, sticky="nsew")

    style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])


def config_round_corners():
    images = _create_images()
    _config_style()
    return images

def main():
    root = Tkinter.Tk()
    images = config_round_corners()

    frame = ttk.Frame(style="RoundedFrame", padding=10)
    frame.pack(fill='x')

    frame2 = ttk.Frame(style="RoundedFrame", padding=10)
    frame2.pack(fill='both', expand=1)

    entry = ttk.Entry(frame, text='Test')
    entry.pack(fill='x')
    entry.bind("<FocusIn>", lambda evt: frame.state(["focus"]))
    entry.bind("<FocusOut>", lambda evt: frame.state(["!focus"]))

    text = Tkinter.Text(frame2, borderwidth=0, bg="white", highlightthickness=0)
    text.pack(fill='both', expand=1)
    text.bind("<FocusIn>", lambda evt: frame2.state(["focus"]))
    text.bind("<FocusOut>", lambda evt: frame2.state(["!focus"]))

    root.mainloop()
