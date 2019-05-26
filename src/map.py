import tcod as libtcod
from random import randint
from src.tile import Tile
from src.entity import Entity
from src.rectangle import Rect
from data.colors import Colors

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # starts with a solid map and carves out areas
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # generate a random width and height for the rooms
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # get a random position within the bounds of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h -1)

            # use the Rect class to make rooms
            new_room = Rect(x, y, w, h)

            # check for intersections
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            # if the rooms didn't intersect, room is valid
            else:
                self.create_room(new_room)

                # get coords of center of the room
                (new_x, new_y) = new_room.center()

                # place player in the first room
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y

                # connect subsequent rooms with tunnels
                else:
                    # get center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms -1].center()

                    # determine whether to start horizontally or vertically
                    if randint(0, 1) == 1:
                        # horizontal first
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)

                    else:
                        # vertical first
                        self.create_v_tunnel(prev_y, new_y, new_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)

                # place entities in rooms
                self.place_entities(new_room, entities, max_monsters_per_room)

                # lastly, add the new room to the list of rooms
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # iterate through tiles in room and make them not blocked
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    # creates halls between rooms in the dungeon map
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # place entities in rooms
    def place_entities(self, room, entities, max_monsters_per_room):
        # get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        # select a random location in a room to place the monster
        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # choose an entity to place based on percentage chance
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', Colors.green, 'orc', blocks=True)

                else:
                    monster = Entity(x, y, 'T', Colors.green, 'troll', blocks=True)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
