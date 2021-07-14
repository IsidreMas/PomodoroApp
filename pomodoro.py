# POMODORO ISIDRE MAS 1.0

from tkinter import *
from playsound import playsound
from threading import Thread
import math
# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
ticks = ""
pomodoro_count = 0
timer = None
reset_flag = False
muted = False
egg_offset = 0

def focus_window():
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)


def wind_up_sound():
    if not muted:
        playsound("./resources/WindUp.mp3")


def break_sound():
    if not muted:
        playsound("./resources/Break.mp3")

def mute():
    global muted
    muted = not muted
    if muted:
        mute_button.config(text="Unmute", bg=GREEN, fg=YELLOW)
    else:
        mute_button.config(text="Mute", bg=YELLOW, fg=PINK)

def wind_up_pomodoro(MINUTES):
    clicks = 24
    if MINUTES > 5:
        wind_up = Thread(target=wind_up_sound)
        wind_up.start()

    if reps > 1:
        break_bell = Thread(target=break_sound)
        break_bell.start()

    def move_dial(clicks_remaining):
        global egg_offset
        if clicks_remaining > 0:
            egg_canvas.move(egg_top, (183 / 25) * MINUTES / 24, 0)
            egg_offset += MINUTES / 24
            window.after(42, move_dial, clicks_remaining - 1)

    move_dial(clicks)


# ---------------------------- TIMER RESET ------------------------------- #
def start_reset_button():
    global reset_flag
    global egg_offset

    if reset_flag:
        egg_canvas.move(egg_top, -(183 / 25) * egg_offset, 0)
        break_bell = Thread(target=break_sound)
        break_bell.start()
        egg_offset -= egg_offset
        reset_flag = False
        start_button.config(text="Start", bg=PINK)
        reset_timer()
    else:
        egg_canvas.move(egg_top, -(183 / 25) * egg_offset, 0)
        egg_offset -= egg_offset
        reset_flag = True
        start_button.config(text="Reset", bg=GREEN)
        start_timer()

def reset_timer():
    global reps
    global ticks
    global pomodoro_count
    global egg_offset

    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    reps = 1
    ticks = ""
    pomodoro_count = 0
    ticks_label.config(text=ticks)
    pomodoro_canvas.itemconfig(pomodoros, image=pomodoro_list[pomodoro_count])
    timer_status.config(text="Timer", fg=GREEN)
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        timer_status.config(text="Break", fg=RED)
        focus_window()
        wind_up_pomodoro(LONG_BREAK_MIN)
        if pomodoro_count > 6:
            start_reset_button()
            timer_status.config(text="Go sleep!", fg=RED)
        else:
            countdown(long_break_sec)

    elif reps % 2 == 0:
        timer_status.config(text="Break", fg=PINK)
        focus_window()
        wind_up_pomodoro(SHORT_BREAK_MIN)
        countdown(short_break_sec)
    else:
        timer_status.config(text="Work", fg=GREEN)
        focus_window()
        wind_up_pomodoro(WORK_MIN)
        countdown(work_sec)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global reps
    global ticks
    global pomodoro_count
    global timer
    global egg_offset

    min_count = round(math.floor(count/60))
    sec_count = round(count % 60)
    if sec_count < 10:
        sec_count = f"0{sec_count}"
    canvas.itemconfig(timer_text, text=f"{min_count}:{sec_count}")
    egg_canvas.move(egg_top, -(183 / 25)/60, 0)
    egg_offset -= 1/60

    if count >= 0:
        timer = window.after(1000, countdown, count - 1)
    else:

        reps += 1
        if reps % 8 == 0:
            ticks = ""
            pomodoro_count += 1
            pomodoro_canvas.itemconfig(pomodoros, image=pomodoro_list[pomodoro_count])
        elif reps % 2 == 0:
            ticks += "✔"
        ticks_label.config(text=ticks)
        start_timer()
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(pady=10, bg=YELLOW)
window.iconphoto(False, PhotoImage(file='./resources/tomato.png'))
window.resizable(0, 0)
# Tomato
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="./resources/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill=YELLOW, font=(FONT_NAME, 40, "bold"))
canvas.grid(column=1, row=1)

# Egg clock

egg_canvas = Canvas(width=400, height=100, bg=YELLOW, highlightthickness=0)
egg_top_image = PhotoImage(file="./resources/Top_marks.png")
egg_bottom_image = PhotoImage(file="./resources/Bottom_marks.png")
egg_top = egg_canvas.create_image(200, 25, image=egg_top_image)
egg_bottom = egg_canvas.create_image(200, 73, image=egg_bottom_image)
egg_canvas.grid(column=1, row=2, pady=5)

# Timer status label
timer_status = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
timer_status.grid(column=1, row=0)

#Start button

start_button = Button(text="Start", highlightthickness=0, command=start_reset_button,
                      activebackground=RED, bg=PINK, fg=YELLOW, font=(FONT_NAME, 20, "bold"), relief="flat")
start_button.grid(column=1, row=5)

#Tick label

ticks_label = Label(text=f"{ticks}", fg=GREEN, font=(FONT_NAME, 20, "bold"), bg=YELLOW, padx=10, pady=10)
ticks_label.grid(column=1, row=3)

#Pomodoro canvas

pomodoro_canvas = Canvas(width=400, height=100, bg=YELLOW, highlightthickness=0)
pomodoro_list = []
for i in range(8):
    pomodoro_list.append(PhotoImage(file=f"./resources/pomodoro_{i}.png"))

pomodoros = pomodoro_canvas.create_image(200, 25, image=pomodoro_list[pomodoro_count])
pomodoro_canvas.grid(column=1, row=4, pady=5)
#Mute button

mute_button = Button(text="Mute", highlightthickness=0, command=mute,
                     activebackground=YELLOW, bg=YELLOW, fg=PINK, font=(FONT_NAME, 10, "bold"), relief="flat",
                     activeforeground=RED, borderwidth=0)
mute_button.grid(column=1, row=6, pady=10)
mute_button.bind("<Enter>", lambda e: mute_button.config(fg=RED) if muted else mute_button.config(fg=RED))
mute_button.bind("<Leave>", lambda e: mute_button.config(fg=YELLOW) if muted else mute_button.config(fg=PINK))



window.mainloop()
