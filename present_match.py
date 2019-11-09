import arcade, random
from classes.scene import Scene

class PresentMatch(Scene):
    def __init__(self, game):
        super().__init__(game)

        # conveyor belt data storage
        self.conveyor_belts = [
            {"items": arcade.SpriteList(), "sprites": arcade.SpriteList(), "speed": None, "direction": 1},
            {"items": arcade.SpriteList(), "sprites": arcade.SpriteList(), "speed": None, "direction": -1},
            {"items": arcade.SpriteList(), "sprites": arcade.SpriteList(), "speed": None, "direction": 1}
        ]

        # insert sprites for conveyor belts
        for x in range(0, 800, 96):
            conveyor = ConveyorBelt()
            conveyor.center_x = x
            conveyor.center_y = 490
            self.conveyor_belts[0]["sprites"].append(conveyor)

        for x in range(0, 800, 96):
            conveyor = ConveyorBelt(mirrored=True)
            conveyor.center_x = x
            conveyor.center_y = 350
            self.conveyor_belts[1]["sprites"].append(conveyor)

        for x in range(0, 800, 96):
            conveyor = ConveyorBelt()
            conveyor.center_x = x
            conveyor.center_y = 210
            self.conveyor_belts[2]["sprites"].append(conveyor)

        # initialise list of items
        self.item_list = {"robin": "images/present_match/robin.png"}

    def setup(self):
        # reset items and randomise belt speeds
        for belt in self.conveyor_belts:
            belt["items"] = arcade.SpriteList()
            belt["speed"] = random.randint(2, 3)

            for sprite in belt["sprites"]:
                sprite.FRAMES_PER_UPDATE = belt["speed"]

        self.add_item_to_conveyor(0)

    def add_item_to_conveyor(self, conveyor_id):
        # get the conveyor and its top y value
        conveyor = self.conveyor_belts[conveyor_id]
        conveyor_top_y = conveyor["sprites"][0].center_y + 16

        # choose a random item from the choices
        item_name, item_image = random.choice(list(self.item_list.items()))

        # setup the item's x and y
        item = ConveyorItem(item_image)
        item.center_y = conveyor_top_y + (item.height / 2)
        # choose starting side based on conveyor direction
        item.center_x = -32 if conveyor["direction"] == 1 else 832

        # add the item to the relevant conveyor belt
        self.conveyor_belts[conveyor_id]["items"].append(item)

    def draw(self):
        # draw all the conveyor belts and their items
        for belt in self.conveyor_belts:
            belt["items"].draw()
            belt["sprites"].draw()

    def update(self, delta_time):
        # update item positions and animation state in each belt
        for belt in self.conveyor_belts:
            for item in belt["items"]:
                # 6 is is the number of pixels moved each frame of conveyor animation
                item.center_x += 6 / belt["speed"] * belt["direction"]

            belt["sprites"].update_animation(delta_time)

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the game menu if escape is pressed
            self.game.change_game_state("GAME_MENU")


class ConveyorBelt(arcade.Sprite):
    def __init__(self, mirrored=False):
        super().__init__()

        # load tilesheet of animations for conveyor
        self.animated_textures = arcade.load_textures("images/present_match/conveyor.png", [
            [0, 0, 96,  33],
            [96, 0, 96, 33],
            [192, 0, 96, 33],
            [288, 0, 96, 33]
        ], mirrored=mirrored)

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

class ConveyorItem(arcade.Sprite):
    def __init__(self, filename=None):
        super().__init__(filename)
