import arcade
import random
from classes.scene import Scene

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    # load two sprites facing either direction
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class PresentCatch(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/present_catch/background.jpg")

        # currently pressed keys
        self.pressed_keys = []

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

        # initialise empty array for presents
        self.present_list = arcade.SpriteList()

        self.summon_present()

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

    def summon_present(self):
        # creates a present at a random x coord to fall from the sky
        present = Present()
        present.center_x = random.randint(0 + present.width / 2, 800 - present.width / 2)
        present.center_y = 600 + present.height / 2
        self.present_list.append(present)

    def draw(self):
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)

        # draw ground tiles
        self.ground_list.draw()

        # draw the presents
        self.present_list.draw()

        # draw the player
        self.player.draw()

    def update(self, delta_time):
        # move if keys are being pressed
        if arcade.key.RIGHT in self.pressed_keys and arcade.key.LEFT in self.pressed_keys:
            # if both keys are pressed, do the one that was pressed last
            if self.pressed_keys.index(arcade.key.RIGHT) > self.pressed_keys.index(arcade.key.LEFT) and self.player.center_x < self.game.SCREEN_WIDTH:
                self.player.change_x = self.player.MOVEMENT_SPEED
            elif self.player.center_x > 0:
                self.player.change_x = -self.player.MOVEMENT_SPEED
            else:
                self.player.change_x = 0

        elif arcade.key.RIGHT in self.pressed_keys and self.player.center_x < self.game.SCREEN_WIDTH:
            # just right key
            self.player.change_x = self.player.MOVEMENT_SPEED

        elif arcade.key.LEFT in self.pressed_keys and self.player.center_x > 0:
            # just left key
            self.player.change_x = -self.player.MOVEMENT_SPEED

        else:
            self.player.change_x = 0

        # check for present collisions with player
        player_present_hit_list = arcade.check_for_collision_with_list(self.player, self.present_list)
        for present in player_present_hit_list:
            present.remove_from_sprite_lists()
            self.score += 1

        # check for presents hitting the ground
        for present in self.present_list:
            if present.center_y - present.height / 2 <= 128:
                present.remove_from_sprite_lists()

        # update the player and their animation state
        self.player.update()
        self.player.update_animation(delta_time)

        # update the presents
        self.present_list.update()

    def key_press(self, key, modifiers):
        # add key to list of pressed keys
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.pressed_keys.append(key)

    def key_release(self, key, modifiers):
        # remove key from list of pressed keys
        while key in self.pressed_keys: self.pressed_keys.remove(key)


# Player class
class Player(arcade.Sprite):
    def __init__(self):
        self.MOVEMENT_SPEED = 3

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

        # hitbox
        self.points = [[-40, 64], [40, 64], [40, -64], [-40, -64]]

    def update_animation(self, delta_time):
        # determine direction to be facing
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

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


# Present Class
class Present(arcade.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(filename=None, center_x=x, center_y=y)

        # all present textures
        self.present_textures = [
            "images/present_catch/present_1.png"
        ]

        # load a random present texture
        self.texture = arcade.load_texture(random.choice(self.present_textures))

        self.change_y = -2.5
