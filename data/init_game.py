import tcod as libtcod
from data.colors import Colors
from src.fighter import Fighter
from src.inventory import Inventory
from src.entity import Entity
from src.messages import MessageLog
from src.game_states import GameStates
from src.map import GameMap
from src.render_functions import RenderOrder

def get_constants():
    window_title = "PYRL"

    # set dimensions of consoles
    screen_width = 120
    screen_height 70
    map_width = 80
    map_height = 50
    msg_width = 80
    msg_height = 15
    bars_width = 80
    bars_height = 5
    status_width = 40
    status_height = 20
    enemy_list_width = 40
    enemy_list_height = 50

    # assign font
    game_font = 'fonts/Potash-10x10.png'

    # set positions of consoles
    msg_x = 0
    msg_y = 0
    map_x = 0
    map_y = msg_height + 1
    bars_x = 0
    bars_y = msg_height + map_height + 1
    status_x = msg_width + 1
    status_y = 0
    enemy_list_x = msg_width + 1
    enemy_list_y = status_height + 1

    # dungeon variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 6
    max_monsters_per_room = 3
    max_items_per_room = 3

    # dungeon terrain colors
    colors = {
            'dark_wall_fg': Colors.black,
            'dark_wall_bg': Colors.darkGray,
            'dark_ground': Colors.darkGray,
            'light_wall_fg': Colors.black,
            'light_wall_bg': Colors.lightGray,
            'light_ground': Colors.lightGray
    }

    # assign constants for use in engine
    constants = {
            'window_title': window_title,
            'screen_width': screen_width,
            'screen_height': screen_height,
            'map_width': map_width,
            'map_height': map_height,
            'msg_width': msg_width,
            'msg_height': msg_height,
            'bars_width': bars_width,
            'bars_height': bars_height,
            'status_width': status_width,
            'status_height': status_height,
            'enemy_list_width': enemy_list_width,
            'enemy_list_height': enemy_list_height,
            'msg_x': msg_x,
            'msg_y': msg_y,
            'map_x': map_x,
            'map_y': map_y,
            'bars_x': bars_x,
            'bars_y': bars_y,
            'status_x': status_x,
            'status_y': status_y,
            'enemy_list_x': enemy_list_x,
            'enemy_list_y': enemy_list_y,
            'room_max_size': room_max_size,
            'room_min_size': room_min_size,
            'max_rooms': max_rooms,
            'fov_algorithm': fov_algorithm,
            'fov_light_walls': fov_light_walls,
            'fov_radius': fov_radius,
            'max_monsters_per_room': max_monsters_per_room,
            'max_items_per_room': max_items_per_room,
            'colors': colors
    }

    return constants

# set up game components
def get_game_variables(constants):
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])

    msg_log = MessageLog(constants['msg_x'], constants['msg_width'], constants['msg_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, msg_log, game_state
