import math
from tkinter import Frame, Label

from PIL import Image, ImageTk


class PlayerTeam:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        white_img = Image.open("client/img/white/pawn.png")
        black_img = Image.open("client/img/black/pawn.png")
        white_img = white_img.resize((24, 24), Image.ANTIALIAS)
        black_img = black_img.resize((24, 24), Image.ANTIALIAS)
        self.white_img = ImageTk.PhotoImage(image=white_img)
        self.black_img = ImageTk.PhotoImage(image=black_img)

        self.team_lbl = Label(self.frame)
        self.team_lbl.grid(column=0, row=0)

        self.nick_lbl = Label(self.frame, text="")
        self.nick_lbl.grid(column=1, row=0)

        self.timer_lbl = Label(self.frame, text="")
        self.timer_lbl.grid(column=0, row=1, columnspan=2)

        self.time: int = 0
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0

        self.timer_id: any = None

    def reset(self):
        self.reset_all_except_nick()
        self.nick_lbl["text"] = ""

    def reset_all_except_nick(self):
        self.stop_timer()
        self.time = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.team_lbl["image"] = ""
        self.timer_lbl["text"] = ""

    def stop_timer(self):
        if self.timer_id:
            self.frame.after_cancel(self.timer_id)

    def update_time(self, time_ms: int):
        self.stop_timer()
        self.hours = time_ms // (1000 * 3600)
        left = time_ms - self.hours * 1000 * 3600
        self.minutes = left // (1000 * 60)
        left = left - self.minutes * 1000 * 60
        self.seconds = int(math.ceil(left / 1000))

    def update_timer_lbl(self):
        hours_str = f"0{self.hours}" if self.hours < 10 else str(self.hours)
        minutes_str = f"0{self.minutes}" if self.minutes < 10 else str(self.minutes)
        seconds_str = f"0{self.seconds}" if self.seconds < 10 else str(self.seconds)

        self.timer_lbl["text"] = f"{hours_str}:{minutes_str}:{seconds_str}"

    def start_counting(self):
        self.timer_id = self.frame.after(self.time % 1000, self.count_second)

    def count_second(self):
        if self.seconds == 0:
            self.seconds = 59
            if self.minutes == 0:
                self.minutes = 59
                if self.hours == 0:
                    return
                else:
                    self.hours -= 1
            else:
                self.minutes -= 1
        else:
            self.seconds -= 1

        self.update_timer_lbl()
        self.timer_id = self.frame.after(1000, self.count_second)
