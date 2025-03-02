import tkinter as tk
import random
from animation import AnimatedGIF

# List of words categorized by difficulty
countries = {
    'easy': ['China', 'Japan', 'India', 'Chile', 'Greece','Egypt', 'Italy', 'Peru', 'Mexico', 'Jordan', 'Kenya', 'Wales', 'Cuba', 'Fiji', 'Ireland', 'Iceland', 'Malta', 'Mali', 'Russia', 'Laos', 'Iran', 'Iraq'],
    'medium': ['Brazil', 'France', 'Turkey', 'Norway', 'Spain','Canada', 'Ghana', 'Poland', 'Cyprus', 'Brazil', 'Denmark', 'Madagascar', 'Morocco', 'Belgium', 'Finland', 'Portugal', 'Croatia', 'Georgia', 'Bolivia', 'Monaco', 'Serbia', 'Slovenia'],
    'hard': ['Australia', 'Thailand', 'Argentina', 'Hungary', 'Malaysia','Slovakia', 'Nepal', 'Estonia', 'Switzerland', 'Liechtenstein', 'Cambodia', 'Andorra', 'Luxembourg', 'Zimbabwe','Mozambique', 'Ethiopia', 'Tanzania', 'Indonesia', 'Belarus', 'Gibraltar', 'Uruguay', 'Vietnam'],
    'expert': ['Uzbekistan', 'Kyrgyzstan', 'Azerbaijan', 'Tajikistan', 'Turkmenistan', 'Djibouti', 'Eritrea', 'Suriname', 'Vanuatu', 'Bhutan', 'Netherlands', 'Philippines', 'Mauritius', 'Solomon Islands', 'Costa Rica', 'Papua New Guinea', 'New Zealand', 'Kazakhstan', 'Myanmar', 'Somalia', 'Vatican City', 'Bangladesh']
}

# Number of rounds
TOTAL_ROUNDS = 10
timer_id = None
time_limit = 20  # Time limit for timed mode
high_score = 0  # Variable to track the high score
hint_count = 0
used_words = []

# Initialize round variables
current_round = 0
selected_difficulty = ''
game_mode = ''

def scramble_word(word):
    # Split the country name into individual words
    words = word.split()  
    # Scramble each word individually and join them back with spaces
    scrambled_words = [''.join(random.sample(w.lower(), len(w))) for w in words]
    return ' '.join(scrambled_words)


def get_random_word(difficulty):
    global used_words
    word = random.choice(countries[difficulty])
    while word in used_words:
        word = random.choice(countries[difficulty])
    used_words.append(word)
    return scramble_word(word), word

def start_game():
    global current_round ,score, game_mode, used_words
    used_words = []
    current_round = 1  # Start at the first round
    score = 0  # Reset score to 0 at the start of the game
    game_mode = mode_var.get() # Set the game mode (time or untimed)
    score_label.config(text=f"Score: {score}")  # Update score label to show 0 at the start
    next_round()
    result_label.config(text="") # Reset the result label for a new round
    play_again_button.pack_forget()
    bind_enter_key()  # Bind the Enter key when the game starts

    # Hide the mode selection label and radio buttons
    mode_label.place_forget()
    untimed_button.place_forget()
    timed_button.place_forget()
    high_score_label.place_forget()

    # Show the widgets once the game starts
    scrambled_label.pack()
    guess_entry.pack(pady=5)
    check_button.pack()
    score_label.pack()
    animated_gif.pack_forget()

    hint_label.place(x=370, y=110)
    hint_button.place(x=400, y=55)

def display_scrambled_word_with_blanks(scrambled_word):
    letters = ' '.join(scrambled_word.lower())  # Display letters in lowercase for better visibility
    blanks = ' '.join(['_' for _ in scrambled_word])  # Underlines under each letter
    return letters, blanks

