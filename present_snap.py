import arcade, random, textwrap, time
from classes.scene import Scene
from classes.shapes import BorderRadiusRectangle

class PresentSnap(Scene):
    def __init__(self, game):
        super().__init__(game)

        # background
        arcade.set_background_color((71, 71, 71))
        self.background = arcade.load_texture("images/present_snap/table.jpg")

        # set text colour
        self.text_colour = (231,205,182)

        # initialise all the images
        self.images = arcade.load_textures("images/present_snap/present_snap_sprites.png",[
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
        self.computer_pile = BorderRadiusRectangle(self.game.SCREEN_WIDTH - 102, self.game.SCREEN_HEIGHT - 222, 125, 175, (240,240,240), 5)
        self.computer_separator = BorderRadiusRectangle(self.game.SCREEN_WIDTH - 47, self.game.SCREEN_HEIGHT - 222, 11, 175, (25,25,25), 5)
        self.computer_decorator_card = Card(self, self.game.SCREEN_WIDTH - 105, self.game.SCREEN_HEIGHT - 222, 125, 175, colour=(240,240,240), flipped=True)

        # initialise the empty play pile
        self.empty_play_pile = BorderRadiusRectangle(345, 253, 125, 175, colour=(147,91,30), border_rad=5)
        text_wrapper = textwrap.TextWrapper(width=15)
        self.play_pile_desc = text_wrapper.wrap("This is the play pile.\nCards will be placed here once played.")

        # initialise box to show the second card
        self.second_card_box = BorderRadiusRectangle(467, 305, 50, 70, colour=(240,240,240), border_rad=5)
        self.empty_second_box = BorderRadiusRectangle(467, 305, 50, 70, colour=(147,91,30), border_rad=5)

        # initialise snap button
        self.snap_button_texture = arcade.load_texture("images/present_snap/snap_button.png")
        self.snap_button = SnapButton(self, 400, 86, 128, 64, self.snap_button_texture)

        self.drawn = False

    def setup(self):
        # makes the first card playable
        self.played_card = True

        # keeps track of player and computer turns
        self.turn_number = 1

        # keep track of snaps
        self.snap = False
        self.snap_frame = 0

        # self.player_snap = False
        self.computer_snap = False
        self.snap_history = []

        # track the time for the computer to wait before snapping
        self.computer_snap_time = 0
        self.snap_frames = 0

        self.snap_display_timer = 0

        # deal the cards
        self.play_pile = []
        random.shuffle(self.deck)
        self.player_hand = self.deck[:26]
        self.computer_hand = self.deck[26:]
        self.current_card = Card(self, 105, 127, 125, 175, image=self.player_hand[0], colour=(240,240,240), face="back")

    def draw(self):

        # central line
        # arcade.draw_line(self.game.SCREEN_WIDTH // 2, 0, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT, (255, 0, 0))
        # arcade.draw_line((self.game.SCREEN_WIDTH // 2) + 1, 0, (self.game.SCREEN_WIDTH // 2) + 1, self.game.SCREEN_HEIGHT, (255, 0, 0))

        # draw background
        arcade.draw_texture_rectangle(400, 300, 800, 600, texture=self.background)

        # draw player card pile
        if len(self.player_hand) > 1:
            self.player_pile.draw()
            self.player_separator.draw()
            self.player_decorator_card.draw()
        if len(self.player_hand) > 0:
            self.current_card.draw()

        # draw computer card pile
        if len(self.computer_hand) > 1:
            self.computer_pile.draw()
            self.computer_separator.draw()
        if len(self.computer_hand) > 0:
            self.computer_decorator_card.draw()

        # tells the player which turn it is
        arcade.draw_text( ("Your " if self.turn_number % 2 == 1 else "Computer's ") + "turn",
                        400, 50, self.text_colour, 20, font_name="fonts/Courgette-Regular.ttf", anchor_x="center")
        
        # number of cards for player and computer
        # player
        arcade.draw_text("Cards: {}".format( len(self.player_hand) ), 43, 224, self.text_colour, 13, font_name="fonts/Courgette-Regular.ttf", anchor_x="left")
        # computer
        arcade.draw_text("Cards: {}".format( len(self.computer_hand) ), 727, 281, self.text_colour, 13, font_name="fonts/Courgette-Regular.ttf", anchor_x="center", anchor_y="top")

        # PLAY PILE
        # labels
        arcade.draw_text("Play Pile", 273, 306, (*self.text_colour, 140), 13, font_name="fonts/Courgette-Regular.ttf", anchor_x="center", anchor_y="center", rotation=90)
        arcade.draw_text("Previous", 432, 306, (*self.text_colour, 140), 13, font_name="fonts/Courgette-Regular.ttf", anchor_x="center", anchor_y="center", rotation=90)

        # draws the empty play pile
        if len(self.play_pile) == 0:

            self.empty_play_pile.draw()
            # description text
            for i, line in enumerate(self.play_pile_desc):
                arcade.draw_text(line, 345, 318 - (20 * i), self.text_colour, 13, font_name="fonts/Courgette-Regular.ttf", anchor_x="center")

        # draws the top card in the play pile
        elif len(self.play_pile) != 0:
            self.play_pile[-1][1].draw()

        # displays the second card in the play pile
        if len(self.play_pile) > 1:
            self.second_card_box.draw()
            arcade.draw_rectangle_outline(467, 305, 40, 60, color=(220,32,32))
            arcade.draw_texture_rectangle(467, 296, 40, 40, texture=self.play_pile[-2][0][1])
        else:
            # displays empty box for the second card
            self.empty_second_box.draw()

        # renders if snap is drawn
        if self.snap:
            self.snap_button.draw()
            # arcade.draw_texture_rectangle(400, 124, 128, 64, texture=self.snap_button_texture)

        # tell the player who got snap
        if self.snap_display_timer > 0:
            self.snap_display_timer -= 1
            arcade.draw_text( ("You " if self.snap_history[-1] == "player" else "Computer ") + "got snap!",
                400, 430, self.text_colour, 16, font_name="fonts/Courgette-Regular.ttf", anchor_x="center")

        # allows logic to execute
        self.drawn = True

    def update(self, delta_time):
        # snap detection
        if self.drawn:

            if len(self.play_pile) > 1 and self.play_pile[-1][0] == self.play_pile[-2][0]:
                self.snap = True

                # add snap button to button list
                if self.snap_button not in self.button_list:
                    self.button_list.append(self.snap_button)
                    # print(self.button_list)

                if self.computer_snap_time == 0:
                    self.computer_snap_time = random.uniform(0.7,1.3)
                    self.snap_frames = self.computer_snap_time * 60
                    # print("delta_time: {}\ncomputer_snap_time: {}\nsnap_frames: {}\nsnap_frame: {}".format(delta_time, self.computer_snap_time, self.snap_frames, self.snap_frame))

                # tests if computer gets a snap before player
                if self.snap_frame > self.snap_frames:
                    self.computer_snap = True
                    print("computer snap")

                    # no longer snap situation (reset snap)
                    self.snap = False
                    self.snap_frame = 0
                    self.computer_snap_time = 0
                    self.snap_frames = 0

                    # computer takes all cards in snap pile to the bottom of its deck
                    self.computer_hand += [item[0] for item in self.play_pile]
                    # empty the play pile
                    self.play_pile = []

                    # no longer snap on next move
                    self.computer_snap = False

                    # remove snap button from button list
                    self.button_list.remove(self.snap_button)

                    self.snap_history.append("computer")
                    self.snap_display_timer = 1.5 * 60

                    self.drawn = False

                else:
                    self.snap_frame += 1



            # when a card is played, the next card becomes the current card and becomes pressable
            if self.turn_number % 2 == 1 and not self.snap:
                # checks that it's the players turn
                if len(self.player_hand) > 0 and self.played_card:
                    # the player has not played a card in the current turn
                    self.played_card = False
                    # make next card pressable
                    self.button_list.append(self.current_card)
                    # print("added to button list\n{}".format(self.button_list))

            # do the computer's move if it's the computer's turn
            elif self.turn_number % 2 == 0 and not self.snap:
                # wait for a bit before the computer moves
                time.sleep(0.8)
                
                # create the card
                computer_card = Card(self, self.game.SCREEN_WIDTH - 105, self.game.SCREEN_HEIGHT - 127, 125, 175, image=self.computer_hand[0], colour=(240,240,240), flipped=True)
                
                # move the card to the play pile
                computer_card.update_position(345, 253)
                computer_card.flipped = False
                computer_card.face = "face"

                # the next turn begins
                self.turn_number += 1

                self.play_pile.append([self.computer_hand.pop(0), computer_card])


            self.drawn = False

    def snap_player(self):
        # checks computer hasn't already got snap
        if not self.computer_snap:

            print("player snap")

            # no longer snap situation (reset snap)
            self.snap = False
            self.computer_snap_time = 0
            self.snap_frame = 0
            self.snap_frames = 0

            # player takes all cards in snap pile to the bottom of their deck
            self.player_hand += [item[0] for item in self.play_pile]
            # empty the play pile
            self.play_pile = []

            # no longer snap on next move
            # self.player_snap = False

            # remove snap button from button list
            self.button_list.remove(self.snap_button)

            self.snap_history.append("player")
            self.snap_display_timer = 1.5 * 60

        # force game to draw before executing logic again
        self.drawn = False

    def play_card(self, card):
        # moves the card to the play pile and removes from the player's hand
        card.update_position(345, 253)
        card.face = "face"

        self.play_pile.append([self.player_hand.pop(0), self.current_card])
        
        # stops the played card being pressable
        self.button_list.remove(self.current_card)

        # instantiates the next card
        if len(self.player_hand) > 0:
            self.current_card = Card(self, 105, 127, 125, 175, image=self.player_hand[0], colour=(240,240,240), face="back")

        # makes the next card playable
            self.played_card = True

        # the next turn will occur (computer turn)
        self.turn_number += 1

        self.drawn = False


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
        self.card_back = arcade.load_texture("images/present_snap/card_back.png")

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

class SnapButton:
    def __init__(self, present_snap, x=0, y=0, width=64, height=64, image=None):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

        self.image = image

        self.present_snap = present_snap

    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.image)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        # player gets snap
        self.present_snap.snap_player()
