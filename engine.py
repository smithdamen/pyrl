# IMPORT STATEMENTS
print('# running imports')
# import system files
import tcod as libtcod
print('# system files imported')

# import engine files
from src.entity import Entity
from src.input_handlers import handle_keys
from src.render_functions import clear_all, render_all
from src.map import GameMap
print('# engine files imported')

# import data files
print('# data files imported')
print('# imports completed')


# MAIN GAME LOOP
print('# starting main')
def main():
    print('# initializing variables')
    screen_width = 120
    screen_height = 70
    map_width = 80
    map_height = 50
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # eventually move these colors out to their own file in data/colors
    colors = {
            'dark_wall': libtcod.Color(0, 0, 100),
            'dark_ground': libtcod.Color(50, 50, 150)
            }
    print('# variables initialized')

    # initialize entities
    # TODO: possibly change '@' to a variable referenced from a symbols file
    player = Entity(int(map_width / 2), int(map_height / 2), '@', libtcod.white)
    npc = Entity(int(map_width / 2 - 5), int(map_height / 2), '@', libtcod.yellow)

    # store list of entities
    entities = [npc, player]

    # assign font
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # variables holding key components for the engine
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    con = libtcod.console_new(screen_width, screen_height)
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # initialize root console
    libtcod.console_init_root(screen_width, screen_height, 'pyrl', False)


    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # renders entities to the screen
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        libtcod.console_flush()

        # clears entities from screen when they move or are destroyed
        clear_all(con, entities)

        # listen for keypresses
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
