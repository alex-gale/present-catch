import arcade

class BorderRadiusRectangle:
    def __init__(self, x=0, y=0, width=100, height=100, colour=(255,255,255), border_rad=0, resolution=1):

        self.center_x = x
        self.center_y = y

        self.width = width
        self.height = height

        self.colour = colour
        self.border_rad = border_rad
        self.res = resolution

        self.set_points()

    def set_points(self):
        # define points on the rectangle
        self.bottom_l_1 = (self.center_x - (self.width // 2), self.center_y - (self.height // 2) + self.border_rad)
        self.top_l_1 = (self.center_x - (self.width // 2), self.center_y + (self.height // 2) - self.border_rad)
        self.top_l_2 = (self.center_x - (self.width // 2) + self.border_rad, self.center_y + (self.height // 2))
        self.top_r_1 = (self.center_x + (self.width // 2) - self.border_rad, self.center_y + (self.height // 2))
        self.top_r_2 = (self.center_x + (self.width // 2), self.center_y + (self.height // 2) - self.border_rad)
        self.bottom_r_1 = (self.center_x + (self.width // 2), self.center_y - (self.height // 2) + self.border_rad)
        self.bottom_r_2 = (self.center_x + (self.width // 2) - self.border_rad, self.center_y - (self.height // 2))
        self.bottom_l_2 = (self.center_x - (self.width // 2) + self.border_rad, self.center_y - (self.height // 2))

    def update_position(self, x, y):
        self.center_x = x
        self.center_y = y
        self.set_points()

    def draw(self):
        # render the shape
        arcade.draw_polygon_filled([
            self.bottom_l_1,
            self.top_l_1,
            self.top_l_2,
            self.top_r_1,
            self.top_r_2,
            self.bottom_r_1,
            self.bottom_r_2,
            self.bottom_l_2
            ], self.colour)
