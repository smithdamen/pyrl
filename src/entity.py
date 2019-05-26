# generic entity class to represent players, enemies, items, etc.
class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    # moves the entity
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
