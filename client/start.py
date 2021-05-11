from tkinter import *
from PIL import ImageTk
import platform

if platform.system() == "Darwin":
    from tkmacosx import Button


class Start:
    def __init__(self, root):
        self.root = root
        self.root.title("Start")
        self.root.geometry("1200x600")

        self.bg_img = ImageTk.PhotoImage(file="img/bg2.jpg")
        self.bg = Label(self.root, image=self.bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=150, y=150, width=500, height=340)

        self.title = Label(self.frame, text="Start", font=("Impact", 35, "bold"), fg="#d77337", bg="white")
        self.title.place(x=90, y=30)

        # TODO add welcome message

        if platform.system() == "Darwin":
            self.join_ranked_btn = Button(self.root, text="Join ranked", font=("Times New Roman", 16, "bold"),
                                          fg="white", bg="#d77337", activeforeground="white",
                                          activebackground="#c56328", borderless=1, cursor="hand2",
                                          command=self.join_ranked)

            self.create_private_room_btn = Button(self.root, text="Create private room",
                                                  font=("Times New Roman", 16, "bold"), fg="white", bg="#d77337",
                                                  activeforeground="white", activebackground="#c56328", borderless=1,
                                                  cursor="hand2", command=self.create_private_room)
        else:
            self.join_ranked_btn = Button(self.root, text="Join ranked", font=("Times New Roman", 16, "bold"),
                                          fg="white", bg="#d77337", activeforeground="white",
                                          activebackground="#c56328", cursor="hand2", command=self.join_ranked)

            self.create_private_room_btn = Button(self.root, text="Create private room",
                                                  font=("Times New Roman", 16, "bold"), fg="white", bg="#d77337",
                                                  activeforeground="white", activebackground="#c56328", cursor="hand2",
                                                  command=self.create_private_room)

        self.join_ranked_btn.place(x=205, y=470, width=180, height=40)

        self.create_private_room_btn.place(x=405, y=470, width=180, height=40)

    def join_ranked(self):
        pass

    def create_private_room(self):
        pass