def next_round():
    global current_round, original_word, scrambled_word, selected_difficulty, hint_count

    if current_round <= TOTAL_ROUNDS:
        hint_count = 0
        hint_button.config(state="normal")  # Enable the hint button for the new round
        hint_label.config(text="")  # Clear the previous hint

        # Reset the result label for a new round
        result_label.config(text="")
        timer_message_label.config(text="")  # Clear any previous timer messages

        # Randomly select a difficulty level
        selected_difficulty = random.choice(list(countries.keys()))

        # Get a scrambled word based on the selected difficulty
        scrambled_word, original_word = get_random_word(selected_difficulty)

        # Generate the display format for letters and blanks
        letters, blanks = display_scrambled_word_with_blanks(scrambled_word)

        # Update the label with letters and blanks
        scrambled_label.config(text=f"{letters}\n")  # Display letters above blanks
        difficulty_label.config(text=f"Difficulty: {selected_difficulty.capitalize()}")
        round_label.config(text=f"Round {current_round} of {TOTAL_ROUNDS}")
        guess_entry.delete(0, tk.END)

        # Start timer if timed mode is selected
        if game_mode == "timed":
            start_timer()

    else:

        # Stop and hide the timer when the game ends
        if timer_id is not None:
            root.after_cancel(timer_id)  # Stop the timer
        timer_label.config(text="")  # Clear the timer label

        # Game over when all rounds are completed
        result_label.config(text="Game Over!", fg="darkblue", bg='lightblue')
        round_label.config(text="")
        scrambled_label.config(text="")
        difficulty_label.config(text="")
        timer_message_label.config(text="")
        mode_label.place(x=10, y=50)
        untimed_button.place(x=30, y=80)
        timed_button.place(x=30, y=110)
        high_score_label.place(x=350, y=10)
        guess_entry.delete(0, tk.END)
        animated_gif.pack()
        score_label.pack()
        check_high_score()  # Check for high score when the game ends

        # Hide the widgets when the game ends
        scrambled_label.pack_forget()
        guess_entry.pack_forget()
        check_button.pack_forget()
        start_button.pack_forget()
        play_again_button.pack()
        hint_button.place_forget()
        hint_label.place_forget()


def check_guess():
    global current_round
    guess = guess_entry.get().strip().lower()
    if guess == original_word.lower():
        result_label.config(text="Correct!", fg="green", bg='lightgreen')
        update_score(True)
    else:
        result_label.config(text=f"Wrong! The correct word was '{original_word}'", fg="red", bg='lightcoral')
        update_score(False)

    current_round += 1
    root.after(2000, next_round)  # 2000 milliseconds = 2 seconds

def check_high_score():
    global high_score, score
    if score > high_score:
        high_score = score
        high_score_label.config(text=f"High Score: {high_score}")


def update_score(correct=None):
    global score , selected_difficulty
    difficulty = selected_difficulty  # Get the selected difficulty level
    
    # Assign points based on the difficulty level
    if difficulty == 'easy':
        correct_points = 5
        wrong_points = -2
    elif difficulty == 'medium':
        correct_points = 10
        wrong_points = -5
    elif difficulty == 'hard':
        correct_points = 15
        wrong_points = -7
    elif difficulty == 'expert':
        correct_points = 20
        wrong_points = -10

    # Update score based on correctness
    if correct is True:
        score += correct_points
    elif correct is False:
        score += wrong_points
    
    score_label.config(text=f"Score: {score}")


def start_timer():
    global timer_id, time_left, current_round

    # Reset the time left to the time limit for each round
    time_left = time_limit

    # Cancel any previous timer if it's running
    if timer_id is not None:
        root.after_cancel(timer_id)

    def countdown():
        global timer_id, time_left, current_round, score

        # Stop the timer if all rounds are completed
        if current_round > TOTAL_ROUNDS:
            return  # Do nothing and exit countdown if game is over

        # If time is up, end the round
        if time_left <= 0:
            score -= 2
            timer_message_label.config(text="Time's up! Moving to the next round.", fg="orange", bg='lightblue')
            result_label.config(text=f"Wrong! The correct word was '{original_word}'", fg="red", bg='lightcoral')
            score_label.config(text=f"Score: {score}")
            current_round += 1
            root.after(1000, next_round)
        else:
            # Update timer label with the remaining time
            timer_label.config(text=f"Time left: {time_left}s")
            time_left -= 1
            # Schedule the countdown function to run after 1 second (1000 ms)
            timer_id = root.after(1000, countdown)

    # Start the countdown
    countdown()

# Bind the Enter key to the check_guess function
def bind_enter_key():
    root.bind('<Return>', lambda event: check_guess())

def use_hint():
    global original_word, hint_used, score, hint_count
    
    if hint_count < 3:  # Check if fewer than 3 hints have been used
        if hint_count == 0:  # First press, reveal the first letter
            first_letter = original_word[0].capitalize()
            hint_label.config(text=f"First letter: {first_letter}")
        elif hint_count == 1:  # Second press, reveal the second letter
            second_letter = original_word[1].lower()
            hint_label.config(text=f"First letter: {original_word[0].capitalize()}\nSecond letter: {second_letter}")
        elif hint_count == 2:
            third_letter = original_word[2].lower() 
            hint_label.config(text=f"First letter: {original_word[0].capitalize()}\nSecond letter: {original_word[1].lower()}\nThird letter: {third_letter}")


        score -= 2  # Deduct 2 points each time a hint is used
        score_label.config(text=f"Score: {score}")
        hint_count += 1  # Increment the hint counter
        
        if hint_count == 3:  # Disable the hint button after 2 presses
            hint_button.config(state="disabled")



