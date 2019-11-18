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
        self.add_item_to_conveyor(1)

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
        # add the item to button list for click detection
        self.button_list.append(item)

    def remove_item(self, item):
        # remove the item from the game
        item.remove_from_sprite_lists()
        self.button_list.remove(item)

    def draw(self):
        # draw all the conveyor belts
        for belt in self.conveyor_belts:
            belt["sprites"].draw()

        # draw all the conveyor items
        for belt in self.conveyor_belts:
            belt["items"].draw()
            print(len(belt["items"]))

    def update(self, delta_time):
        # update items and animation state in each belt
        for belt in self.conveyor_belts:
            for item in belt["items"]:
                # 6 is is the number of pixels moved each frame of conveyor animation
                item.update_x(6 / belt["speed"] * belt["direction"] * item.on_belt)

                # drop item if it has been taken off the belt and released
                if item.on_belt == 0 and not item.pressed:
                    item.change_y -= 9 * delta_time
                    item.center_y += item.change_y

                # remove the item if it is off the screen
                if item.center_y + (item.height / 2) < 0:
                    self.remove_item(item)
                # only remove horizontally if it has travelled the right distance (so it isn't destroyed at the start)
                if item.distance_travelled > 800:
                    if item.center_x - (item.width / 2) > 800 or item.center_x + (item.width / 2) < 0:
                        self.remove_item(item)

            # continue animation of conveyor belt sprite
            belt["sprites"].update_animation(delta_time)

    def key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # return to the game menu if escape is pressed
            self.game.change_game_state("GAME_MENU")

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # detect if item on conveyor belt is being dragged
        for belt in self.conveyor_belts:
            for item in belt["items"]:
                if item.pressed:
                    # remove item from belt and set position to mouse
                    item.on_belt = 0
                    item.center_x = x
                    item.center_y = y

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

        self.pressed = False
        # if the item is on the belt
        self.on_belt = 1
        # the total distance the item has travelled while on the belt
        self.distance_travelled = 0

    def on_press(self):
        self.pressed = True

        # reset y change when clicked
        self.change_y = 0

    def on_release(self):
        self.pressed = False

    def update_x(self, diff):
        # move the sprite and update the distance travelled
        self.center_x += diff
        self.distance_travelled += abs(diff)
