from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card={}
to_learn={}

#----------------Error Prevention-------------------------------
try:
    data=pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data=pandas.read_csv("data/french_words.csv")
    to_learn=original_data.to_dict(orient="records")
else:    
    to_learn=data.to_dict(orient="records")
#------------------------------Functions------------------------

def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card=random.choice(to_learn)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_word,text=current_card["French"],fill="black")
    canvas.itemconfig(card_background,image=card_front)
    flip_timer=window.after(3000,func=flip_card)

def flip_card():
    
    current_card=random.choice(to_learn)
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card["English"],fill="white")
    canvas.itemconfig(card_background,image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data=pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()
#-------------------------------UI------------------------------

#Window
window=Tk()
window.title("Flash Card")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
flip_timer=window.after(3000,func=flip_card)

#Canvas
canvas = Canvas(width=800,height=526)
card_front=PhotoImage(file="images/card_front.png")
card_back_img=PhotoImage(file="images/card_back.png")
card_background=canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
card_title=canvas.create_text(400, 150, text="",font=("Ariel",40,"italic"))
card_word=canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))
canvas.grid(row=0,column=0,columnspan=2)

#Buttons
wrong=PhotoImage(file="images/wrong.png")
check=PhotoImage(file="images/right.png")
unknown_button=Button(image=wrong, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
check_button=Button(image=check, bg=BACKGROUND_COLOR, highlightthickness=0,command=is_known)
unknown_button.grid(row=1,column=0)
check_button.grid(row=1,column=1)


next_card()
window.mainloop()
