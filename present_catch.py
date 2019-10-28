import arcade, random
from classes.scene import Scene

class PresentCatch(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/present_catch/background.jpg")

        # initialise present score
        self.present_count = 25

    def setup(self):
        self.score = 0

        # initialise empty array for ground tiles
        self.ground_list = arcade.SpriteList()

        # random ground tiles
        # ground level tiles
        for x in range(0, 800, 64):
            tile_id = random.randint(0, 1)
            ground = arcade.Sprite("images/present_catch/ground_{}.jpg".format(tile_id))
            ground.center_x = x
            ground.center_y = 96
            self.ground_list.append(ground)

        # underground tiles
        for x in range(0, 800, 64):
            tile_id = random.randint(2, 3)
            ground = arcade.Sprite("images/present_catch/ground_{}.jpg".format(tile_id))
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)

    def draw(self):
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)

        # draw ground tiles
        self.ground_list.draw()
