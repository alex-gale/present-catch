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

    def draw(self):      
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)
        
        # draw title text
        arcade.draw_text("Select a Game", self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, "#ffa51e", 60, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        # draw all the buttons
        for button in self.button_list:
            button.draw()

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the title screen if escape is pressed
            self.game.change_game_state("TITLE_SCREEN")
