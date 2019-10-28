import arcade, textwrap

class GameSelectButton:
    # button from to select the game to play
    def __init__(self, game, gamestate, x=0, y=0, filename=None, title_text="", desc_text=""):
        self.height = 400
        self.width = 200

        self.gamestate = gamestate
        self.game = game

        self.x = x
        self.y = y
        # center_x and center_y for click detection in main.py
        self.center_x = self.x + self.width / 2
        self.center_y = self.y - self.height / 2

        self.alpha = 255

        # set image if one is provided, otherwise grey square
        if filename is not None:
            self.image = arcade.Sprite(filename)
            self.image.alpha = self.alpha
            self.image.center_x = self.x + (self.width / 2)
            self.image.center_y = self.y - 75
        else:
            self.image = arcade.create_rectangle_filled(self.x + (self.width / 2), self.y - 75, 200, 150, [100, 100, 100, self.alpha])

        # create other shapes
        self.border_line = arcade.create_line(self.x, self.y - 152, self.x + (self.width), self.y - 152, [140, 140, 140, self.alpha], line_width=4)
        self.text_rectangle = arcade.create_rectangle_filled(self.x + (self.width / 2), self.y - 277, 200, 246, [184, 184, 184, self.alpha])
        self.title_underline = arcade.create_line(self.x + 10, self.y - 185, self.x + (self.width - 10), self.y - 185, [0, 0, 0, self.alpha], line_width=2)
        self.button_border = arcade.create_rectangle_outline(self.center_x, self.center_y, self.width - 4, self.height - 4, [140, 140, 140, self.alpha], 4)

        # initialise text values
        self.title_text = title_text
        self.desc_test = desc_text

        # fit desc_text into the space given with line breaks
        wrapper = textwrap.TextWrapper(width=25)
        self.desc_test_lines = wrapper.fill(self.desc_test)
        print(self.desc_test_lines)

        self.pressed = False

    def draw(self):
        # draw the button
        self.image.draw()
        self.border_line.draw()
        self.text_rectangle.draw()
        self.title_underline.draw()
        self.button_border.draw()

        # draw text
        arcade.draw_text(self.title_text, self.x + 10, self.y - 180, [0, 0, 0, self.alpha], 20, font_name="fonts/Courgette-Regular.ttf")
        arcade.draw_text(self.desc_test_lines, self.x + 10, self.y - 195, [0, 0, 0, self.alpha], 13, anchor_x="left", anchor_y="top")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        self.game.change_game_state(self.gamestate)
