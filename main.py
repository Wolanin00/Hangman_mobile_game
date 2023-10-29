from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

import re
import random


class MenuWindow(Screen):
    """
    Menu Window Screen class

    :return: None
    """
    def __init__(self, **kwargs):
        super(MenuWindow, self).__init__(**kwargs)

    def start_game(self):
        """
        Start game.
        Every click on `start_game` clear data and start game from the beginning.

        :return: None
        """
        word_to_find = generate_random_sentence().replace(' ', '\n')
        sm.get_screen("game").current_word = re.sub(r'[a-zA-Z]', ' _', word_to_find).replace('\n', ' \n')
        sm.get_screen("game").word_to_find = word_to_find
        sm.get_screen("game").entered_words = []
        sm.get_screen("game").wrong_words = 0
        sm.get_screen("game").remove_canvas()
        sm.current = 'game'

    def go_to_options(self):
        """
        Function to go option screen.

        :return: None
        """
        sm.current = 'options'


class GameWindow(Screen):
    """
    Main Game Screen.
    Every occurs on page generate random sentence to find.

    :return: None
    """

    entered_words = []
    word_to_find = ""
    current_word = StringProperty()
    txt = StringProperty()
    error_message = StringProperty()
    wrong_words = 0
    hangman_draw_color = (0, 0, 0)

    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.txt = ""
        self.error_message = ""

    @staticmethod
    def find_indices_with_loop(word, search_letter) -> list:
        """
        Static function which find indices with loop.

        :param word:
        :param search_letter:
        :return: indices
        """
        indices = []
        for i, letter in enumerate(word):
            if letter == search_letter:
                indices.append(i)
        return indices

    def back_menu(self):
        """
        Function to go to menu screen.

        :return: None
        """
        sm.current = 'menu'

    def enter_letter(self):
        """
        Function check error handling when letter entered.
        Function calculate wrong added char and updating hangman draw.

        :return: None
        """
        pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\/\|`\'"]'
        if len(self.ids.input_text_game_page.text) == 0:
            self.show_error(message='Can not provide empty field!')
            self.ids.input_text_game_page.text = ""
        elif len(self.ids.input_text_game_page.text) > 1:
            self.show_error(message='Provide only one character')
            self.ids.input_text_game_page.text = ""
        elif self.ids.input_text_game_page.text == ' ':
            self.show_error(message='Provide a letter instead of a space bar')
            self.ids.input_text_game_page.text = ""
        elif self.ids.input_text_game_page.text == chr(9):
            self.show_error(message='Provide a letter instead of a tab')
            self.ids.input_text_game_page.text = ""
        elif self.ids.input_text_game_page.text.isdigit():
            self.show_error(message='Provide a letter instead of a number')
            self.ids.input_text_game_page.text = ""
        elif re.search(pattern, self.ids.input_text_game_page.text):
            self.show_error(message='Provide a letter instead of a special characters')
            self.ids.input_text_game_page.text = ""
        else:
            if self.ids.input_text_game_page.text.lower().isalpha():
                if self.ids.input_text_game_page.text.lower() not in self.entered_words:
                    self.entered_words.append(self.ids.input_text_game_page.text.lower())
                    if self.ids.input_text_game_page.text.lower() in self.word_to_find.lower():
                        all_index = self.find_indices_with_loop(self.word_to_find.lower(), self.ids.input_text_game_page.text.lower())
                        temp = list(self.ids.current_word.text)
                        for index in all_index:
                            temp[1+index*2] = self.word_to_find[index]
                        self.ids.current_word.text = ''.join(temp)
                        if '_' not in self.ids.current_word.text:
                            self.show_won_popup()
                    else:
                        self.wrong_words += 1
                        if self.wrong_words == 1:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.2,
                                    self.height * 0.55,
                                    self.width * 0.8,
                                    self.height * 0.55],
                                    width=2)
                        elif self.wrong_words == 2:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.35,
                                    self.height * 0.55,
                                    self.width * 0.35,
                                    self.height * 0.9],
                                    width=2)
                        elif self.wrong_words == 3:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.35,
                                    self.height * 0.9,
                                    self.width * 0.6,
                                    self.height * 0.9],
                                    width=2)
                        elif self.wrong_words == 4:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.9,
                                    self.width * 0.6,
                                    self.height * 0.85],
                                    width=2)
                        elif self.wrong_words == 5:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(circle=(
                                    self.width * 0.6,
                                    self.height * 0.8,
                                    self.height * 0.05),
                                    width=2)
                        elif self.wrong_words == 6:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.75,
                                    self.width * 0.6,
                                    self.height * 0.65],
                                    width=2)
                        elif self.wrong_words == 7:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.65,
                                    self.width * 0.5,
                                    self.height * 0.58],
                                    width=2)
                        elif self.wrong_words == 8:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.65,
                                    self.width * 0.7,
                                    self.height * 0.58],
                                    width=2)
                        elif self.wrong_words == 9:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.7,
                                    self.width * 0.5,
                                    self.height * 0.75],
                                    width=2)
                        elif self.wrong_words == 10:
                            with self.canvas:
                                Color(*self.hangman_draw_color)
                                Line(points=[
                                    self.width * 0.6,
                                    self.height * 0.7,
                                    self.width * 0.7,
                                    self.height * 0.75],
                                    width=2)
                            self.show_lose_popup()
                    self.ids.input_text_game_page.text = ""
                else:
                    self.show_error(message='You have already entered this letter!')
                    self.ids.input_text_game_page.text = ""
            else:
                self.show_error(message='Invalid character!')
                self.ids.input_text_game_page.text = ""

    def go_menu(self, instance):
        """
        Function go to menu screen.

        :param instance: game instance
        :return: None
        """
        sm.transition.direction = 'right'
        sm.current = 'menu'
        self.lose_popup.dismiss()

    def play_again(self, instance):
        """
        Function play again.

        :param instance: game instance
        :return: None
        """
        word_to_find = generate_random_sentence().replace(' ', '\n')
        self.current_word = re.sub(r'[a-zA-Z]', ' _', word_to_find).replace('\n', ' \n')
        self.word_to_find = word_to_find
        self.entered_words = []
        self.wrong_words = 0
        self.remove_canvas()
        self.lose_popup.dismiss()

    def show_lose_popup(self):
        """
        Function which show lose popup witch `go menu` ang `play again` buttons.

        :return: None
        """

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='You lose the game', font_size='30'))
        buttons = BoxLayout(orientation='horizontal')
        go_menu_button = Button(text='Go menu')
        go_menu_button.bind(on_release=self.go_menu)
        buttons.add_widget(go_menu_button)
        play_again_button = Button(text='Play again')
        play_again_button.bind(on_release=self.play_again)
        buttons.add_widget(play_again_button)
        content.add_widget(buttons)

        self.lose_popup = Popup(title='You Lose', content=content, size_hint=(None, None), size=(800, 600))
        self.lose_popup.open()

    def show_won_popup(self):
        """
        Function which show won popup witch `go menu` ang `play again` buttons.

        :return: None
        """

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='You won the game', font_size='30'))
        buttons = BoxLayout(orientation='horizontal')
        go_menu_button = Button(text='Go menu')
        go_menu_button.bind(on_release=self.go_menu)
        buttons.add_widget(go_menu_button)
        play_again_button = Button(text='Play again')
        play_again_button.bind(on_release=self.play_again)
        buttons.add_widget(play_again_button)
        content.add_widget(buttons)

        self.lose_popup = Popup(title='You Won', content=content, size_hint=(None, None), size=(800, 600))
        self.lose_popup.open()

    def remove_canvas(self):
        """
        Funtion which remove hangman canvas to start again with clear board.

        :return: None
        """
        for instruction in self.canvas.children:
            if isinstance(instruction, Line):
                self.canvas.remove(instruction)

    def show_error(self, message=""):
        """
        Function showing error for error handling with customize error message

        :param message: error message to display
        :return: None
        """
        self.ids.error_message_game_window.text = message
        self.ids.error_message_game_window.opacity = 1
        Clock.schedule_once(self.hide_error, 2)

    def hide_error(self, dt):
        """
        Function which hide error after 2 second presented.

        :param dt:
        :return: None
        """
        self.ids.error_message_game_window.opacity = 0


class OptionsWindow(Screen):
    """
    Game Option Screen.
    Possible to change theme between dark and light mode

    :return: None
    """

    def back_menu(self):
        """
        Funtion go back to Menu.

        :return: None
        """
        sm.current = 'menu'

    def __init__(self, **kwargs):
        super(OptionsWindow, self).__init__(**kwargs)

    def change_to_dark_mode(self):
        """
        Funtion changing theme into dark mode.

        :return: None
        """
        for screen_name in sm.screen_names:
            # change all label with unique id
            for key, value in dict(sm.get_screen(screen_name).ids).items():
                if isinstance(value, Label):
                    exec(f"sm.get_screen('{screen_name}').ids.{key}.color = (1,1,1)")
            # change all background color
            for key, value in sm.get_screen(screen_name).ids.items():
                if isinstance(value, FloatLayout):
                    for children in value.canvas.before.children:
                        if isinstance(children, Color):
                            children.rgb = (0.2, 0.2, 0.2)
            # change hangman graw color
            if screen_name == 'game':
                sm.get_screen(screen_name).hangman_draw_color = (1, 1, 1)

    def change_to_light_mode(self):
        """
        Funtion changing theme into light mode.

        :return: None
        """
        # change all label with unique id
        for screen_name in sm.screen_names:
            for key, value in dict(sm.get_screen(screen_name).ids).items():
                if isinstance(value, Label):
                    exec(f"sm.get_screen('{screen_name}').ids.{key}.color = (0,0,0)")
            # change all background color
            for key, value in sm.get_screen(screen_name).ids.items():
                if isinstance(value, FloatLayout):
                    for children in value.canvas.before.children:
                        if isinstance(children, Color):
                            children.rgb = (0.89, 0.882, 0.5)
            # change hangman graw color
            if screen_name == 'game':
                sm.get_screen(screen_name).hangman_draw_color = (0, 0, 0)


# class for managing screens
class WindowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file('window_manager_hangman.kv')

# sentences
subjects = ["I", "You", "He", "She", "They", "We"]
adverbs = ["now", "today", "always", "never", "occasionally", "probably"]
verbs = ["love", "hate", "like", "enjoy", "dislike"]
objects = ["apples", "bananas", "cats", "dogs", "music", "movies"]


def generate_random_sentence():
    """
    Function for generating random sentence.
    It is possible to generate 6*6*5*6 unique sentence.

    :return: None
    """
    subject = random.choice(subjects)
    adverb = random.choice(adverbs)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    return f"{subject} {adverb} {verb} {obj}"


sm = WindowManager()


# adding screens
sm.add_widget(MenuWindow(name='menu'))
sm.add_widget(GameWindow(name='game'))
sm.add_widget(OptionsWindow(name='options'))


class Main(App):
    def build(self):
        return sm


if __name__ == "__main__":

    # Window.size = (1080, 2400)  # TODO REMOVE if finished
    Window.fullscreen = 'auto'
    Main().run()
