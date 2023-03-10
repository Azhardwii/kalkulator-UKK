import tkinter as tk

LARGE_FONT_STYLE = ("Satoshi", 40, "bold")
SMALL_FONT_STYLE = ("Satoshi", 16)
DIGITS_FONT_STYLE = ("Satoshi", 24, "bold")
DEFAULT_FONT_STYLE = ("Satoshi", 20)
DEFAULT_FONT_STYLE_BOLD = ("Satoshi", 20, "bold")
OPERATION = "#FFB217"
OPERATION_2 = "#F0F0F0"
DISPLAY_BLACK = "#FFFFFF"
BUTTON_BLACK = "#FAFAFA"
LABEL_COLOR = "#222222"
BLUE_COLOR = "#FE971E"

class Kalkulator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Kalkulator Azhar")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.digits = {
            1: (1, 1), 2: (1, 2), 3: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            7: (3, 1), 8: (3, 2), 9: (3, 3),
            '.': (4, 1), 0: (4, 2), '\u232B':(4, 3)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<Delete>", lambda event: self.clear())
        self.window.bind("<x>", lambda event: self.square())
        self.window.bind("<v>", lambda event: self.sqrt())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_delete_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=BUTTON_BLACK, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=BUTTON_BLACK, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label
    
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=BUTTON_BLACK)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=BUTTON_BLACK, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        check_current_expression = self.current_expression + operator

        if check_current_expression[:-1] != "":
            if float(check_current_expression[:-1]):
                self.current_expression += operator
                self.total_expression += self.current_expression
                self.current_expression = ""
                self.update_total_label()
                self.update_label()
            else:
                self.total_expression += self.current_expression
                self.current_expression = ""
                self.update_total_label()
                self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OPERATION_2, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="AC", bg=OPERATION_2, fg=BLUE_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)


    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OPERATION_2, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()
        
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221a", bg=OPERATION_2, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_delete_button(self):
        button = tk.Button(self.buttons_frame, text="\u232B", bg=OPERATION_2, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.delete)
        button.grid(row=4, column=3, sticky=tk.NSEW)

    def delete(self):
        checkStrLen = len(str(self.current_expression))
        if checkStrLen == 1:
            self.current_expression = "0"
            self.update_label()
        else:
            self.current_expression = str(eval(self.current_expression[:-1]))
            self.update_label()


    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=BLUE_COLOR, fg=DISPLAY_BLACK, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=4, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:9])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    kal = Kalkulator()
    kal.run()