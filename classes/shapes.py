class BorderRadiusRectangle:
    def __init__(self, center, dimensions, colour, border_rad=0, resolution=1):
        self.center_x = center[0]
        self.center_y = center[1]

        self.width = dimensions[0]
        self.height = dimensions[1]

        self.colour = colour
        self.border_rad = border_rad
        self.res = resolution

        self.bottom_l_1 = (self.center_x - (self.width // 2), self.center_y - (self.height // 2) + self.border_rad)
        self.top_l_1 = (self.center_x - (self.width // 2), self.center_y + (self.height // 2) - self.border_rad)
        self.top_l_2 = (self.center_x - (self.width // 2) + self.border_rad, self.center_y + (self.height // 2))
        self.top_r_1 = (self.center_x + (self.width // 2) - self.border_rad, self.center_y + (self.height // 2))
        self.top_r_2 = (self.center_x + (self.width // 2), self.center_y + (self.height // 2) - self.border_rad)
        self.bottom_r_1 = (self.center_x + (self.width // 2), self.center_y - (self.height // 2) + self.border_rad)
        self.bottom_r_2 = (self.center_x + (self.width // 2) - self.border_rad, self.center_y - (self.height // 2))
        self.bottom_l_2 = (self.center_x - (self.width // 2) + self.border_rad, self.center_y - (self.height // 2))

    def draw(self):
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