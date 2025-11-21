import tkinter as tk
from tkinter import font
import ast
import operator

# --- Veilige evaluatie ---
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

def safe_eval(expr: str):
    expr = expr.replace(',', '.').replace(' ', '')
    try:
        node = ast.parse(expr, mode='eval')
    except Exception:
        raise ValueError("Ongeldige uitdrukking")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if hasattr(ast, "Constant") and isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            else:
                raise ValueError("Ongeldige waarde")
        if isinstance(n, ast.Num):
            return n.n
        if isinstance(n, ast.BinOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Ongeldige operator")
            return ALLOWED_OPERATORS[op_type](_eval(n.left), _eval(n.right))
        if isinstance(n, ast.UnaryOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Ongeldige uniaire operator")
            return ALLOWED_OPERATORS[op_type](_eval(n.operand))
        raise ValueError("Ongeldige structuur")
    return _eval(node)

class ColorCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("rekenmachine")
        self.resizable(False, False)
        self._make_fonts()
        self._set_colors()
        self._build_ui()
        self._bind_keys()

    def _make_fonts(self):
        self.display_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=18, weight="bold")

    def _set_colors(self):
        self.bg = "#ffffff"  # Wit achtergrond
        self.display_bg = "#ffffff"
        self.display_fg = "#000000"
        self.num_bg = "#1e90ff"      # Blauw voor cijfers
        self.op_bg = "#b8860b"       # Donkergeel voor operatoren
        self.btn_fg = "#ffffff"       # Witte letters
        self.configure(bg=self.bg)

    def _build_ui(self):
        pad = 10
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(self, textvariable=self.display_var, font=self.display_font,
                                bd=0, justify="right", relief="flat", readonlybackground=self.display_bg,
                                fg=self.display_fg, insertbackground=self.display_fg, state="readonly", width=16)
        self.display.grid(row=0, column=0, columnspan=4, padx=pad, pady=(pad,0), ipady=18, sticky="we")

        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "⌫", "="],
        ]

        # Knoppen aanmaken met juiste kleuren
        for r, row in enumerate(buttons, start=1):
            for c, label in enumerate(row):
                cmd = lambda x=label: self._on_button(x)
                b = tk.Button(self, text=label, font=self.button_font, bd=0, command=cmd)
                b.grid(row=r, column=c, padx=6, pady=6, ipadx=10, ipady=14, sticky="nsew")

                # Operatoren = donkergeel, andere knoppen = blauw
                if label in ["÷","×","-","+","="]:
                    b.configure(bg=self.op_bg, fg=self.btn_fg)
                else:
                    b.configure(bg=self.num_bg, fg=self.btn_fg)

                b.configure(relief="flat", highlightthickness=0)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1, minsize=80)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)

    def _bind_keys(self):
        self.bind("<Key>", self._on_keypress)
        self.bind("<Return>", lambda e: self._on_button("="))
        self.bind("<BackSpace>", lambda e: self._on_button("⌫"))
        self.bind("<Escape>", lambda e: self._on_button("AC"))

    def _on_keypress(self, event):
        ch = event.char
        if ch.isdigit():
            self._on_button(ch)
        elif ch in "+-*/().":
            self._on_button("×" if ch=="*" else "÷" if ch=="/" else ch)
        elif ch=="%":
            self._on_button("%")

    def _on_button(self, label):
        current = self.display_var.get()
        if current=="": current="0"

        if label=="AC":
            self.display_var.set("0")
            return
        if label=="⌫":
            self.display_var.set("0" if len(current)<=1 else current[:-1])
            return
        if label=="+/-":
            try:
                val = safe_eval(current.replace("×","*").replace("÷","/"))
                val = -val
                self.display_var.set(str(int(val)) if float(val).is_integer() else str(val))
            except Exception:
                self.display_var.set("Fout")
            return
        if label=="=":
            expr = current.replace("×","*").replace("÷","/")
            expr = expr.rstrip("+-*/.")
            try:
                result = safe_eval(expr)
                if isinstance(result,float) and result.is_integer(): result=int(result)
                self.display_var.set(str(result))
            except Exception:
                self.display_var.set("Fout")
            return
        if label=="%":
            try:
                val = safe_eval(current.replace("×","*").replace("÷","/"))
                val = val/100.0
                self.display_var.set(str(val))
            except Exception:
                self.display_var.set("Fout")
            return

        # Cijfers en punt toevoegen
        if current=="0" and (label.isdigit() or label=="."):
            new = label
        else:
            ops = set(["+", "-", "×", "÷", "*", "/"])
            if label in ops:
                new = current[:-1]+label if current[-1] in ops else current+label
            else:
                import re
                if label==".":
                    parts=re.split(r'[\+\-\×\÷\*\/]', current)
                    if "." in parts[-1]: return
                new=current+label
        self.display_var.set(new)

if __name__=="__main__":
    app=ColorCalc()
    app.mainloop()