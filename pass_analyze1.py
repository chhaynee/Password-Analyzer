import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import bcrypt

# File to store users' data
USER_DATA_FILE = "user_data1.json"

# Define the character sets for password generation
lowCase = "abcdefghijklmnopqrstuvxyz"
upCase = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
Numbers = "0123456789"
SpecialChar = "£$&()*+[]@#^-_!?"
AllChars = lowCase + upCase + Numbers + SpecialChar

# Function to generate a secure password
def generate_password(length=24):
    return ''.join(random.choice(AllChars) for i in range(length))

# Function to analyze password strength
def analyze_password(password):
    if len(password) < 12:
        return "Too short"
    elif not any(char.isupper() for char in password):
        return "Weak (missing uppercase letter)"
    elif not any(char.islower() for char in password):
        return "Weak (missing lowercase letter)"
    elif not any(char.isdigit() for char in password):
        return "Weak (missing number)"
    elif not any(char in SpecialChar for char in password):
        return "Weak (missing special character)"
    else:
        return "Strong"

# Function to hash and store password securely
def store_password(username, password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Load existing user data from file
    users = load_user_data()

    # Store the hashed password for the user
    users[username] = hashed_password.decode('utf-8')

    # Save updated user data back to file
    save_user_data(users)

# Function to load user data from JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save user data to JSON file
def save_user_data(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# GUI function for submit button
def on_submit():
    username = username_entry.get()
    password = password_entry.get()

    if not username:
        messagebox.showerror("Error", "Username cannot be empty.")
        return

    if password_choice.get() == "generate":
        password = generate_password()  # Generate a secure password
    
    # Automatically populate the password input field with the generated password if applicable
    if password_choice.get() == "generate":
        password_entry.delete(0, tk.END)  # Clear the current text in the password field
        password_entry.insert(0, password)  # Insert the generated password
    
    # Analyze the password
    strength = analyze_password(password)

    if strength == "Strong":
        store_password(username, password)
        messagebox.showinfo("Success", f"Password saved for {username}.\nGenerated password: {password}")
    else:
        messagebox.showwarning("Weak Password", f"Password is {strength}.\nPlease choose a stronger password.")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Password Analyzer")
root.geometry("400x350")

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack(pady=5)

# Password choice radio buttons (user input or random generation)
password_choice = tk.StringVar(value="input")
password_choice_input = tk.Radiobutton(root, text="Input your own password", variable=password_choice, value="input")
password_choice_input.pack(pady=5)
password_choice_generate = tk.Radiobutton(root, text="Generate a secure password", variable=password_choice, value="generate")
password_choice_generate.pack(pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
