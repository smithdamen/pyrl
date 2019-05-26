# represents a tile on the map that may or may not block sight
class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # if the tile is blocked it will block sight by default
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False
