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

        # initialise scenes
        self.scenes = []

    def setup(self):
        # setup scenes
        title_screen = TitleScreen(self)
        self.scenes.append(title_screen)


    def on_draw(self):
        ## main game renderer
        arcade.start_render()

        state_value = self.current_state.value
        self.scenes[state_value].draw()

    def on_update(self, delta_time):
        state_value = self.current_state.value
        self.scenes[state_value].update(delta_time)

    def on_mouse_press(self, x, y, button, key_modifiers):
        ## check for mouse presses
        state_value = self.current_state.value
        check_mouse_press_for_buttons(x, y, self.scenes[state_value].button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        ## check for mouse releases
        state_value = self.current_state.value
        check_mouse_release_for_buttons(x, y, self.scenes[state_value].button_list)

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()