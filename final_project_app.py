import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def create_database():
    """Create the SQLite database and table if they do not already exist."""
    connection = sqlite3.connect("student_preferences.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            favorite_language TEXT NOT NULL,
            comments TEXT
        )
    """)

    connection.commit()
    connection.close()


def clear_fields():
    """Clear all input fields."""
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    language_combobox.set("")
    comments_entry.delete(0, tk.END)


def save_data():
    """Validate user input and save it into the SQLite database."""
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    favorite_language = language_combobox.get().strip()
    comments = comments_entry.get().strip()

    if name == "":
        messagebox.showerror("Input Error", "Please enter your name.")
        return

    if age == "":
        messagebox.showerror("Input Error", "Please enter your age.")
        return

    if not age.isdigit():
        messagebox.showerror("Input Error", "Age must be a number.")
        return

    if favorite_language == "":
        messagebox.showerror("Input Error", "Please select a favorite programming language.")
        return

    connection = sqlite3.connect("student_preferences.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO preferences (name, age, favorite_language, comments)
        VALUES (?, ?, ?, ?)
    """, (name, int(age), favorite_language, comments))

    connection.commit()
    connection.close()

    messagebox.showinfo("Success", "Your information was saved successfully!")
    clear_fields()


def view_records():
    """Open a new window and display all saved records from the database."""
    records_window = tk.Toplevel(root)
    records_window.title("Saved Records")
    records_window.geometry("650x350")
    records_window.configure(bg="#f2f2f2")

    title = tk.Label(
        records_window,
        text="Saved Student Preferences",
        font=("Arial", 16, "bold"),
        bg="#f2f2f2",
        fg="#333333",
        pady=10
    )
    title.pack()

    records_text = tk.Text(
        records_window,
        width=75,
        height=15,
        font=("Arial", 10)
    )
    records_text.pack(padx=10, pady=10)

    connection = sqlite3.connect("student_preferences.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, age, favorite_language, comments
        FROM preferences
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    if not records:
        records_text.insert(tk.END, "No records found.")
    else:
        for record in records:
            name, age, language, comments = record
            records_text.insert(
                tk.END,
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Favorite Language: {language}\n"
                f"Comments: {comments}\n"
                f"{'-' * 50}\n"
            )

    records_text.config(state="disabled")


def show_about():
    """Show information about the app."""
    messagebox.showinfo(
        "About",
        "Student Preference Tracker\n\n"
        "Created for IST 4320 Final Project.\n\n"
        "This app collects user input and saves it into a local SQLite database."
    )


# Create database before the app starts
create_database()

# Main window
root = tk.Tk()
root.title("Student Preference Tracker")
root.geometry("600x450")
root.configure(bg="#f2f2f2")

# Menu bar
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Clear Form", command=clear_fields)
file_menu.add_command(label="View Records", command=view_records)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Title label
title_label = tk.Label(
    root,
    text="Student Preference Tracker",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2",
    fg="#333333",
    pady=15
)
title_label.pack()

# Form area
form_frame = tk.Frame(root, bg="#f2f2f2")
form_frame.pack(pady=10)

name_label = tk.Label(
    form_frame,
    text="Name:",
    font=("Arial", 12),
    bg="#f2f2f2"
)
name_label.grid(row=0, column=0, sticky="w", padx=10, pady=8)

name_entry = tk.Entry(
    form_frame,
    font=("Arial", 12),
    width=30
)
name_entry.grid(row=0, column=1, padx=10, pady=8)

age_label = tk.Label(
    form_frame,
    text="Age:",
    font=("Arial", 12),
    bg="#f2f2f2"
)
age_label.grid(row=1, column=0, sticky="w", padx=10, pady=8)

age_entry = tk.Entry(
    form_frame,
    font=("Arial", 12),
    width=30
)
age_entry.grid(row=1, column=1, padx=10, pady=8)

language_label = tk.Label(
    form_frame,
    text="Favorite Language:",
    font=("Arial", 12),
    bg="#f2f2f2"
)
language_label.grid(row=2, column=0, sticky="w", padx=10, pady=8)

language_combobox = ttk.Combobox(
    form_frame,
    values=["Python", "JavaScript", "C++", "Java", "SQL", "Other"],
    font=("Arial", 12),
    width=28,
    state="readonly"
)
language_combobox.grid(row=2, column=1, padx=10, pady=8)

comments_label = tk.Label(
    form_frame,
    text="Comments:",
    font=("Arial", 12),
    bg="#f2f2f2"
)
comments_label.grid(row=3, column=0, sticky="w", padx=10, pady=8)

comments_entry = tk.Entry(
    form_frame,
    font=("Arial", 12),
    width=30
)
comments_entry.grid(row=3, column=1, padx=10, pady=8)

# Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=20)

save_button = tk.Button(
    button_frame,
    text="Save Information",
    command=save_data,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    width=18,
    padx=5,
    pady=5
)
save_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=("Arial", 12),
    bg="#cccccc",
    fg="black",
    width=10,
    padx=5,
    pady=5
)
clear_button.grid(row=0, column=1, padx=10)

view_button = tk.Button(
    button_frame,
    text="View Records",
    command=view_records,
    font=("Arial", 12),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    activeforeground="white",
    width=12,
    padx=5,
    pady=5
)
view_button.grid(row=0, column=2, padx=10)

# Instruction label
instruction_label = tk.Label(
    root,
    text="Use the form to save your information. Use View Records to see saved entries.",
    font=("Arial", 10),
    bg="#f2f2f2",
    fg="#555555"
)
instruction_label.pack(pady=5)

# Start the app
root.mainloop()