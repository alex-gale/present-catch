import arcade, random, textwrap, time
from classes.scene import Scene
from classes.shapes import BorderRadiusRectangle

class PresentSnap(Scene):
    def __init__(self, game):
        super().__init__(game)

        arcade.set_background_color((71, 71, 71))
        self.background = arcade.load_texture("images/present_snap/table.jpg")

        # set colours
        self.TEXT_COLOUR = (231,205,182)
        self.CARD_COLOUR = (240,240,240)

        images = arcade.load_textures("images/present_snap/present_snap_sprites.png",[
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
        images_names = ["Santa Claus", "Candy Cane", "Present", "Stocking", "Christmas Tree", "Holly Leaves", "Christmas Wreath", "Gingerbread Man", "Christmas Candles", "Baubles", "Christmas Pudding", "Snow Globe", "Christmas Robin"]

        # initialise the deck in form [name, image]
        self.deck = [[images_names[i], images[i]] for i in range(13)] * 4
        # self.deck = [[images_names[0], images[0]] for i in range(2)]

        # the player's decorator deck
        self.player_pile = BorderRadiusRectangle(102, 127, 125, 175, self.CARD_COLOUR, 5)
        self.player_separator = BorderRadiusRectangle(47, 127, 11, 175, (25,25,25), 5)
        self.player_decorator_card = Card(self, 105, 127, 125, 175, colour=self.CARD_COLOUR)

        # the computer's decorator deck
        self.computer_pile = BorderRadiusRectangle(698, 378, 125, 175, self.CARD_COLOUR, 5)
        self.computer_separator = BorderRadiusRectangle(753, 378, 11, 175, (25,25,25), 5)
        self.computer_decorator_card = Card(self, 695, 378, 125, 175, colour=self.CARD_COLOUR, angle=180)

        # initialise box to show second card
        self.second_card_box = BorderRadiusRectangle(467, 305, 50, 70, colour=self.CARD_COLOUR, border_rad=5)
        self.empty_second_box = BorderRadiusRectangle(467, 305, 50, 70, colour=(147,91,30), border_rad=5)

        # initialise the empty play pile
        self.empty_play_pile = BorderRadiusRectangle(345, 253, 125, 175, colour=(147,91,30), border_rad=5)
        text_wrapper = textwrap.TextWrapper(width=15)
        self.play_pile_desc = text_wrapper.wrap("This is the play pile.\nPlace cards here to start playing.")

        # initialise snap button
        self.snap_button_texture = arcade.load_texture("images/present_snap/snap_button.png")
        self.snap_button = SnapButton(self, 400, 116, 128, 64, self.snap_button_texture)

        # initialise the font
        self.FONT = "fonts/Courgette-Regular.ttf"

    def setup(self):
        # track turns
        self.turn_number = 0
        self.computer_turn_time = 0.8

        # track wins
        self.winner = None

        # track snaps
        self.snap = False
        self.snap_history = []
        self.snap_timer = None
        self.snap_winner_timer = 0

        # deal the cards
        self.play_pile = []
        random.shuffle(self.deck)
        self.player_hand = self.deck[:len(self.deck) // 2]
        self.computer_hand = self.deck[len(self.deck) // 2:]

        # initialise first card
        self.current_card = Card(self, 105, 127, 125, 175, card_info=self.player_hand[0], colour=self.CARD_COLOUR, face="back")
        self.button_list.append(self.current_card)

        # initialise the play pile
        self.play_pile = []


    def play_card(self, card):
        # show the card
        card.face = "front"
        card.update_position(345, 253)

        # remove from button list
        self.button_list.remove(card)

        # add to play pile
        self.play_pile.append([self.player_hand.pop(0), card])

        # instantiate next card
        if len(self.player_hand) > 0:
            self.current_card = Card(self, 105, 127, 125, 175, card_info=self.player_hand[0], colour=self.CARD_COLOUR, face="back")

        # next turn starts
        self.computer_turn_time = 0.8
        self.turn_number += 1

    def player_snap(self):
        print("player snap")
        # merge to player's hand and remove from play pile
        self.player_hand += [item[0] for item in self.play_pile]
        self.play_pile = []

        # add to history
        self.snap_history.append("player")

        # reset snap status
        self.reset_snap()

    def reset_snap(self):
        # resets everything for the next snap
        self.button_list.remove(self.snap_button)
        self.snap = False
        self.snap_timer = None
        self.snap_winner_timer = 1.5


    def draw(self):
        # draw background
        arcade.draw_texture_rectangle(400, 300, 800, 600, self.background)

        # draw player's decorator deck
        if len(self.player_hand) > 1:
            self.player_pile.draw()
            self.player_separator.draw()
            self.player_decorator_card.draw()

        # draw computer's decorator deck
        if len(self.computer_hand) > 1:
            self.computer_pile.draw()
            self.computer_separator.draw()
        if len(self.computer_hand) > 0:
            self.computer_decorator_card.draw()

        # draw top card in play pile
        if len(self.play_pile) > 0:
            self.play_pile[-1][1].draw()
        else:
            # draw empty play pile with description
            self.empty_play_pile.draw()
            for i, line in enumerate(self.play_pile_desc):
                arcade.draw_text(line, 345, 318 - (20 * i), self.TEXT_COLOUR, 13, font_name=self.FONT, anchor_x="center")

        # draw second card in play pile
        if len(self.play_pile) > 1:
            self.second_card_box.draw()
            arcade.draw_rectangle_outline(467, 305, 40, 60, color=(220,32,32))
            arcade.draw_texture_rectangle(467, 296, 40, 40, texture=self.play_pile[-2][0][1])
        else:
            # draw empty previous pile
            self.empty_second_box.draw()

        # label the piles
        arcade.draw_text("Play Pile", 273, 306, (*self.TEXT_COLOUR, 140), 13, font_name=self.FONT, anchor_x="center", anchor_y="center", rotation=90)
        arcade.draw_text("Previous", 432, 306, (*self.TEXT_COLOUR, 140), 13, font_name=self.FONT, anchor_x="center", anchor_y="center", rotation=90)

        # draw number of cards for player and computer
        arcade.draw_text("Cards: {}".format(len(self.player_hand)), 43, 224, self.TEXT_COLOUR, 13, font_name=self.FONT, anchor_x="left")
        arcade.draw_text("Cards: {}".format(len(self.computer_hand)), 727, 267, self.TEXT_COLOUR, 13, font_name=self.FONT, anchor_x="center")

        # tell the player whose turn it is
        arcade.draw_text( ("Your " if self.turn_number % 2 == 0 else "Computer's ") + "turn",
                        400, 50, self.TEXT_COLOUR, 20, font_name=self.FONT, anchor_x="center")

        # say who won the previous snap
        if self.snap_winner_timer > 0:
            arcade.draw_text(("You " if self.snap_history[-1] == "player" else "Computer ") + "got snap!",
                400, 430, self.TEXT_COLOUR, 16, font_name=self.FONT, anchor_x="center")

        # draw snap button
        if self.snap:
            self.snap_button.draw()

        # draw the next card
        if len(self.player_hand) > 0:
            self.current_card.draw()

        # display if the game is done
        if self.winner:
            arcade.draw_rectangle_filled(400, 350, 600, 200, (184,184,184))
            arcade.draw_rectangle_outline(400, 350, 600, 200, (140,140,140), 4)
            # arcade.draw_text(self.winner, 400, 450, self.TEXT_COLOUR, 18, font_name=self.FONT, anchor_x="center")
            
            # player win message
            if self.winner == "player":
                title_text = "You Win!"
                main_text = "Congratulations, you beat the computer."

            # computer win message
            elif self.winner == "computer":
                title_text = "You Lose!"
                main_text = "Oh dear, it seems the computer beat you."

            # draw message
            else:
                title_text = "Draw!"
                main_text = "It seems you both ran out of cards."

            arcade.draw_text(title_text, 400, 400, (0,0,0), 25, font_name=self.FONT, anchor_x="center", anchor_y="center")
            arcade.draw_text(main_text, 400, 350, (0,0,0), 15, font_name=self.FONT, anchor_x="center", anchor_y="center")
            arcade.draw_text("Press ESCAPE to quit", 400, 300, (50,50,50), 14, font_name=self.FONT, anchor_x="center", anchor_y="center")

    def update(self, delta_time):
        # print(delta_time)

        # sets time remaining of the snap win message
        if self.snap_winner_timer > 0:
            self.snap_winner_timer -= delta_time

        # snap detection
        elif len(self.play_pile) > 1 and self.play_pile[-1][0] == self.play_pile[-2][0]:
            self.snap = True

            # add snap button to button list
            if self.snap_button not in self.button_list:
                self.button_list.append(self.snap_button)
            
            # random time for computer to get snap
            if self.snap_timer == None:
                self.snap_timer = random.uniform(0.7, 1.3)
            
            if self.snap_timer <= 0:
                # computer gets snap
                print("computer snap")
                # merge to player's hand and remove from play pile
                self.computer_hand += [item[0] for item in self.play_pile]
                self.play_pile = []

                # add to history
                self.snap_history.append("computer")

                # reset snap status
                self.reset_snap()

            else:
                self.snap_timer -= delta_time

        # player turn
        elif self.turn_number % 2 == 0:

            if len(self.player_hand) > 0 and len(self.computer_hand) > 0:
                if self.current_card not in self.button_list:
                    self.button_list.append(self.current_card)
            else:
                # someone wins. only happens on your turn
                if not self.winner:
                    if len(self.player_hand) == 0:
                        if len(self.computer_hand) == 0:
                            self.winner = "draw"
                        else:
                            self.winner = "computer"
                    else:
                        self.winner = "player"

        # computer turn
        elif self.turn_number % 2 == 1:

            if len(self.computer_hand) > 0:
                # waits before the computer takes its turn
                if self.computer_turn_time <= 0:
                    # instantiate card
                    computer_card = Card(self, 345, 253, 125, 175, card_info=self.computer_hand[0], colour=self.CARD_COLOUR, face="front")

                    # add to play pile
                    self.play_pile.append([self.computer_hand.pop(0), computer_card])

                    # next turn starts
                    self.turn_number += 1
                else:
                    self.computer_turn_time -= delta_time

    # handle key presses
    def key_press(self, key, modifiers):
        pass

    def key_release(self, key, modifiers):
        # exit game wen escape is pressed
        if key == arcade.key.ESCAPE:
            self.game.change_game_state("GAME_MENU")

    # handle mouse motion
    def mouse_movement(self, x, y, dx, dy):
        if self.current_card.active:
            self.current_card.update_position(x, y)
            self.current_card.update_alpha(190)


class Card:
    def __init__(self, present_snap, x=0, y=0, width=125, height=175, card_info=['', None], colour=(0,0,0), alpha=255, face="back", angle=0):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.angle = angle

        self.colour = colour
        self.alpha = alpha

        # card [name, image]
        text_wrapper = textwrap.TextWrapper(width=11)
        self.name = text_wrapper.wrap(card_info[0])
        self.image = card_info[1]


        self.present_snap = present_snap
        self.face = face
        self.active = False

        # initialise the card border
        self.card_background = BorderRadiusRectangle(self.center_x, self.center_y, self.width, self.height, (*self.colour, self.alpha), border_rad=5)
        self.card_back = arcade.load_texture("images/present_snap/card_back.png")

    def draw(self):
        # render the card
        self.card_background.draw()

        # render either face or back, depending on side visible
        if self.face == "back":
                arcade.draw_texture_rectangle(self.center_x, self.center_y, 110, 160, self.card_back, alpha=self.alpha, angle=self.angle)

        elif self.face == "front":
            arcade.draw_rectangle_outline(self.center_x, self.center_y, 110, 160, (220,32,32,self.alpha))
            arcade.draw_texture_rectangle(self.center_x, self.center_y - 24, 100, 100, self.image, alpha=self.alpha, angle=self.angle)

            for i, line in enumerate(self.name):
                arcade.draw_text(line, self.center_x, self.center_y + 50 - (15 * i), (220,32,32,self.alpha), 15, font_name="fonts/Courgette-Regular.ttf", anchor_x="center", anchor_y="center")
    
    def update_position(self, x, y):
        # update the position of the card
        self.center_x = x
        self.center_y = y
        self.card_background.update_position(self.center_x, self.center_y)

    def update_alpha(self, alpha):
        # update the alpha of the card
        self.alpha = alpha
        self.card_background.colour = (*self.card_background.colour[:3], self.alpha)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        # toggle self.active on press
        # if the card is within the play pile area
        if 280 < self.center_x < 410 and 165 < self.center_y < 341:
            self.update_alpha(255)
            self.present_snap.play_card(self)
        # if the card is within the player's card pile area
        elif 40 < self.center_x < 170 and 39 < self.center_y < 215:
            self.active = False if self.active else True
            if not self.active:
                self.update_position(105, 127)
                self.update_alpha(255)

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
        self.present_snap.player_snap()
