from tkinter import *
from tkinter_widgets import TkinterWidgets
import pandas
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
CARD_BACK_PATH = "images/card_back.png"
CARD_FRONT_PATH = "images/card_front.png"
RIGHT_IMAGE_PATH = "images/right.png"
WRONG_IMAGE_PATH = "images/wrong.png"
WORDS_PATH = "data/kanji_and_furigana.csv"

TITLE_FONT = ("Arial", 40, "italic")
KANJI_FONT = ("Arial", 60, "bold")
FURIGANA_FONT = ("Arial", 30, "bold")


class FlashCardApp:
    def __init__(self):
        # init variables for later
        self.title_text = None
        self.kanji_text = None
        self.furigana_text = None
        self.canvas_image = None
        self.data = pandas.read_csv(WORDS_PATH).to_dict(orient="records")

        # create window and images
        self.window = Tk()
        self.window.title("Learn Japanese")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # create PhotoImages for later use
        self.card_back = PhotoImage(file=CARD_BACK_PATH)
        self.card_front = PhotoImage(file=CARD_FRONT_PATH)
        self.right_button_image = PhotoImage(file=RIGHT_IMAGE_PATH)
        self.wrong_button_image = PhotoImage(file=WRONG_IMAGE_PATH)

        # create data struct for widgets
        self.widgets = TkinterWidgets()

        # create required widgets
        self.create_canvas()
        self.create_buttons()

        self.window.mainloop()

    def create_canvas(self):
        # create canvas with logo image
        canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas_image = canvas.create_image(400, 263, image=self.card_front)
        canvas.grid(row=0, column=0, columnspan=2)

        self.title_text = canvas.create_text(400, 150, text="Title", fill="black", font=TITLE_FONT)
        self.kanji_text = canvas.create_text(400, 263, text="Word", fill="black", font=KANJI_FONT)
        self.furigana_text = canvas.create_text(400, 350, text="Word", fill="black", font=FURIGANA_FONT)

        self.widgets.add_canvas("canvas", canvas)

    def create_buttons(self):
        wrong_button = Button(image=self.wrong_button_image, highlightthickness=0, command=self.update_word)
        right_button = Button(image=self.right_button_image, highlightthickness=0, command=self.update_word)

        wrong_button.grid(row=1, column=0)
        right_button.grid(row=1, column=1)

        buttons = {
            "right button": right_button,
            "wrong button": wrong_button,
        }

        self.widgets.add_button_dict(buttons)

    def update_word(self):
        canvas = self.widgets.get_canvas("canvas")
        word = choice(self.data)
        canvas.itemconfig(self.canvas_image, image=self.card_front)

        canvas.itemconfig(self.title_text, fill="black", text="Japanese")
        canvas.itemconfig(self.kanji_text, fill="black", text=word["Kanji"])
        canvas.itemconfig(self.furigana_text, text=word["Furigana"])

        self.window.after(3000, self.show_translation, canvas, word)

    def show_translation(self, canvas:Canvas, word):
        canvas.itemconfig(self.canvas_image, image=self.card_back)
        canvas.itemconfig(self.title_text, fill="white", text="English")
        canvas.itemconfig(self.kanji_text, fill="white", text=word["English"])
        canvas.itemconfig(self.furigana_text, text="")
