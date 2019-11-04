import arcade, enum
from effects import fade_in, slide_in
from classes.buttons import ImageButton
from title_screen import TitleScreen
from game_menu import GameMenu
from present_catch import PresentCatch
from present_snap import PresentSnap
from present_match import PresentMatch

# store game state constants in Enum
class GameState(enum.Enum):
    TITLE_SCREEN = 0
    GAME_MENU = 1
    PRESENT_CATCH = 2
    PRESENT_SNAP = 3
    PRESENT_MATCH = 4

def check_mouse_press_for_buttons(x, y, button_list):
    # checks if mouse is over button when clicked
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue

        button.on_press()

def check_mouse_release_for_buttons(_x, _y, button_list):
    # checks if mouse is over button when released
    for button in button_list:
        if button.pressed:
            button.on_release()


class Game(arcade.Window):
    def __init__(self):
        ## initialise application
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN_TITLE = "Present Catch"

        # call the init of arcade.Window
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)

        # initialise game state to the title screen
        self.current_state = GameState.TITLE_SCREEN

        # initialise scenes
        self.scenes = []

        # initialise mouse positions
        self.mouse_x = 0
        self.mouse_y = 0

    def setup(self):
        ## setup scenes
        # 0 = title screen
        title_screen = TitleScreen(self)
        self.scenes.append(title_screen)

        # 1 = game menu
        game_menu = GameMenu(self)
        self.scenes.append(game_menu)

        # 2 = present catch
        present_catch = PresentCatch(self)
        self.scenes.append(present_catch)

        # 3 = present snap
        present_snap = PresentSnap(self)
        self.scenes.append(present_snap)

        # 4 = present match
        present_match = PresentMatch(self)
        self.scenes.append(present_match)

        # setup initial scene
        self.setup_current_scene()


    def get_current_state_value(self):
        # return the integer value of the current state
        return self.current_state.value

    def setup_current_scene(self):
        # setup the currently loaded scene
        state_value = self.get_current_state_value()
        self.scenes[state_value].setup()

    def change_game_state(self, new_state):
        # get the old scene's state_value
        old_state_value = self.get_current_state_value()

        # switch the state
        self.current_state = GameState[new_state]

        # setup the scene
        self.setup_current_scene()

        # run the unload method for the old scene
        self.scenes[old_state_value].unload()


    def on_draw(self):
        ## main game renderer
        arcade.start_render()

        # run the draw method for the current scene
        state_value = self.get_current_state_value()
        self.scenes[state_value].draw()

    def on_update(self, delta_time):
        ## run updates to scenes
        state_value = self.get_current_state_value()
        self.scenes[state_value].update(delta_time)

    def on_key_press(self, key, modifiers):
        ## send key presses to scenes
        state_value = self.get_current_state_value()
        self.scenes[state_value].key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        ## send key releases to scenes
        state_value = self.get_current_state_value()
        self.scenes[state_value].key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, key_modifiers):
        ## check for mouse presses
        state_value = self.get_current_state_value()
        check_mouse_press_for_buttons(x, y, self.scenes[state_value].button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        ## check for mouse releases
        state_value = self.get_current_state_value()
        check_mouse_release_for_buttons(x, y, self.scenes[state_value].button_list)

    def on_mouse_motion(self, x, y, dx, dy):
        ## check for mouse movement
        self.mouse_x = x
        self.mouse_y = y

        # send mouse positions to loaded scene
        state_value = self.get_current_state_value()
        self.scenes[state_value].mouse_movement(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        ## check for mouse click and drag
        state_value = self.get_current_state_value()
        self.scenes[state_value].mouse_drag(x, y, dx, dy, buttons, modifiers)

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
