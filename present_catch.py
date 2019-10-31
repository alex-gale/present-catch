import arcade
import random
import enum
import math
import textwrap
from classes.scene import Scene

RIGHT_FACING = 0
LEFT_FACING = 1
DANCING = 2

def load_texture_pair(filename):
    # load two sprites facing either direction
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class PresentCatchGameState(enum.Enum):
    WAITING = 0
    COUNTDOWN = 1
    PLAYING = 2
    GAME_OVER = 3

class PresentCatch(Scene):
    def __init__(self, game):
        self.PRESENT_FREQUENCY = 2
        self.PRESENTS_TO_DROP = 25

        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/present_catch/background.jpg")

        # currently pressed keys
        self.pressed_keys = []

        # initialise game state variable
        self.game_state = None

        # format info text
        wrapper = textwrap.TextWrapper(width=66)
        self.intro_text_lines = wrapper.wrap("The elves are drunk again and are throwing all the presents out of a helicopter. Help Santa catch them all so they don't break.")

    def setup(self):
        # initialise game state
        self.game_state = PresentCatchGameState.WAITING

        # initialise countdown timer
        self.countdown = 3

        # initialise game scores
        self.present_count = 0
        self.presents_fallen = 0
        self.score = 0

        # setup player
        self.player = Player()
        self.player.center_x = 400
        self.player.center_y = 192

        # initialise empty array for presents
        self.present_list = arcade.SpriteList()

        # initialise present time counter
        self.time_since_present = self.PRESENT_FREQUENCY

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

        # initialise score counter array
        self.score_icon_list = arcade.SpriteList()

        # generate the right number of score indicators
        for x in range(0, 750, 750 // self.PRESENTS_TO_DROP):
            score_icon = arcade.Sprite("images/present_catch/score_present_blank.png", 0.9)
            score_icon.center_x = x + 40.5
            score_icon.center_y = 30
            score_icon.alpha = 150
            self.score_icon_list.append(score_icon)

    def start_game(self):
        # hide the info box when space is pressed and begin the game
        self.game_state = PresentCatchGameState.COUNTDOWN

    def exit_game(self):
        # return to the game menu
        self.game.change_game_state("GAME_MENU")

    def summon_present(self):
        # creates a present at a random x coord to fall from the sky
        present = Present()
        present.center_x = random.randint(0 + present.width / 2, 800 - present.width / 2)
        present.center_y = 600 + present.height / 2
        present.id = self.present_count
        self.present_list.append(present)

    def draw(self):
        # draw background
        arcade.draw_texture_rectangle(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.background)

        # draw ground tiles
        self.ground_list.draw()

        # draw score list
        self.score_icon_list.draw()

        # draw the presents
        self.present_list.draw()

        # draw the player
        self.player.draw()

        # show the countdown if in the countdown game state
        if self.game_state == PresentCatchGameState.COUNTDOWN:
            arcade.draw_text(str(math.ceil(self.countdown)), self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.5, arcade.color.WHITE, 60, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")


        # show the game info if in the waiting state
        if self.game_state == PresentCatchGameState.WAITING:
            arcade.draw_rectangle_filled(self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, 600, 150, (184, 184, 184))
            arcade.draw_rectangle_outline(self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, 600, 150, (140, 140, 140), 4)

            arcade.draw_text("Present Catch", self.game.SCREEN_WIDTH * 0.5, 510, arcade.color.BLACK, 25, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

            # draw intro text line by line
            line_offset = 0
            for line in self.intro_text_lines:
                arcade.draw_text(line, self.game.SCREEN_WIDTH * 0.5, 485 - line_offset, arcade.color.BLACK, 15, anchor_x="center", font_name="fonts/OpenSans-Regular.ttf")
                line_offset += 17

            arcade.draw_text("Press SPACE to start", self.game.SCREEN_WIDTH * 0.5, 421, (50, 50, 50), 14, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        
        # show win message is game is over
        if self.game_state == PresentCatchGameState.GAME_OVER:
            arcade.draw_rectangle_filled(self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, 600, 150, (184, 184, 184))
            arcade.draw_rectangle_outline(self.game.SCREEN_WIDTH * 0.5, self.game.SCREEN_HEIGHT * 0.8, 600, 150, (140, 140, 140), 4)

            arcade.draw_text("Congratulations", self.game.SCREEN_WIDTH * 0.5, 510, arcade.color.BLACK, 25, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")
            arcade.draw_text("You saved Christmas.", self.game.SCREEN_WIDTH * 0.5, 485, arcade.color.BLACK, 15, anchor_x="center", font_name="fonts/OpenSans-Regular.ttf")
            arcade.draw_text("Score: {}".format(self.score), self.game.SCREEN_WIDTH * 0.5, 455, arcade.color.BLACK, 15, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

            arcade.draw_text("Press ESCAPE to quit", self.game.SCREEN_WIDTH * 0.5, 421, (50, 50, 50), 14, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

        # draw the little score counter above the counter icons
        arcade.draw_text(str(self.score), self.game.SCREEN_WIDTH * 0.5, 50, arcade.color.WHITE, 17, anchor_x="center", font_name="fonts/Courgette-Regular.ttf")

    def update(self, delta_time):
        # countdown state
        if self.game_state == PresentCatchGameState.COUNTDOWN:
            self.countdown -= delta_time
            if self.countdown <= 0:
                self.game_state = PresentCatchGameState.PLAYING


        if self.game_state == PresentCatchGameState.COUNTDOWN or self.game_state == PresentCatchGameState.PLAYING:
            # move if keys are being pressed and state is countdown or playing
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


        if self.game_state == PresentCatchGameState.PLAYING:
            # only run collision checks and summon presents if in playing state
            # check for present collisions with player
            player_present_hit_list = arcade.check_for_collision_with_list(self.player, self.present_list)
            for present in player_present_hit_list:
                # light up the score indicator with the correct texture
                self.score_icon_list[present.id].texture = arcade.load_texture(present.texture_string, scale=0.45)
                self.score_icon_list[present.id].alpha = 200

                # remove the present and increment score
                present.remove_from_sprite_lists()
                self.presents_fallen += 1
                self.score += 1

            # check for presents hitting the ground
            for present in self.present_list:
                if present.center_y - present.height / 2 <= 128:
                    # remove present if it hits the ground
                    present.remove_from_sprite_lists()
                    self.presents_fallen += 1

            # summon a present every self.PRESENT_FREQUENCY seconds
            self.time_since_present += delta_time
            if self.time_since_present >= self.PRESENT_FREQUENCY and self.present_count < self.PRESENTS_TO_DROP:
                self.summon_present()
                self.present_count += 1
                self.time_since_present = 0


        # if all the presents have been caught, the game is over
        if self.presents_fallen == self.PRESENTS_TO_DROP:
            self.game_state = PresentCatchGameState.GAME_OVER


        if self.game_state == PresentCatchGameState.GAME_OVER:
            self.player.change_x = 0
            self.present_list = arcade.SpriteList()
            self.player.action = DANCING


        # update the player and their animation state
        self.player.update()
        self.player.update_animation(delta_time)

        # update the presents
        self.present_list.update()


    def key_press(self, key, modifiers):
        # add key to list of pressed keys
        if key == arcade.key.RIGHT or key == arcade.key.LEFT or key == arcade.key.SPACE:
            self.pressed_keys.append(key)

    def key_release(self, key, modifiers):
        # remove key from list of pressed keys
        while key in self.pressed_keys: self.pressed_keys.remove(key)

        if key == arcade.key.SPACE and self.game_state == PresentCatchGameState.WAITING:
            self.start_game()

        if key == arcade.key.ESCAPE:
            self.exit_game()


# Player class
class Player(arcade.Sprite):
    def __init__(self):
        self.MOVEMENT_SPEED = 4.7

        super().__init__()

        # set initial direction
        self.action = RIGHT_FACING

        # load all santa sprites
        # right and left for idle
        self.idle_textures = load_texture_pair("images/present_catch/santa_idle.png")

        # get running textures from sprite map
        self.animated_textures = [
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
            ]),
            arcade.load_textures("images/present_catch/santa_dancing.png", [
                # dancing
                [0, 0, 128, 128],
                [128, 0, 128, 128],
                [256, 0, 128, 128],
                [384, 0, 128, 128],
                [512, 0, 128, 128],
                [640, 0, 128, 128],
                [768, 0, 128, 128],
                [896, 0, 128, 128]
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
        if self.change_x < 0 and self.action == RIGHT_FACING:
            self.action = LEFT_FACING
        elif self.change_x > 0 and self.action == LEFT_FACING:
            self.action = RIGHT_FACING

        # idle texture
        if self.change_x == 0 and self.action != DANCING:
            self.current_texture = 0
            self.texture = self.idle_textures[self.action]
            return
        
        # walking animation
        self.current_texture += 1
        if self.current_texture >= (len(self.animated_textures[self.action])) * self.updates_per_frame:
            self.current_texture = 0
        self.texture = self.animated_textures[self.action][self.current_texture // self.updates_per_frame]


# Present Class
class Present(arcade.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(filename=None, center_x=x, center_y=y)

        # all present textures with weight to be chosen
        self.present_textures = [
            ["images/present_catch/present_1.png", 0.198],
            ["images/present_catch/present_2.png", 0.198],
            ["images/present_catch/present_3.png", 0.198],
            ["images/present_catch/present_4.png", 0.198],
            ["images/present_catch/present_5.png", 0.198],
            ["images/present_catch/present_6.png", 0.01]
        ]

        # weighted choice
        self.texture_string = random.choices(population=[i[0] for i in self.present_textures], weights=[j[1] for j in self.present_textures], k=1)[0]

        # load the texture
        self.texture = arcade.load_texture(self.texture_string)

        # falling velocity
        self.change_y = -2.5

        # numberical id
        self.id = None
