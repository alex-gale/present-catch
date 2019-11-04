import arcade
from classes.scene import Scene
from classes.buttons import ChangeGameStateButton

class GameMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/mountain.jpg")

        # initial alpha and scale for buttons
        self.INITIAL_BUTTON_ALPHA = 180
        self.INITIAL_BUTTON_SCALE = 0.975

        # initialise each button and add to button_list
        self.pcatch_button = ChangeGameStateButton(self.game, "PRESENT_CATCH", "images/game_menu/present_catch_button.jpg", 160, 250, self.INITIAL_BUTTON_SCALE)
        self.button_list.append(self.pcatch_button)

        self.psnap_button = ChangeGameStateButton(self.game, "PRESENT_SNAP", "images/game_menu/present_snap_button.jpg", 400, 250, self.INITIAL_BUTTON_SCALE)
        self.button_list.append(self.psnap_button)

        self.psnap_button = ChangeGameStateButton(self.game, "PRESENT_MATCH", "images/game_menu/present_match_button.jpg", 640, 250, self.INITIAL_BUTTON_SCALE)
        self.button_list.append(self.psnap_button)

    def setup(self):
        for button in self.button_list:
            button.alpha = self.INITIAL_BUTTON_ALPHA
            button.scale = self.INITIAL_BUTTON_SCALE

    def draw(self):      
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)
        
        # draw title text
        arcade.draw_text("Select a Game", self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, "#ffa51e", 60, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        # draw all the buttons
        for button in self.button_list:
            button.draw()

    def update(self, delta_time):
        for button in self.button_list:
            # detect if the button is moused over
            mouse_on = True
            if self.game.mouse_x > button.center_x + button.width / 2:
                mouse_on = False
            elif self.game.mouse_x < button.center_x - button.width / 2:
                mouse_on = False
            elif self.game.mouse_y > button.center_y + button.height / 2:
                mouse_on = False
            elif self.game.mouse_y < button.center_y - button.height / 2:
                mouse_on = False

            # scale and change alpha depending on mouseover state
            if mouse_on:
                if button.alpha + 5 <= 255:
                    button.alpha += 5
                    # add the appropriate difference in scale
                    button.scale += (1 - self.INITIAL_BUTTON_SCALE) / ((255 - self.INITIAL_BUTTON_ALPHA) / 5)
                else:
                    button.alpha = 255
                    button.scale = 1
            else:
                if button.alpha - 5 >= self.INITIAL_BUTTON_ALPHA:
                    button.alpha -= 5
                    # subtract the appropriate difference in scale
                    button.scale -= (1 - self.INITIAL_BUTTON_SCALE) / ((255 - self.INITIAL_BUTTON_ALPHA) / 5)
                else:
                    button.alpha = self.INITIAL_BUTTON_ALPHA
                    button.scale = self.INITIAL_BUTTON_SCALE

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the title screen if escape is pressed
            self.game.change_game_state("TITLE_SCREEN")