def exit_game():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Country Scramble Game")
root.geometry("500x500")
root.config(bg='lightblue')  # Set background color of the main window

# Initialize game state
original_word = ''
score = 0

# Create frames for better layout
top_frame = tk.Frame(root, bg='lightblue')
top_frame.pack(pady=10)

difficulty_frame = tk.Frame(root, bg='lightyellow')
difficulty_frame.pack(pady=10)

game_frame = tk.Frame(root,  bg='lightblue')
game_frame.pack(pady=10)

result_frame = tk.Frame(root, bg='lightblue')
result_frame.pack(pady=10)

# Create widgets
difficulty_var = tk.StringVar(value='easy')

difficulty_label = tk.Label(difficulty_frame, text="", font=('Arial', 12), bg='lightblue', fg='darkblue')
difficulty_label.pack()

# Mode selection (radio buttons) - positioned below the "Country Scramble" label
mode_var = tk.StringVar(value="untimed")

# Add a label for the mode selection below the game title
mode_label = tk.Label(root, text="Select Mode:", font=('Arial', 12), bg='lightblue', fg='darkblue')
mode_label.place(x=10, y=50)

# Add the "Untimed" and "Timed" radio buttons below the mode label (stacked vertically)
untimed_button = tk.Radiobutton(root, text="Untimed", variable=mode_var, value="untimed", bg='lightblue', fg='darkblue', font=('Arial', 10))
untimed_button.place(x=30, y=80)

timed_button = tk.Radiobutton(root, text="Timed", variable=mode_var, value="timed", bg='lightblue', fg='darkblue', font=('Arial', 10))
timed_button.place(x=30, y=110)

game_title_label = tk.Label(root, text="Find the country", font=('Arial', 12, 'bold'), bg='lightblue', fg='darkblue')
game_title_label.place(x=10 , y=10) 

start_button = tk.Button(top_frame, text="Start Game", command=start_game, font=('Arial', 12, 'bold'), bg='lightblue')
start_button.pack()

play_again_button = tk.Button(game_frame, text="Play again", command=start_game, font=('Arial', 12, 'bold'), bg='lightblue')
play_again_button.pack_forget()

scrambled_label = tk.Label(game_frame, text="Scrambled word will appear here", font=('Arial', 14, 'bold'), bg='lightblue')
scrambled_label.pack_forget()

guess_entry = tk.Entry(game_frame, font=('Arial', 12))
guess_entry.pack_forget()

check_button = tk.Button(game_frame, text="Check Guess", command=check_guess, font=('Arial', 12, 'bold'), bg='lightgreen')
check_button.pack_forget()

score_label = tk.Label(result_frame, text="Score: 0", font=('Arial', 14, 'bold'), bg='lightblue')
score_label.pack_forget()

result_label = tk.Label(result_frame, text="", font=('Arial', 12), bg='lightblue')
result_label.pack()

round_label = tk.Label(root, text="", font=('Arial', 14, 'bold'), bg='lightblue')
round_label.place(x=5, y=470)

# Timer label (for timed mode)
timer_label = tk.Label(root, text="", font=('Arial', 12), bg='lightblue')
timer_label.place(x=400, y=10)

hint_label = tk.Label(root, text="", font=('Arial', 12, 'bold'), bg='lightblue', fg='darkblue')
hint_label.place_forget()

# Create the Hint button under the time label
hint_button = tk.Button(root, text="Hint", command=lambda: use_hint(), font=('Arial', 12, 'bold' ), bg='lightblue', fg='darkblue')
hint_button.place_forget()

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=('Arial', 12, 'bold'), bg='lightblue', fg='darkblue')
high_score_label.place(x=350, y=10)

# Timer message label to show time-related alerts
timer_message_label = tk.Label(root, text="", font=('Arial', 12), bg='lightblue', fg='darkblue')
timer_message_label.pack()  # Adjust the position as needed

animated_gif = AnimatedGIF(root, "C:/Users/gtak2/source/repos/Word_Scramble/gifgit.gif")
animated_gif.pack() 

# Place the Exit button in the bottom-right corner
exit_button = tk.Button(root, text="Exit", command=exit_game, font=('Arial', 14, 'bold'), bg='red')
exit_button.place(relx=1.0, rely=1.0, anchor='se')  # Position at the bottom-right corner


# Start the Tkinter event loop
root.mainloop()
