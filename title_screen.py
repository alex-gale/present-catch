import arcade
from classes.button import ImageButton
from classes.scene import Scene
from effects import fade_in, slide_in

class TitleScreen(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/mountain.jpg")

        # initialise present catch logo
        self.logo = arcade.Sprite("images/logo.png")
        self.logo.alpha = 0
        self.logo.center_x = self.game.SCREEN_WIDTH * 0.5
        self.logo.center_y = self.game.SCREEN_HEIGHT * 0.8

        # initialise santa sprite
        self.santa = arcade.Sprite("images/santa.png")
        self.santa.center_x = 160
        self.santa.center_y = -200

        # initialise buttons
        self.button_list = []

        # main play button
        play_button = ImageButton("images/play_button.png", 550, 300)
        play_button.alpha = 0
        self.button_list.append(play_button)

    def draw(self):
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)

        # fade in the logo
        if self.logo.alpha < 255:
            fade_in(self.logo, 4)
        self.logo.draw()

        # slide in the santa
        if self.santa.center_y < 140:
            slide_in(self.santa, 3, 140)
        self.santa.draw()

        # fade in buttons after logo is shown
        if self.logo.alpha == 255:
            for button in self.button_list:
                if button.alpha < 255:
                    fade_in(button, 4)
                button.draw()
