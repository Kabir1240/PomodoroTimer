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
    def __init__(self, work_min=25, short_break_min=5, long_break_min=20):
        """
        Create windows, Tk widgets and initialize main loop
        :param work_min: amount of time allocated to work, in minutes
        :param short_break_min: amount of time allocated to breaks, in minutes
        :param long_break_min: amount of time allocated to long break, in minutes. Occurs after every 4 pomodoros
        """

        # initialize timer values
        self.work_min = work_min
        self.short_break_min = short_break_min
        self.long_break_min = long_break_min

        # create Tk window
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        # initialize required variables
        self.reps = 0
        self.timer = None
        self.timer_text = ""
        self.tomato_img = PhotoImage(file=IMAGE_PATH)

        # create required widgets and store them
        self.widgets = TkinterWidgets()
        self.create_labels()
        self.create_buttons()
        self.create_canvas()

        # main loop
        self.window.mainloop()

    def create_labels(self) -> None:
        """
        creates required Label objects, organizes them in grid format, saves them in widgets
        :return: None
        """

        timer_title = Label(text="Timer", font=(FONT_NAME, 50, 'bold'), fg=GREEN, bg=YELLOW)
        timer_title.grid(row=0, column=1)

        checkmarks = Label(text="", font=(FONT_NAME, 13, 'bold'), fg=GREEN, bg=YELLOW)
        checkmarks.grid(row=3, column=1)

        label_dict = {
            "timer": timer_title,
            "checkmarks": checkmarks,
        }
        self.widgets.add_label_dict(label_dict)

    def create_buttons(self) -> None:
        """
        creates required Button objects, organizes them in grid format, saves them in widgets
        :return: None
        """

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

    def create_canvas(self) -> None:
        """
        creates required Canvas objects, organizes them in grid format, saves them in widgets
        :return: None
        """

        # create canvas with tomato image
        canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        canvas.create_image(100, 112, image=self.tomato_img)
        # add timer to canvas
        self.timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, 'bold'))
        canvas.grid(row=1, column=1)

        self.widgets.add_canvas("canvas", canvas)

    def countdown(self, count) -> None:
        """
        countdown from given time (count) in seconds. Displays time in MM:SS format
        :param count: time, in seconds
        :return: None
        """

        # convert seconds to minutes and seconds
        minutes = math.floor(count / 60)
        seconds = count % 60

        # fix display
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"

        # display timer
        self.widgets.get_canvas("canvas").itemconfig(self.timer_text, text=f"{minutes}:{seconds}")

        # start next rep if time reaches 0. Otherwise, carry out recursion
        if count > 0:
            self.timer = self.window.after(1000, self.countdown, count - 1)
        else:
            self.start_clock()

    def start_clock(self) -> None:
        """
        Starts countdown
        :return: None
        """

        self.reps += 1

        # convert timers into seconds
        work_sec = self.work_min * 60
        short_break_sec = self.short_break_min * 60
        long_break_sec = self.long_break_min * 60

        # get appropriate widgets
        timer_title = self.widgets.get_labels("timer")
        checkmarks = self.widgets.get_labels("checkmarks")

        # long break every 8 reps (4 complete pomodoros), alternate between work and break, starting with work
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

    def reset_timer(self) -> None:
        """
        resets timer
        :return: None
        """

        # cancel after loop
        self.window.after_cancel(self.timer)

        # reset timer, reps and title to normal
        timer_title = self.widgets.get_labels("timer")
        timer_title.config(text="Timer", fg=GREEN)
        self.widgets.get_canvas("canvas").itemconfig(self.timer_text, text="00:00")
        self.reps = 0
