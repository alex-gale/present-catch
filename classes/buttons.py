import arcade, sys

class ImageButton(arcade.Sprite):
    # plain old image button
    def __init__(self, filename=None, x=0, y=0, scale=1):
        ## initialise parent class (sprite)
        super().__init__(filename, center_x=x, center_y=y, scale=scale)

        self.pressed = False

    def on_press(self):
        # runs when button pressed
        self.pressed = True

    def on_release(self):
        # runs when mouse released over button
        self.pressed = False


class ChangeGameStateButton(ImageButton):
    # button to change the game state. requires access to the game class
    def __init__(self, game, gamestate, filename=None, x=0, y=0, scale=1):
        super().__init__(filename, x, y, scale)

        self.game = game
        self.gamestate = gamestate

    def on_release(self):
        self.pressed = False
        self.game.change_game_state(self.gamestate)


class ExitButton(ImageButton):
    # button to exit the game
    def __init__(self, filename=None, x=0, y=0, scale=1):
        super().__init__(filename, x, y, scale)

    def on_release(self):
        sys.exit()

