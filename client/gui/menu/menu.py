from tkinter import Frame, Label

from client.gui.shared import DisplayBoundary


def menu_frame(master, display_size: DisplayBoundary) -> Frame:
    frame = Frame(master, bg="white", padx=0.05*display_size.width, pady=0.05*display_size.width)
    frame.place(
        x=display_size.x + 0.15*display_size.width,
        y=display_size.y + 0.2*display_size.height,
        width=0.3*display_size.width,
        height=0.6*display_size.height
    )
    frame.update()
    return frame


def menu_title(menu, text: str) -> Label:
    title = Label(menu, text=text, font=("Impact", 25, "bold"), fg="#d77337", bg="white")
    title.grid(row=0, column=0, sticky="WN")
    return title
