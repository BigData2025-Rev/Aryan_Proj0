import pandas as pd
import random
import re
from tkinter.messagebox import showinfo
from tkinter import *

# with open("Automobile.csv", "r") as file:
#     content = pandas(file.read())
try:
    data = pd.read_csv("Automobile.csv") 
    car_origin = data[["name" , "origin"]]

    # create question answer list

    questions = car_origin["name"].to_list()  
    answers = car_origin["origin"].to_list()

    # making dictionary of question and answer

    game_dict = dict(zip(questions, answers))
    
    # print(game_dict)
except FileNotFoundError:
    print("there is no csv file ")
    game_dict = {}

current_question = None
score = 0
question_count = 0  #counter for the number of the question ask from user
total_question = 10    #limit for question ask from user
username = input("What is your username: ")

def get_highest_score():
     # get the highest score form the text file
    try:
        with open("score.txt", "r") as file:
            scores = [line.strip().split(": ") for line in file.readlines()]
            scores = [(name, int(s)) for name, s in scores]
            highest = max(scores, key=lambda x: x[1])
            return f"{highest[0]}: {highest[1]}"
    except(FileNotFoundError, ValueError):
        return "No High score yet!"


def next_question():
    # Display next random car name
    global current_question, question_count
    if question_count< total_question and  game_dict:
        current_question = random.choice(list(game_dict.keys()))
        canvas.itemconfig(card_title, text= "Car Name", fill= "black")
        canvas.itemconfig(card_word, text=current_question , fill= "black")
        canvas.itemconfig(card_background, image= card_front_img)

        entry.delete(0, END) # clear the input
        question_count += 1
    else:
       end_game()


def is_valid_country_name(country_name):
    pattern = r"[A-Za-z\s]+$"
    return bool(re.match(pattern, country_name))

def check_answer():
    #check if the user guess the right answer
    global score
    user_guess = entry.get().strip().lower()

    if not is_valid_country_name(user_guess):
        showinfo("invalid input", "Please enter a valid country name only alphabet")
        return

    correct_answer = game_dict[current_question].lower()

    if user_guess == correct_answer:
        score += 1
        score_label.config(text=f"Score: {score}")
        
        del game_dict[current_question]
    next_question()

def end_game():
     # End of the game, show the final score and save it in file
     canvas.itemconfig(card_title, text= "Game Over", fill= "black")
     canvas.itemconfig(card_word, text= f"Final Score: {score}", fill="black")
     canvas.itemconfig(card_background, image=card_front_img)
     save_score()
     highest_score_label.config(text= f"Highest Score: {get_highest_score()}")

def save_score():
    #save the user score to text file
    with open("score.txt", "a") as file:
              file.write(f"{username}: {score}\n")

window = Tk()
window.title("Car Knowledge Game")
window.config(padx=50, pady= 50, bg="#B1DDC6")

canvas = Canvas(width = 1000, height= 600)
card_front_img = PhotoImage(file= "images/card_front.png")
card_back_img = PhotoImage(file= "images/card_back.png")

card_background =canvas.create_image(500, 300, image= card_front_img)
canvas.config(bg="#B1DDC6", highlightthickness=0)
canvas.grid(row=0, column=0, columnspan= 2)

card_title = canvas.create_text(500, 200, text= "", font=("Arial", 40, "italic"))
card_word = canvas.create_text(500, 300, text="", font=("Arial", 60, "bold"), width=900)

#entry box for user
entry = Entry(width=40, font=("Arial, 20"))
entry.grid(row=1, column=0, columnspan=2, pady=20)



# Buttons for interactions
# cross_img = PhotoImage(file="images/wrong.png")
submit_buttion = Button(text="Submit", command=check_answer, highlightthickness=0)
submit_buttion.grid(row=2, column=0)

# check_img = PhotoImage(file= "images/right.png")
skip_button = Button(text = "Skip", command=next_question, highlightthickness=0)
skip_button.grid(row=2, column=1)

#score label
score_label = Label(text="Score: 0", font=("Arial", 16), bg="#B1DDC6")
score_label.grid(row=3, column=0, columnspan=2)

highest_score_label = Label(text = f"Highest Score: {get_highest_score()}" , bg="#B1DDC6" , font=("Arial", 16))
highest_score_label.grid(row=4, column=0, columnspan=2)
next_question()
window.mainloop()