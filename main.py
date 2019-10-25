import arcade, enum
from effects import fade_in, slide_in
from classes.button import ImageButton, check_mouse_press_for_buttons, check_mouse_release_for_buttons
from title_screen import TitleScreen

# store game state constants in Enum
class GameState(enum.Enum):
    TITLE_SCREEN = 0
    GAME_MENU = 1
    PRESENT_CATCH = 2
    PRESENT_SNAP = 3
    PRESENT_MATCH = 4


class Game(arcade.Window):
    def __init__(self):
        ## initialise application
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN_TITLE = "Present Catch"
        self.TITLE_BACKGROUND = "images/mountain.jpg"

        # call the init of arcade.Window
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)

        # initialise game state
        self.current_state = GameState.TITLE_SCREEN

        self.title_screen = TitleScreen(self)

        # button list
        # self.title_screen_button_list = None

    def setup(self):
        pass

    def draw_title_screen(self):
        ## title screen
        # draw the title background
        self.title_screen.draw()


    def on_draw(self):
        ## main game renderer
        arcade.start_render()

        if self.current_state == GameState.TITLE_SCREEN:
            self.draw_title_screen()


    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        ## check for mouse presses
        check_mouse_press_for_buttons(x, y, self.title_screen.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        ## check for mouse releases
        check_mouse_release_for_buttons(x, y, self.title_screen.button_list)

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()