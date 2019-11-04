import arcade
from classes.scene import Scene
from classes.game_select_button import GameSelectButton

class GameMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/mountain.jpg")

        # initialise each button and add to button_list
        self.pcatch_button = GameSelectButton(self.game, "PRESENT_CATCH", 60, 450, "images/present_catch.jpg", "Present Catch", "The original Christmas classic reimagined. Save Christmas by catching the presents being thrown out of a helicopter!")
        self.button_list.append(self.pcatch_button)

        self.psnap_button = GameSelectButton(self.game, "PRESENT_SNAP", 300, 450, title_text="Present Snap", desc_text="Coming soon")
        self.button_list.append(self.psnap_button)

        self.pmatch_button = GameSelectButton(self.game, "PRESENT_MATCH", 540, 450, title_text="Present Match", desc_text="Coming soon")
        self.button_list.append(self.pmatch_button)

    def setup(self):
        for button in self.button_list:
            button.alpha = button.INITIAL_ALPHA

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
            mouse_on = True
            if self.game.mouse_x > button.center_x + button.width / 2:
                mouse_on = False
            elif self.game.mouse_x < button.center_x - button.width / 2:
                mouse_on = False
            elif self.game.mouse_y > button.center_y + button.height / 2:
                mouse_on = False
            elif self.game.mouse_y < button.center_y - button.height / 2:
                mouse_on = False

            if mouse_on:
                if button.alpha + 5 < 255:
                    button.change_alpha(5)
                else:
                    button.alpha = 255
            else:
                if button.alpha - 5 > 180:
                    button.change_alpha(-5)
                else:
                    button.alpha = 180

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the title screen if escape is pressed
            self.game.change_game_state("TITLE_SCREEN")
