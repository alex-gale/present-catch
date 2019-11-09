import arcade
from classes.scene import Scene

class PresentMatch(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise the conveyor belt sprite positions
        self.conveyor_list = arcade.SpriteList()

        for x in range(0, 800, 128):
            conveyor = ConveyorBelt()
            conveyor.center_x = x
            conveyor.center_y = 400
            self.conveyor_list.append(conveyor)

    def setup(self):
        # initialise the conveyor belt speed for the start of the game (lower is faster)
        self.conveyor_speed = 3
        for c in self.conveyor_list:
            c.FRAMES_PER_UPDATE = self.conveyor_speed

    def draw(self):
        # draw all the conveyor belts
        self.conveyor_list.draw()

    def update(self, delta_time):
        # update animation state of conveyor belts
        self.conveyor_list.update_animation(delta_time)

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the game menu if escape is pressed
            self.game.change_game_state("GAME_MENU")


class ConveyorBelt(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # load tilesheet of animations for conveyor
        self.animated_textures = arcade.load_textures("images/present_match/conveyor.png", [
            [0, 0, 128,  44],
            [128, 0, 128, 44],
            [256, 0, 128, 44],
            [384, 0, 128, 44]
        ])

        # initialise animation speed
        self.FRAMES_PER_UPDATE = 3

        # current frame in animation
        self.current_texture = 0

    def update_animation(self, delta_time):
        # move through frames of animation
        self.current_texture += 1
        if self.current_texture >= len(self.animated_textures) * self.FRAMES_PER_UPDATE:
            self.current_texture = 0

        self.texture = self.animated_textures[self.current_texture // self.FRAMES_PER_UPDATE]
