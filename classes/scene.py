import arcade

class Scene:
    def __init__(self, game):
        ## this is run when the scene is initially created
        self.game = game
        # buttons added to this list will have click detection
        self.button_list = []

    def setup(self):
        ## this is run every time the game state is changed to this scene
        pass

    def unload(self):
        ## this is run every time the game state is changed away from this scene
        pass

    def draw(self):
        ## this is run every time the game is drawn and this is the current scene
        pass

    def update(self, delta_time):
        ## this is run every time the game is updated and this is the current scene
        pass

    def key_press(self, key, modifier):
        ## this is run whenever a key is pressed
        pass

    def key_release(self, key, modifier):
        ## this is run whenever a key is released
        pass

    def mouse_movement(self, x, y, dx, dy):
        ## this is run whenever the mouse is moved
        pass

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        ## this is run whenever the mouse is dragged
        pass
