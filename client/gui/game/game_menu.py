from tkinter import Frame, Tk

from client.gui.shared import DisplayBoundary


def game_menu(root: Tk, display: DisplayBoundary) -> Frame:
    menu = Frame(root, bg="#ffffff")
    menu.place(x=display.x + round(10 / 16 * display.width), y=display.y + round(0.5 / 9 * display.height),
               width=round(5 / 16 * display.width), height=8 / 9 * display.height)
    return menu
