import tkinter
import math

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

# --- WINDOW SETUP ---
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45),
                      background=color_black, foreground=color_white,
                      anchor="e", width=4)
label.grid(row=0, column=0, columnspan=4, sticky="we")

# --- GLOBALS ---
A = None
B = None
operator = None

# --- HELPER FUNCTIONS ---
def remove_zero_decimal(num):
    """Removes unnecessary .0 from floats."""
    if num % 1 == 0:
        num = int(num)
    return str(num)

def clear_all():
    global A, B, operator
    A = None
    B = None
    operator = None
    label["text"] = "0"

def calculate():
    """Perform operation based on A, operator, and label text."""
    global A, operator
    if A is None or operator is None:
        return
    try:
        B = float(label["text"])
        if operator == "+":
            result = A + B
        elif operator == "-":
            result = A - B
        elif operator == "×":
            result = A * B
        elif operator == "÷":
            if B == 0:
                label["text"] = "Error"
                A = None
                operator = None
                return
            result = A / B
        label["text"] = remove_zero_decimal(result)
        A = result
        operator = None
    except Exception:
        label["text"] = "Error"
        A = None
        operator = None

# --- MAIN BUTTON HANDLER ---
def button_clicked(value):
    global A, B, operator

    # Handle arithmetic operators
    if value in right_symbols:
        if value == "=":
            calculate()
        else:
            A = float(label["text"])
            operator = value
            label["text"] = "0"
        return

    # Handle top row
    if value in top_symbols:
        if value == "AC":
            clear_all()
        elif value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except:
                pass
        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except:
                pass
        return

    # Handle square root
    if value == "√":
        try:
            num = float(label["text"])
            if num < 0:
                label["text"] = "Error"
            else:
                result = math.sqrt(num)
                label["text"] = remove_zero_decimal(result)
        except:
            label["text"] = "Error"
        return

    # Handle numbers and dot
    if value == ".":
        if "." not in label["text"]:
            label["text"] += value
    elif value in "0123456789":
        if label["text"] == "0" or label["text"] == "Error":
            label["text"] = value
        else:
            label["text"] += value

# --- BUTTON CREATION ---
for row in range(len(button_values)):
    for column in range(len(button_values[0])):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
                                width=4, height=1,
                                command=lambda value=value: button_clicked(value))
        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)
        button.grid(row=row + 1, column=column)

frame.pack()

# --- CENTER WINDOW ---
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()