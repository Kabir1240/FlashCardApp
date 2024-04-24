from tkinter import *
from tkinter_widgets import TkinterWidgets
import pandas
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
CARD_BACK_PATH = "images/card_back.png"
CARD_FRONT_PATH = "images/card_front.png"
RIGHT_IMAGE_PATH = "images/right.png"
WRONG_IMAGE_PATH = "images/wrong.png"
WORDS_PATH = "data/kanji_and_furigana_200.csv"
TO_LEARN_PATH = "data/to_learn.csv"

TITLE_FONT = ("Arial", 40, "italic")
KANJI_FONT = ("Arial", 60, "bold")
FURIGANA_FONT = ("Arial", 30, "bold")

TIME_BEFORE_DISPLAYING_ENGLISH = 3000


class FlashCardApp:
    def __init__(self):
        """
        initialize variables, widgets and data required for the FlashCardApp
        """

        # init variables for later
        self.title_text = None
        self.kanji_text = None
        self.furigana_text = None
        self.canvas_image = None
        self.flip_timer = None
        self.current_card = {}

        try:
            self.data = pandas.read_csv(TO_LEARN_PATH).to_dict(orient="records")
        except FileNotFoundError:
            print("file not found")
            self.data = pandas.read_csv(WORDS_PATH).to_dict(orient="records")

        # create window and images
        self.window = Tk()
        self.window.title("Learn Japanese")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # create data struct for widgets
        self.widgets = TkinterWidgets()

        # create required widgets
        self.create_photoimages()
        self.create_canvas()
        self.create_buttons()

        # window main loop
        self.window.mainloop()

    def create_photoimages(self) -> None:
        """
        creates a PhotoImage dictionary which is stored in the widgets data struct
        :return: None
        """

        # create 4 PhotoImages
        card_back = PhotoImage(file=CARD_BACK_PATH)
        card_front = PhotoImage(file=CARD_FRONT_PATH)
        right_button_image = PhotoImage(file=RIGHT_IMAGE_PATH)
        wrong_button_image = PhotoImage(file=WRONG_IMAGE_PATH)

        # create dictionary
        image_dict = {
            "card back": card_back,
            "card front": card_front,
            "known button": right_button_image,
            "unknown button": wrong_button_image,
        }

        # store in widgets
        self.widgets.add_image_dict(image_dict)

    def create_canvas(self) -> None:
        """
        creates a canvas for the flash cards and stores it in widgets
        :return: None
        """

        # create canvas with logo image
        canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        card_front = self.widgets.get_images("card front")
        self.canvas_image = canvas.create_image(400, 263, image=card_front)
        canvas.grid(row=0, column=0, columnspan=2)

        # create texts on canvas to display the title, kanji and furigana
        self.title_text = canvas.create_text(400, 150, text="Title", fill="black", font=TITLE_FONT)
        self.kanji_text = canvas.create_text(400, 263, text="Word", fill="black", font=KANJI_FONT)
        self.furigana_text = canvas.create_text(400, 350, text="Word", fill="black", font=FURIGANA_FONT)

        # store canvas in widgets
        self.widgets.add_canvas("canvas", canvas)

    def create_buttons(self) -> None:
        """
        creates a Button dictionary which is stored in the widgets data struct
        :return: None
        """

        # create 2 buttons
        unknown_button_img = self.widgets.get_images("unknown button")
        known_button_image = self.widgets.get_images("known button")
        unknown_button = Button(image=unknown_button_img, highlightthickness=0, command=self.update_word)
        known_button = Button(image=known_button_image, highlightthickness=0, command=self.remove_word)

        # position buttons
        unknown_button.grid(row=1, column=0)
        known_button.grid(row=1, column=1)

        # create dictionary
        buttons = {
            "known button": known_button,
            "unknown button": unknown_button,
        }

        # store buttons in widgets
        self.widgets.add_button_dict(buttons)

    def remove_word(self) -> None:
        """
        removes current card from card collection and stores remaining cards in to_learn.csv
        :return: None
        """

        # try to remove word. if the word doesn't exist, pass
        try:
            self.data.remove(self.current_card)
        except ValueError:
            pass
        else:
            updated_data = pandas.DataFrame(self.data)
            updated_data.to_csv(TO_LEARN_PATH, index=False)

        # update to next word
        self.update_word()

    def update_word(self) -> None:
        """
        flips card to japanese kanji and updates the word
        :return: None
        """

        # remove any previous timer, if it exists
        if self.flip_timer is not None:
            self.window.after_cancel(self.flip_timer)

        # flip card
        canvas = self.widgets.get_canvas("canvas")
        card_front = self.widgets.get_images("card front")
        word = choice(self.data)
        self.current_card = word
        canvas.itemconfig(self.canvas_image, image=card_front)

        # display new word
        canvas.itemconfig(self.title_text, fill="black", text="Japanese")
        canvas.itemconfig(self.kanji_text, fill="black", text=word["Kanji"])
        canvas.itemconfig(self.furigana_text, text=word["Furigana"])

        # display english translation 3 seconds later
        self.flip_timer = self.window.after(TIME_BEFORE_DISPLAYING_ENGLISH, self.flip_card, canvas)

    def flip_card(self, canvas:Canvas) -> None:
        """
        flips card to english translation
        :param canvas: canvas for FlashCardApp
        :return: None
        """

        # flip card
        card_back = self.widgets.get_images("card back")
        canvas.itemconfig(self.canvas_image, image=card_back)

        # display english translation
        canvas.itemconfig(self.title_text, fill="white", text="English")
        canvas.itemconfig(self.kanji_text, fill="white", text=self.current_card["English"])
        canvas.itemconfig(self.furigana_text, text="")
