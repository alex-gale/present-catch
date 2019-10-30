import arcade, random
from classes.scene import Scene

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    # load two sprites facing either direction
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # set initial direction
        self.facing_direction = RIGHT_FACING

        # load all santa sprites
        # right and left for idle
        self.idle_textures = load_texture_pair("images/present_catch/santa_idle.png")

        # get running textures from sprite map
        self.running_textures = [
            arcade.load_textures("images/present_catch/santa_running.png", [
                # moving right
                [0, 0, 128, 128],
                [128, 0, 128, 128],
                [256, 0, 128, 128],
                [384, 0, 128, 128]
            ]),
            arcade.load_textures("images/present_catch/santa_running.png", [
                # moving left
                [0, 128, 128, 128],
                [128, 128, 128, 128],
                [256, 128, 128, 128],
                [384, 128, 128, 128]
            ])
        ]

        # animation updates per frame
        self.updates_per_frame = 10

        # current texture in animation
        self.current_texture = 0

    def update_animation(self, delta_time):
        # determine direction to be facing
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = LEFT_FACING

        # idle texture
        if self.change_x == 0:
            self.current_texture = 0
            self.texture = self.idle_textures[self.facing_direction]
            return
        
        # walking animation
        self.current_texture += 1
        if self.current_texture >= 4 * self.updates_per_frame:
            self.current_texture = 0
        self.texture = self.running_textures[self.facing_direction][self.current_texture // self.updates_per_frame]


class PresentCatch(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/present_catch/background.jpg")

        # initialise player variable
        self.player = None

    def setup(self):
        # initialise game scores
        self.present_count = 25
        self.score = 0

        # setup player
        self.player = Player()
        self.player.center_x = 400
        self.player.center_y = 192

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

        # draw the player
        self.player.draw()

    def update(self, delta_time):
        # update the player and their animation
        self.player.update()
        self.player.update_animation(delta_time)
