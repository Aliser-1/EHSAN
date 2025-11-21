import tkinter as tk
from tkinter import font

# --- App-instellingen ---
root = tk.Tk()
root.title("Mooie Rekenmachine ✨")
root.geometry("360x520")
root.resizable(False, False)

# --- Lettertypen ---
display_font = font.Font(family="Segoe UI", size=28, weight="bold")
button_font = font.Font(family="Segoe UI", size=16, weight="bold")

# --- Thema-kleuren ---
themes = {
    "licht": {"bg": "white", "fg": "black", "btn_bg": "black", "btn_fg": "white",
              "special_bg": "#f0f0f0", "special_fg": "black"},
    "donker": {"bg": "#121212", "fg": "white", "btn_bg": "#2b2b2b", "btn_fg": "white",
               "special_bg": "#3b3b3b", "special_fg": "#00ff88"},
}

huidig_thema = "licht"

# --- Functies ---
uitdrukking = ""

def update_display(waarde):
    global uitdrukking
    uitdrukking += str(waarde)
    display_label.config(text=uitdrukking)

def clear_display():
    global uitdrukking
    uitdrukking = ""
    display_label.config(text="")

def delete_last():
    global uitdrukking
    uitdrukking = uitdrukking[:-1]
    display_label.config(text=uitdrukking)

def bereken():
    global uitdrukking
    try:
        resultaat = str(eval(uitdrukking))
        display_label.config(text=resultaat)
        uitdrukking = resultaat
    except:
        display_label.config(text="Fout")
        uitdrukking = ""

def wissel_thema():
    global huidig_thema
    huidig_thema = "donker" if huidig_thema == "licht" else "licht"
    pas_thema_toe()

def pas_thema_toe():
    thema = themes[huidig_thema]
    root.config(bg=thema["bg"])
    display_frame.config(bg=thema["bg"])
    display_label.config(bg=thema["bg"], fg=thema["fg"])
    button_frame.config(bg=thema["bg"])
    toggle_button.config(bg=thema["special_bg"], fg=thema["special_fg"],
                         activebackground=thema["btn_bg"], activeforeground=thema["btn_fg"])
    for knop in alle_knoppen:
        tekst = knop["text"]
        if tekst in ["C", "←", "="]:
            knop.config(bg=thema["special_bg"], fg=thema["special_fg"],
                        activebackground=thema["btn_bg"], activeforeground=thema["btn_fg"])
        else:
            knop.config(bg=thema["btn_bg"], fg=thema["btn_fg"],
                        activebackground="#333333", activeforeground="white")

# --- Weergave ---
display_frame = tk.Frame(root)
display_frame.pack(expand=True, fill="both", pady=(10, 0))

display_label = tk.Label(display_frame, text="", anchor="e", padx=20, font=display_font)
display_label.pack(expand=True, fill="both")

# --- Knoppen ---
button_frame = tk.Frame(root)
button_frame.pack(expand=True, fill="both")

knoppen = [
    ["C", "←", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""]
]

alle_knoppen = []

for rij in knoppen:
    frame = tk.Frame(button_frame)
    frame.pack(expand=True, fill="both")
    for tekst in rij:
        if tekst == "":
            tk.Label(frame).pack(side="left", expand=True, fill="both", padx=2, pady=2)
            continue

        def make_lambda(x=tekst):
            if x == "C": return clear_display
            elif x == "←": return delete_last
            elif x == "=": return bereken
            else: return lambda: update_display(x)

        knop = tk.Button(frame, text=tekst, font=button_font, borderwidth=0,
                         relief="flat", command=make_lambda())
        knop.pack(side="left", expand=True, fill="both", padx=3, pady=3)
        alle_knoppen.append(knop)

# --- Wisselknop voor thema ---
toggle_button = tk.Button(root, text="Wissel thema", font=("Segoe UI", 12, "bold"),
                          borderwidth=0, relief="flat", command=wissel_thema)
toggle_button.pack(fill="x", pady=(5, 10), padx=10)

# --- Start met licht thema ---
pas_thema_toe()

root.mainloop()