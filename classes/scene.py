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

    def draw(self):
        ## this is run every time the game is drawn and this is the current scene
        pass

    def update(self, delta_time):
        ## this is run every time the game is updated and this is the current scene
        pass
