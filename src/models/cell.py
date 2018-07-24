import enum

# @enum.unique
class Type(enum.Enum):
    FREE = 0
    OBSTACLE = 1

class Cell:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.phe = 0.0

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def get_pos(self):
        return self.x_pos, self.y_pos

    def get_phe(self):
        return self.phe

    def set_phe(self, phe):
        self.phe = phe