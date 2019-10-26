import arcade

class ImageButton(arcade.Sprite):
    # plain old image button
    def __init__(self, filename=None, x=0, y=0):
        ## initialise parent class (sprite)
        super().__init__(filename, center_x=x, center_y=y)

        self.pressed = False

    def on_press(self):
        # runs when button pressed
        self.pressed = True

    def on_release(self):
        # runs when mouse released over button
        self.pressed = False


class ChangeGameStateButton(ImageButton):
    # button to change the game state. requires access to the game class
    def __init__(self, gamestate, game, filename=None, x=0, y=0):
        super().__init__(filename, x, y)

        self.gamestate = gamestate
        self.game = game

    def on_release(self):
        self.pressed = False
        self.game.change_game_state(self.gamestate)