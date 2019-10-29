import arcade, random
from classes.scene import Scene
from classes.shapes import BorderRadiusRectangle

class PresentSnap(Scene):
    def __init__(self, game):
        super().__init__(game)

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
        # names of images in order
        self.images_names = ["Santa Claus", "Candy Cane", "Present", "Stocking", "Christmas Tree", "Holly Leaves", "Christmas Wreath", "Gingerbread Man", "Christmas Candles", "Baubles", "Christmas Pudding", "Snow Globe", "Christmas Robin"]

        # initialise the deck in form [name, image]
        self.deck = [[self.images_names[i], self.images[i]] for i in range(13)] * 4

        # the shapes that create the deck the player has
        self.player_pile = BorderRadiusRectangle(102, 127, 125, 175, (240,240,240), 5)
        self.player_separator = BorderRadiusRectangle(47, 127, 11, 175, (25,25,25), 5)
        self.player_decorator_card = Card(self, 105, 127, 125, 175, colour=(240,240,240))

        # self.test_card = Card(self, 330, 300, 125, 175, colour=(240, 240, 240), face="back", image=self.images[0])

    def setup(self):
        self.score = 0

        # runs code to add card to the button list
        self.played_card = True

        # deal the cards
        self.play_pile = []
        random.shuffle(self.deck)
        self.player_hand = self.deck[:26]
        self.computer_hand = self.deck[26:]

    def draw(self):

        # draw player card pile
        self.player_pile.draw()
        self.player_separator.draw()
        self.player_decorator_card.draw()
        self.current_card.draw()

        # draws the last card in the play pile
        if len(self.play_pile) != 0:
            self.play_pile[-1].draw()

    def update(self, delta_time):
        # when a card is played, the next card becomes the current card and becomes pressable
        if self.played_card:
            self.played_card = False
            self.current_card = Card(self, 105, 127, 125, 175, image=self.player_hand[0], colour=(240,240,240), face="back")
            self.button_list.append(self.current_card)

    def play_card(self, card):
        # moves the card to the play pile
        card.update_position(330, 300)
        self.play_pile.append(self.current_card)

        # updates the card to turn it and show the face
        card.face = "face"

        # remove the played card from the players hand and stops it being pressable
        self.player_hand.pop(0)
        self.button_list.remove(self.current_card)

        # updates the current card again
        self.played_card = True


class Card:
    def __init__(self, present_snap, x=0, y=0, width=125, height=175, image=['', None], face="back", colour=(0,0,0)):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

        # card [name, image]
        self.image = image

        self.present_snap = present_snap
        self.face = face
        self.played = False

        # initialise the card border
        self.card_background = BorderRadiusRectangle(self.center_x, self.center_y, width, height, colour, border_rad=5)
        self.card_back = arcade.load_texture("images/card_back.png")

    def draw(self):
        # render the card
        self.card_background.draw()
        # render either face or back, depending on side visible
        if self.face == "back":
            arcade.draw_texture_rectangle(self.center_x, self.center_y, 110, 160, self.card_back)
        elif self.face == "face":
            arcade.draw_rectangle_outline(self.center_x, self.center_y, 110, 160, (220,32,32))
            arcade.draw_texture_rectangle(self.center_x, self.center_y - 24, 100, 100, self.image[1])

    def update_position(self, x, y):
        # update the position of the card
        self.center_x = x
        self.center_y = y
        self.card_background.update_position(self.center_x, self.center_y)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        # plays the card
        self.present_snap.play_card(self)
