from sample import test_sample
from tkinter import *
from PIL import ImageTk, Image
import random
import math

BACKGROUND_COLOR = 'white'
SAMPLE_TXT_COLOR = "#41584b"
RED = '#ff9b93'
YELLOW = '#fff3b2'
LIGHT_PINK = '#ffe0d8'
timer, text, clear_box, start_type = None, None, None, None


def on_click(event):
    typing_box.delete('1.0', END)
    # make the callback only work once
    typing_box.unbind('<Button-1>', clear_box)


# -----------------------reset test ------------------------- #
def reset_test():
    global text, clear_box, start_type
    text = random.choice(test_sample)
    canvas.itemconfig(sample_text, text=text)
    reset_timer()
    typing_box.configure(state="normal")
    typing_box.delete('1.0', END)
    typing_box.insert(END, "Test begins when you start typing...")
    clear_box = typing_box.bind('<Button-1>', on_click)
    start_type = typing_box.bind('<Key>', start_timer)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer(event):
    """either user starts typing or user click restart button"""
    count_down(10)
    typing_box.unbind('<Key>', start_type)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    timer_label.config(text="01:00")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_label.config(text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        typing_box.configure(state="disabled")
        check_score()


# --------------------------Check Score ------------------------------- #
def check_score():
    sample_text_list = text.split()
    user_input = typing_box.get("1.0", END)
    user_input_list = user_input.split()
    score = 0
    for n in range(0, len(user_input_list)):
        if user_input_list[n] == sample_text_list[n]:
            score += 1
    timer_label.config(text=f"{score} correct words in 60 seconds")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Test")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# -------------------- canvas for text sample ---------------------- #
canvas = Canvas(width=600, height=340, bg=BACKGROUND_COLOR, highlightthickness=0)
background_img = Image.open("./img/background.jpg")
background_img.thumbnail((600, 340), resample=3, reducing_gap=2.0)
show_img = ImageTk.PhotoImage(background_img)
canvas.create_image(300, 170, image=show_img)
text = random.choice(test_sample)
sample_text = canvas.create_text(300, 170, text=text, width=480, fill=SAMPLE_TXT_COLOR, font=("Ariel", 14, "normal"))
canvas.grid(column=0, row=0)

# --------------------  label for Timer ---------------------- #
timer_label = Label(text="01:00", fg=RED, font=("Ariel", 20, "bold"), background=BACKGROUND_COLOR, pady=10)
timer_label.grid(row=1, column=0)

# --------------------  text box for tying ---------------------- #
typing_box = Text(font=("Ariel", 12, "normal"), bg=YELLOW, highlightthickness=0, padx=20, pady=20, width=54, height=10,
                  fg=SAMPLE_TXT_COLOR)
# initiate the typing box
typing_box.configure(state="normal")
typing_box.insert(END, "Test begins when you start typing...")
clear_box = typing_box.bind('<Button-1>', on_click)
start_type = typing_box.bind('<Key>', start_timer)
typing_box.grid(row=2, column=0)

# ---------------button for retake the tes ------------- #
try_again = Button(text="Try again", bg=LIGHT_PINK, font=("Ariel", 15, "bold"), pady=5, highlightthickness=0, command=
                                                          reset_test, relief="sunken")
try_again.grid(row=3, column=0)

window.mainloop()
