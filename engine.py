# IMPORT STATEMENTS
print('# running imports')
# import system files
import tcod as libtcod
print('# system files imported')

# import engine files
from src.entity import Entity, get_blocking_entities_at_location
from src.input_handlers import handle_keys
from src.render_functions import clear_all, render_all
from src.map import GameMap
from src.fov import initialize_fov, recompute_fov
from src.game_states import GameStates
print('# engine files imported')

# import data files
from data.colors import Colors
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
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 6
    max_monsters_per_room = 3

    # eventually move these colors out to their own file in data/colors
    colors = {
            'dark_wall_fg': Colors.black,
            'dark_wall_bg': Colors.darkGray,
            'dark_ground': Colors.darkGray,
            'light_wall_fg': Colors.darkGray,
            'light_wall_bg': Colors.lightGray,
            'light_ground': Colors.lightGray
            }
    print('# variables initialized')

    # initialize entities
    # TODO: possibly change '@' to a variable referenced from a symbols file
    player = Entity(0, 0, '@', Colors.white, 'Player', blocks=True)

    # store list of entities
    entities = [player]

    # assign font
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # variables holding key components for the engine
    print('# initialize compoent variables')
    con = libtcod.console_new(screen_width, screen_height)
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    game_state = GameStates.PLAYERS_TURN
    print('# components initialized')

    # initialize root console
    libtcod.console_init_root(screen_width, screen_height, 'pyrl', False)


    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # check if the fov needs to be updated
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # renders entities to the screen
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        #after rendering, tell loop it no longer needs to recompute the FOV
        fov_recompute = False

        libtcod.console_flush()

        # clears entities from screen when they move or are destroyed
        clear_all(con, entities)

        # listen for keypresses
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # handle the player's turn
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name)

                else:
                    player.move(dx, dy)
                    fov_recompute = True

                # after player takes a turn, increment the game state
                game_state = GameStates.ENEMY_TURN
                print('# player turn complete')

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # handle the enemies turns
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' takes their turn')

            # after processing enemies, return game state to player's turn
            game_state = GameStates.PLAYERS_TURN
            print('# enemy turns complete')

if __name__ == '__main__':
    main()
