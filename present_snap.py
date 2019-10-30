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

        # the shapes that create the player's deck
        self.player_pile = BorderRadiusRectangle(102, 127, 125, 175, (240,240,240), 5)
        self.player_separator = BorderRadiusRectangle(47, 127, 11, 175, (25,25,25), 5)
        self.player_decorator_card = Card(self, 105, 127, 125, 175, colour=(240,240,240))

        # the shapes that create the computer's deck
        self.computer_pile = BorderRadiusRectangle(self.game.SCREEN_WIDTH - 102, self.game.SCREEN_HEIGHT - 127, 125, 175, (240,240,240), 5)
        self.computer_separator = BorderRadiusRectangle(self.game.SCREEN_WIDTH - 47, self.game.SCREEN_HEIGHT - 127, 11, 175, (25,25,25), 5)
        self.computer_decorator_card = Card(self, self.game.SCREEN_WIDTH - 105, self.game.SCREEN_HEIGHT - 127, 125, 175, colour=(240,240,240), flipped=True)

        # initialise box to show the second card
        self.second_card_box = BorderRadiusRectangle(467, 352, 50, 70, colour=(240,240,240), border_rad=5)

    def setup(self):
        self.score = 0

        # runs code to add card to the button list
        self.played_card = True

        self.player_turn = True

        # deal the cards
        self.play_pile = []
        random.shuffle(self.deck)
        self.player_hand = self.deck[:26]
        self.computer_hand = self.deck[26:]

    def draw(self):

        # central line
        # arcade.draw_line(self.game.SCREEN_WIDTH // 2, 0, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT, (255, 0, 0))
        # arcade.draw_line((self.game.SCREEN_WIDTH // 2) + 1, 0, (self.game.SCREEN_WIDTH // 2) + 1, self.game.SCREEN_HEIGHT, (255, 0, 0))

        # draw player card pile
        if len(self.player_hand) > 1:
            self.player_pile.draw()
            self.player_separator.draw()
            self.player_decorator_card.draw()
        if len(self.player_hand) > 0:
            self.current_card.draw()

        # draw computer card pile
        self.computer_pile.draw()
        self.computer_separator.draw()
        self.computer_decorator_card.draw()

        # draws the top card in the play pile
        if len(self.play_pile) != 0:
            self.play_pile[-1][1].draw()

        # displays the second card in the play pile
        if len(self.play_pile) > 1:
            self.second_card_box.draw()
            arcade.draw_rectangle_outline(467, 352, 40, 60, color=(220,32,32))
            arcade.draw_texture_rectangle(467, 343, 40, 40, texture=self.play_pile[-2][1].image[1])

    def update(self, delta_time):
        # when a card is played, the next card becomes the current card and becomes pressable
        if self.played_card:
            if len(self.player_hand) > 0 and self.player_turn:
                self.played_card = False
                self.current_card = Card(self, 105, 127, 125, 175, image=self.player_hand[0], colour=(240,240,240), face="back")
                self.button_list.append(self.current_card)

    def play_card(self, card):
        # moves the card to the play pile
        card.update_position(365, 300)
        self.play_pile.append([self.player_hand[0], self.current_card])

        # updates the card to turn it and show the face
        card.face = "face"

        # remove the played card from the players hand and stops it being pressable
        self.player_hand.pop(0)
        self.button_list.remove(self.current_card)

        # updates the current card again
        self.played_card = True


class Card:
    def __init__(self, present_snap, x=0, y=0, width=125, height=175, image=['', None], colour=(0,0,0), alpha=255, face="back", flipped=False):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

        self.colour = colour
        self.alpha = alpha

        # card [name, image]
        self.image = image

        self.present_snap = present_snap
        self.face = face
        self.flipped = flipped

        # initialise the card border
        self.card_background = BorderRadiusRectangle(self.center_x, self.center_y, self.width, self.height, (*self.colour, self.alpha), border_rad=5)
        self.card_back = arcade.load_texture("images/card_back.png")

    def draw(self):
        # render the card
        self.card_background.draw()
        # render either face or back, depending on side visible
        if self.face == "back":
            if self.flipped:
                arcade.draw_texture_rectangle(self.center_x, self.center_y, 110, 160, self.card_back, alpha=self.alpha, angle=180)
            else:
                arcade.draw_texture_rectangle(self.center_x, self.center_y, 110, 160, self.card_back, alpha=self.alpha)
        elif self.face == "face":
            arcade.draw_rectangle_outline(self.center_x, self.center_y, 110, 160, (220,32,32,self.alpha))
            arcade.draw_texture_rectangle(self.center_x, self.center_y - 24, 100, 100, self.image[1], alpha=self.alpha)

    def update_position(self, x, y):
        # update the position of the card
        self.center_x = x
        self.center_y = y
        self.card_background.update_position(self.center_x, self.center_y)

    def update_alpha(self, alpha):
        # update the alpha of the card
        self.alpha = alpha
        self.card_background.colour = (*card_background.colour[:3], self.alpha)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        # plays the card
        self.present_snap.play_card(self)
