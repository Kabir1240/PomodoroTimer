from tkinter import *
import math
from tkinter_widgets import TkinterWidgets
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
IMAGE_PATH = "tomato.png"


class Pomodoro:
    def __init__(self, work_min, short_break_min, long_break_min):
        self.work_min = work_min
        self.short_break_min = short_break_min
        self.long_break_min = long_break_min

        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)
        self.reps = 0
        self.timer = None
        self.timer_text = ""
        self.tomato_img = PhotoImage(file=IMAGE_PATH)

        self.widgets = TkinterWidgets()
        self.create_labels()
        self.create_buttons()
        self.create_canvas()

        self.window.mainloop()

    def create_labels(self):
        timer_title = Label(text="Timer", font=(FONT_NAME, 50, 'bold'), fg=GREEN, bg=YELLOW)
        timer_title.grid(row=0, column=1)

        checkmarks = Label(text="", font=(FONT_NAME, 13, 'bold'), fg=GREEN, bg=YELLOW)
        checkmarks.grid(row=3, column=1)

        label_dict = {
            "timer": timer_title,
            "checkmarks": checkmarks,
        }
        self.widgets.add_label_dict(label_dict)

    def create_buttons(self):
        # make start button
        start_button = Button(text="Start", font=(FONT_NAME, 10, 'bold'), command=self.start_clock)
        start_button.grid(row=2, column=0)

        # make reset button
        reset_button = Button(text="Reset", font=(FONT_NAME, 10, 'bold'), command=self.reset_timer)
        reset_button.grid(row=2, column=2)

        button_dict = {
            "start_button": start_button,
            "reset_button": reset_button,
        }

        self.widgets.add_button_dict(button_dict)

    def create_canvas(self):
        # create canvas with tomato image
        canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        canvas.create_image(100, 112, image=self.tomato_img)
        # add timer to canvas
        self.timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, 'bold'))
        canvas.grid(row=1, column=1)

        self.widgets.add_canvas("canvas", canvas)

    def countdown(self, count):
        minutes = math.floor(count / 60)
        seconds = count % 60

        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"

        self.widgets.get_canvas("canvas").itemconfig(self.timer_text, text=f"{minutes}:{seconds}")

        if count > 0:
            self.timer = self.window.after(1000, self.countdown, count - 1)
        else:
            self.start_clock()

    def start_clock(self):
        self.reps += 1
        work_sec = self.work_min * 60
        short_break_sec = self.short_break_min * 60
        long_break_sec = self.long_break_min * 60

        timer_title = self.widgets.get_labels("timer")
        checkmarks = self.widgets.get_labels("checkmarks")

        if self.reps % 8 == 0:
            timer_title.config(text="Break", fg=RED)
            self.countdown(long_break_sec)
        elif self.reps % 2 == 1:
            checkmarks.config(text="✔" * int(self.reps / 2))
            timer_title.config(text="Work", fg=GREEN)
            self.countdown(work_sec)
        elif self.reps % 2 == 0:
            timer_title.config(text="Break", fg=PINK)
            self.countdown(short_break_sec)

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        timer_title = self.widgets.get_labels("timer")
        timer_title.config(text="Timer", fg=GREEN)
        self.widgets.get_canvas("canvas").itemconfig(self.timer_text, text="00:00")
        self.reps = 0