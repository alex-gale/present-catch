import arcade
from classes.scene import Scene

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

        # set image is one is provided, otherwise grey square
        if filename != None:
            self.image = arcade.load_texture(filename)
            self.image.alpha = self.alpha
        else:
            self.image = arcade.create_rectangle_filled(self.x + (self.width / 2), self.y - 75, 200, 150, [100, 100, 100, self.alpha])

        # create other shapes
        self.border_line = arcade.create_line(self.x, self.y - 152, self.x + (self.width), self.y - 152, [140, 140, 140, self.alpha], line_width=4)
        self.text_rectangle = arcade.create_rectangle_filled(self.x + (self.width / 2), self.y - 277, 200, 246, [184, 184, 184, self.alpha])
        self.button_border = arcade.create_rectangle_outline(self.center_x, self.center_y, self.width - 4, self.height - 4, [140, 140, 140, self.alpha], 4)

        # initialise text values
        self.title_text = title_text
        self.desc_test = desc_text

        self.pressed = False

    def draw(self):
        # draw the button
        self.image.draw()
        self.border_line.draw()
        self.text_rectangle.draw()
        self.button_border.draw()

        # draw text
        arcade.draw_text(self.title_text, self.x + 10, self.y - 180, arcade.color.BLACK, 20, font_name="fonts/Courgette-Regular.ttf")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        self.game.change_game_state(self.gamestate)


class GameMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/mountain.jpg")

        # initialise each button and add to button_list
        self.pcatch_button = GameSelectButton(self.game, "PRESENT_CATCH", 60, 450, title_text="Present Catch")
        self.button_list.append(self.pcatch_button)

        self.psnap_button = GameSelectButton(self.game, "PRESENT_SNAP", 300, 450, title_text="Present Snap")
        self.button_list.append(self.psnap_button)

        self.pmatch_button = GameSelectButton(self.game, "PRESENT_MATCH", 540, 450, title_text="Present Match")
        self.button_list.append(self.pmatch_button)

    def draw(self):      
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)
        
        # draw title text
        arcade.draw_text("Select a Game", self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, "#ffa51e", 60, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        # draw all the buttons
        for button in self.button_list:
            button.draw()