import arcade
from classes.scene import Scene

#def draw_game_selector()

class GameMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/mountain.jpg")

    def draw(self):      
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)
        
        arcade.draw_text("Select a Game", self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, "#ffa51e", 60, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        # top corner is at x=60, y=450
        arcade.draw_rectangle_filled(160, 250, 200, 400, [184, 184, 184])
        arcade.draw_line(60, 298, 260, 298, [140, 140, 140], line_width=4)
        arcade.draw_rectangle_filled(160, 375, 200, 150, [100, 100, 100])

        arcade.draw_rectangle_filled(400, 250, 200, 400, [184, 184, 184])

        arcade.draw_rectangle_filled(640, 250, 200, 400, [184, 184, 184])