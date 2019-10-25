import arcade

class ImageButton(arcade.Sprite):
    def __init__(self, filename=None, x=0, y=0):
        super().__init__(filename, center_x=x, center_y=y)

        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        print("hey")


def check_mouse_press_for_buttons(x, y, button_list):
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue

        button.on_press()

def check_mouse_release_for_buttons(_x, _y, button_list):
    for button in button_list:
        if button.pressed:
            button.on_release()