from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None # have to bring it out to make it a global variable, it's actually not going to have any value at all initially.

# ---------------------------- TIMER RESET ------------------------------- # 
# reset all the checkmarks, reset the text inside the timer,
# stop the timer and change this title back to the text that it originally had, which is just the word timer.

def reset_timer():
    window.after_cancel(timer) # we can actually cancel the timer that we had set up previously.
    canvas.itemconfig(timer_text, text="00:00") # timer text 00:00
    title_label.config(text="Timer") # title label: Timer
    check_marks.config(text="") # reset checkmark
    global reps # reps is the number of sessions we've had
    reps = 0 # reset reps


# ---------------------------- TIMER MECHANISM ------------------------------- # 
# unit: millisecond
# 25 min work -> 5 min break -> 25 min work -> 5 min break -> 25 min work -> 5 min break -> 25 min work -> 20 min break

def start_timer():
    global reps # global variable, reps is the number of sessions we've had
    reps = reps + 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0: #if 8th rep
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0: # if 2/4/6th rep
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else: # if 1/3/5/7th rep
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# window.after(millisecond, function_name, input)
# we want it to repeat itself (loop). One way of getting that behavior is to simply put this method, call somewhere inside a function and then call itself.
# And we say that after 1000 milliseconds, call this function count_down and then pass in a count number.
# we want this format: "01:35", not 95

def count_down(count):

    count_min = math.floor(count / 60) # convert from sec to min, and we just want to get rid of everything after the decimal place.
    count_sec = count % 60 # modulo is going to give us the remainder number of seconds after we've cleanly divided it by 600.

    # in order to avoid 5:0, we would like to get 5:00, need to use dynamic typing: change a variable's data(int) type by changing the content(string) in that variable
    # when there is no remainder, it's just going to be equal to zero.
    # So we could use an if statement and check if the count_sec is equal to zero, then instead of making it zero, let's set it to equal a string, which is "00".
    #if count_sec == 0:
    #    count_sec = "00"


    if count_sec < 10: # we would like 09 or 08 or 07 and also 00, not 9,8
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1) # this is a local variable because it's created inside this particular function,

    else:
        start_timer() # count down to the number of seconds that we told it to, once it's done, that's the end. There's no other way of triggering start timer unless we press the button.
        # So what we actually need to do is to add a else statement here and catch when the count goes to zero.

        # want that label to start out as empty. the only time when I want that label to get an extra check mark is when the user has completed a work countdown.
        # So once they've completed their 25 minute session, then they should get that checkmark.
        # every two reps we've completed, we add a checkmark to this checkmark label.
        # for example, if we've done for reps, then that means we've had two work sessions and two breaks.
        # That means we can basically divide reps by two to get the total number of work sessions we've done.
        marks = ""
        work_sessions = math.floor(reps/2) # use floor on reps/2 = floating -> whole number
        for _ in range(work_sessions):
            marks = marks + "✔" # for every work session we complete, we get an extra checkmark
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)






window.mainloop() # this GUI is event driven program, need to keep refreshing


# For example, languages like C or Java or Swift, you won't be able to do this.
# Once you create a variable and you give it a certain type of data, then it must forever hold on to that type of data.
# But Python allows you to change the data type of a variable just by assigning it to a different type of value.









