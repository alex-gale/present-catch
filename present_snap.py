import arcade, random, textwrap, time
from classes.scene import Scene

class PresentSnap(Scene):
    def __init__(self, game):
        super().__init__(game)

        arcade.set_background_color((71, 71, 71))
        self.background = arcade.load_texture("images/present_snap/table.jpg")

        # set colours
        self.TEXT_COLOUR = (231,205,182)

        self.images = arcade.load_textures("images/present_snap/present_snap_sprites.png", [
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
        self.images_names = [
            "Santa Claus",
            "Candy Cane",
            "Present",
            "Stocking",
            "Christmas Tree",
            "Holly Leaves",
            "Christmas Wreath",
            "Gingerbread Man",
            "Christmas Candles",
            "Baubles",
            "Christmas Pudding",
            "Snow Globe",
            "Christmas Robin"
            ]

        # initialise all card backgrounds
        self.card_texture = arcade.load_texture("images/present_snap/card.png")
        self.card_texture_dark = arcade.load_texture("images/present_snap/card_dark.png")
        self.card_texture_brown = arcade.load_texture("images/present_snap/card_brown.png")
        self.card_texture_brown_small = arcade.load_texture("images/present_snap/card_brown_small.png")

        # the player's decorator deck
        self.player_decorator_card = Card(self, 105, 127, 125, 175)

        # the computer's decorator deck
        self.computer_decorator_card = Card(self, 695, 378, 125, 175, angle=180)

        # initialise the empty play pile message
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

        self.computer_card = None
        self.computer_turn_time = None

        # track wins
        self.winner = None

        # track snaps
        self.snap = False
        self.snap_history = []
        self.snap_timer = None
        self.snap_winner_timer = 0

        # initialise the unshuffled deck in form [name, image]
        self.deck = [[self.images_names[i], self.images[i]] for i in range(13)] * 4

        # deal the cards
        self.play_pile = []
        random.shuffle(self.deck)
        self.player_hand = self.deck[:len(self.deck) // 2]
        self.computer_hand = self.deck[len(self.deck) // 2:]

        # initialise first card
        self.current_card = Card(self, 105, 127, 125, 175, card_info=self.player_hand[0], face="back")
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
            self.current_card = Card(self, 105, 127, 125, 175, card_info=self.player_hand[0], face="back")

        # next turn starts
        self.computer_turn_time = 0.8
        self.turn_number += 1

    def player_snap(self):
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
            arcade.draw_texture_rectangle(102, 127, 125, 175, self.card_texture)
            arcade.draw_texture_rectangle(104, 127, 125, 175, self.card_texture_dark)
            self.player_decorator_card.draw()

        # draw computer's decorator deck
        if len(self.computer_hand) > 1:
            arcade.draw_texture_rectangle(698, 378, 125, 175, self.card_texture)
            arcade.draw_texture_rectangle(696, 378, 125, 175, self.card_texture_dark)
        if len(self.computer_hand) > 0:
            self.computer_decorator_card.draw()

        # draw top card in play pile
        if len(self.play_pile) > 0:
            self.play_pile[-1][1].draw()
        else:
            # draw empty play pile with description
            arcade.draw_texture_rectangle(345, 253, 125, 175, self.card_texture_brown)
            for i, line in enumerate(self.play_pile_desc):
                arcade.draw_text(line, 345, 318 - (20 * i), self.TEXT_COLOUR, 13, font_name=self.FONT, anchor_x="center")

        # draw second card in play pile
        if len(self.play_pile) > 1:
            # self.second_card_box.draw()
            arcade.draw_texture_rectangle(467, 305, 50, 70, self.card_texture)
            arcade.draw_rectangle_outline(467, 305, 40, 60, color=(220,32,32))
            arcade.draw_texture_rectangle(467, 296, 40, 40, texture=self.play_pile[-2][0][1])
        else:
            # draw empty previous pile
            arcade.draw_texture_rectangle(467, 305, 50, 70, self.card_texture_brown_small)

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

        # draw the computer's card
        if self.computer_turn_time is not None:
            self.computer_card.draw()

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
        # sets time remaining of the snap win message
        if self.snap_winner_timer > 0:
            self.snap_winner_timer -= delta_time

        # snap detection
        if len(self.play_pile) > 1 and self.play_pile[-1][0] == self.play_pile[-2][0]:
            self.snap = True

            # add snap button to button list
            if self.snap_button not in self.button_list:
                self.button_list.append(self.snap_button)
            
            # random time for computer to get snap
            if self.snap_timer == None:
                self.snap_timer = random.uniform(0.7, 1.3)
            
            if self.snap_timer <= 0:
                # computer gets snap
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

                if self.computer_card is None:
                    self.computer_card = Card(self, 695, 378, card_info=self.computer_hand[0], angle=180)
                    self.computer_turn_time = 0.6

                else:
                    self.computer_turn_time -= delta_time
                    if self.computer_card.center_x > 345 and self.computer_card.center_y > 253:
                        self.computer_card.center_x -= (self.computer_card.center_x - 345) / (self.computer_turn_time / delta_time)
                        self.computer_card.center_y -= (self.computer_card.center_y - 253) / (self.computer_turn_time / delta_time)
                        self.computer_card.alpha = 190

                    if self.computer_card.center_x == 345 and self.computer_card.center_y == 253:
                        if self.computer_turn_time <= 0:
                            if self.computer_card.alpha > 150:
                                self.computer_turn_time = 0.25

                        self.computer_turn_time -= delta_time
                        self.computer_card.alpha -= self.computer_card.alpha / (self.computer_turn_time / delta_time)

                        if round(self.computer_turn_time, 1) == 0:
                            # play the card
                            self.computer_card.alpha = 0
                            self.computer_turn_time = None

                            self.computer_card.height = 175
                            self.computer_card.width = 125
                            self.computer_card.alpha = 255
                            self.computer_card.face = "front"
                            self.computer_card.angle = 0

                            self.play_pile.append([self.computer_hand.pop(0), self.computer_card])
                            self.computer_card = None
                            self.computer_turn_time = None

                            self.turn_number += 1

                    elif self.computer_card.center_x < 345 or self.computer_card.center_y < 253:
                        self.computer_card.center_x = 345
                        self.computer_card.center_y = 253

                # if self.computer_turn_time <= 0:
                #     # instantiate card
                #     computer_card = Card(self, 695, 378, 125, 175, card_info=self.computer_hand[0])

                #     # add to play pile
                #     self.play_pile.append([self.computer_hand.pop(0), computer_card])

                #     # next turn starts
                #     self.turn_number += 1
                # else:
                #     self.computer_turn_time -= delta_time

    def unload(self):
        # unloads the snap button if the game is quit while a snap is detected
        if self.snap:
            self.reset_snap()

    # handle key presses
    def key_press(self, key, modifiers):
        pass

    def key_release(self, key, modifiers):
        # exit game wen escape is pressed
        if key == arcade.key.ESCAPE:
            self.game.change_game_state("GAME_MENU")

    # handle mouse motion
    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.current_card.pressed:
            if self.current_card.alpha != 190:
                self.current_card.update_alpha(190)
            self.current_card.update_position(x, y)
            


class Card:
    def __init__(self, present_snap, x=0, y=0, width=125, height=175, card_info=['', None], alpha=255, face="back", angle=0):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.angle = angle

        self.alpha = alpha

        self.present_snap = present_snap

        # card information [name, image]
        text_wrapper = textwrap.TextWrapper(width=11)
        self.name = text_wrapper.wrap(card_info[0])
        self.image = card_info[1]

        # set the current texture of the card
        self.face = face

        # initialise the card textures
        self.card_texture = arcade.load_texture("images/present_snap/card.png")
        self.card_back = arcade.load_texture("images/present_snap/card_back.png")

    def draw(self):
        # render the card
        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.card_texture, alpha=self.alpha, angle=self.angle)

        # render either face or back, depending on side visible
        if self.face == "back":
                arcade.draw_texture_rectangle(self.center_x, self.center_y, round(self.width - (2 * self.width / 17.86)), self.height - (2 * self.height / 25), self.card_back, alpha=self.alpha, angle=self.angle)

        elif self.face == "front":
            arcade.draw_rectangle_outline(self.center_x, self.center_y, 110, 160, (220,32,32,self.alpha))
            arcade.draw_texture_rectangle(self.center_x, self.center_y - 24, 100, 100, self.image, alpha=self.alpha, angle=self.angle)

            for i, line in enumerate(self.name):
                arcade.draw_text(line, self.center_x, self.center_y + 50 - (15 * i), (220,32,32,self.alpha), 15, font_name="fonts/Courgette-Regular.ttf", anchor_x="center", anchor_y="center")

    def update_position(self, x, y):
        # update the position of the card
        self.center_x = x
        self.center_y = y

    def update_alpha(self, alpha):
        # update the alpha of the card
        self.alpha = alpha

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

        # plays the card when the player drags it to the play pile
        if 280 < self.center_x < 410 and 165 < self.center_y < 341:
            self.update_alpha(255)
            self.present_snap.play_card(self)
        elif self.center_x == 105 and self.center_y == 127 and self.alpha == 255:
            self.present_snap.play_card(self)
        else:
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
