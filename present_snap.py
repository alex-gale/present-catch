import arcade, random
from classes.scene import Scene
from classes.shapes import BorderRadiusRectangle

class PresentSnap(Scene):
    def __init__(self, game):
        super().__init__(game)

        # initialise background
        self.background = arcade.load_texture("images/present_snap_background_2.png")

        # set background colour
        arcade.set_background_color((71, 71, 71))

        # initialise all the images
        self.images = arcade.load_textures("images/present_snap_sprites.png",[
            [0, 0, 128, 128],
            [128, 0, 128, 128],
            [256, 0, 128, 128],
            [384, 0, 128, 128],
            [512, 0, 128, 128],
            [640, 0, 128, 128],
            [768, 0, 128, 128],
            [896, 0, 128, 128],
            [1024, 0, 128, 128],
            [1152, 0, 128, 128],
            [1280, 0, 128, 128],
            [1408, 0, 128, 128],
            [1536, 0, 128, 128]
            ])

        # initialise the deck
        self.deck = [image for image in self.images] * 4

        self.test_card = Card(400, 300, 125, 175, colour=(240, 240, 240), face="face", image=self.images[1])

    def setup(self):
        self.score = 0

        # deal the cards
        random.shuffle(self.deck)
        self.player_hand = self.deck[:26]
        self.computer_hand = self.deck[26:]

    def draw(self):
        self.test_card.draw()


class Card:
    def __init__(self, x=0, y=0, width=125, height=175, image=None, face="back", colour=(255,255,255)):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

        self.image = image
        self.face = face

        # initialise the card border
        self.card_border = BorderRadiusRectangle(self.center_x, self.center_y, width, height, colour, border_rad=5)
        self.card_back = arcade.load_texture("images/card_back.png")

    def draw(self):
        self.card_border.draw()
        if self.face == "back":
            arcade.draw_texture_rectangle(self.center_x, self.center_y, 110, 160, self.card_back)
        elif self.face == "face":
            arcade.draw_rectangle_outline(self.center_x, self.center_y, 110, 160, (0,0,0))
            arcade.draw_texture_rectangle(self.center_x, self.center_y - 24, 100, 100, self.image)

    def update(self):
        self.card_border.update_position(self.center_x, self.center_y)
