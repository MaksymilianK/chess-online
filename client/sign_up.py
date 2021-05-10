from tkinter import *
from PIL import ImageTk
import platform

if platform.system() == "Darwin":
    from tkmacosx import Button


class SignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("1200x600")

        self.bg_img = ImageTk.PhotoImage(file="img/bg1.jpg")
        self.bg = Label(self.root, image=self.bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=150, y=150, width=500, height=340)

        self.title = Label(self.frame, text="Sign Up", font=("Impact", 35, "bold"), fg="#d77337", bg="white")
        self.title.place(x=90, y=30)

        self.nick_lbl = Label(self.frame, text="Nick", font=("Times New Roman", 15, "bold"), fg="gray", bg="white")
        self.nick_lbl.place(x=90, y=100)

        self.nick_entry = Entry(self.frame, font=("Times New Roman", 15), bg="lightgray")
        self.nick_entry.place(x=90, y=130, width=350, height=35)

        self.email_lbl = Label(self.frame, text="Email", font=("Times New Roman", 15, "bold"), fg="gray", bg="white")
        self.email_lbl.place(x=90, y=170)

        self.email_entry = Entry(self.frame, font=("Times New Roman", 15), bg="lightgray")
        self.email_entry.place(x=90, y=200, width=350, height=35)

        self.password_lbl = Label(self.frame, text="Password", font=("Times New Roman", 15, "bold"), fg="gray",
                                  bg="white")
        self.password_lbl.place(x=90, y=240)

        self.password_entry = Entry(self.frame, font=("Times New Roman", 15), bg="lightgray")
        self.password_entry.place(x=90, y=270, width=350, height=35)

        if platform.system() == "Darwin":
            self.sign_up_btn = Button(self.root, text="Sign Up", font=("Times New Roman", 20), fg="white", bg="#d77337",
                                      activeforeground="white", activebackground="#c56328", borderless=1,
                                      cursor="hand2", command=self.sign_up)
        else:
            self.sign_up_btn = Button(self.root, text="Sign Up", font=("Times New Roman", 20), fg="white", bg="#d77337",
                                      activeforeground="white", activebackground="#c56328", cursor="hand2",
                                      command=self.sign_up)
        self.sign_up_btn.place(x=300, y=470, width=180, height=40)

    def sign_up(self):
        pass
