import tkinter as tk
import random

# Set up main window
root = tk.Tk()
root.title("⭐ Catch the Star Game")
root.geometry("400x400")

score = 0
star_button = None

def show_star():
    global star_button

    # Remove previous star
    if star_button:
        star_button.destroy()

    # Random x, y position
    x = random.randint(50, 300)
    y = random.randint(50, 300)

    # Create new star
    star_button = tk.Button(root, text="🌟", font=("Arial", 20), command=star_caught)
    star_button.place(x=x, y=y)

    # After 1000ms (1 second), hide the star if not clicked
    root.after(1000, lambda: star_button and star_button.destroy())

def star_caught():
    global score, star_button
    score += 1
    star_button.destroy()
    score_label.config(text=f"Score: {score}")
    show_star()

# Add score label
score_label = tk.Label(root, text="Score: 0", font=("Arial", 16))
score_label.pack(pady=10)

# Start button
start_button = tk.Button(root, text="Start Game", font=("Arial", 14), command=show_star)
start_button.pack(pady=20)

# Run the GUI
root.mainloop()
