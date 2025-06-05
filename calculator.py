import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to save calculation history to SQLite database
def save_calculation_history(expression, result):
    conn = sqlite3.connect('calculator_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            expression TEXT,
            result TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO history (expression, result)
        VALUES (?, ?)
    ''', (expression, result))
    conn.commit()
    conn.close()

# Function to perform calculations
def calculate():
    try:
        num1 = float(num1_entry.get())
        num2 = float(num2_entry.get())
        operator = operator_var.get()

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise ZeroDivisionError
            result = num1 / num2
        elif operator == '%':
            if num2 == 0:
                raise ZeroDivisionError
            result = num1 % num2
        elif operator == '//':
            if num2 == 0:
                raise ZeroDivisionError
            result = num1 // num2
        else:
            raise ValueError("Invalid operator")

        expression = f"{num1} {operator} {num2}"
        result_label.config(text=f"Result: {result}")
        save_calculation_history(expression, str(result))

    except ZeroDivisionError:
        messagebox.showerror("Error", "Division or modulo by zero is not allowed.")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Function to toggle full screen
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    if not is_fullscreen:
        root.geometry("900x700")  # Set window size when exiting fullscreen

# GUI setup using Tkinter
def setup_gui():
    global num1_entry, num2_entry, operator_var, result_label, root, is_fullscreen

    root = tk.Tk()
    root.title("Simple Calculator")
    is_fullscreen = True
    root.attributes("-fullscreen", is_fullscreen)
    root.configure(bg="#2C3E50")  # Background color

    # Padding frame for spacing
    padding_frame = tk.Frame(root, bg="#2C3E50")
    padding_frame.pack(padx=40, pady=40, fill="both", expand=True)

    # First Number
    tk.Label(padding_frame, text="First Number:", bg="#2C3E50", fg="white", font=("Arial", 24, "bold")).pack(pady=(0,10))
    num1_entry = tk.Entry(padding_frame, font=("Arial", 22), width=25, bg="#ECF0F1", fg="#2C3E50")
    num1_entry.pack(pady=(0,20))

    # Operator Label with large font
    tk.Label(padding_frame, text="Operator:", bg="#2C3E50", fg="white", font=("Arial", 24, "bold")).pack(pady=(0,10))

    # Frame for operator radio buttons horizontally aligned
    operator_frame = tk.Frame(padding_frame, bg="#2C3E50")
    operator_frame.pack(pady=(0,20))

    operator_var = tk.StringVar(value='+')
    operators = ['+', '-', '*', '/', '%', '//']
    for op in operators:
        rb = tk.Radiobutton(
            operator_frame,
            text=op,
            variable=operator_var,
            value=op,
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white",
            selectcolor="#27AE60",
            activebackground="#27AE60",
            activeforeground="white",
            width=3,
            indicatoron=0,
            relief="raised",
            bd=4,
            cursor="hand2"
        )
        rb.pack(side="left", padx=6)

    # Second Number
    tk.Label(padding_frame, text="Second Number:", bg="#2C3E50", fg="white", font=("Arial", 24, "bold")).pack(pady=(0,10))
    num2_entry = tk.Entry(padding_frame, font=("Arial", 22), width=25, bg="#ECF0F1", fg="#2C3E50")
    num2_entry.pack(pady=(0,20))

    # Calculate Button
    calculate_button = tk.Button(
        padding_frame,
        text="Calculate",
        command=calculate,
        font=("Arial", 18, "bold"),
        bg="#27AE60",
        fg="white",
        relief="raised",
        bd=6,
        activebackground="#2ECC71",
        activeforeground="white",
        cursor="hand2",
        width=12,
        height=1
    )
    calculate_button.pack(pady=(0,10))  # Small padding below

    # Result Label directly below Calculate button
    result_label = tk.Label(padding_frame, text="Result: ", bg="#2C3E50", fg="white", font=("Arial", 26, "bold"))
    result_label.pack(pady=(5,0))

    # Bind the Escape key to toggle full screen
    root.bind("<Escape>", toggle_fullscreen)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    setup_gui()
