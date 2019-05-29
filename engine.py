# IMPORT STATEMENTS
print('# running imports')
# import system files
import tcod as libtcod
print('# system files imported')

# import engine files
from src.entity import Entity, get_blocking_entities_at_location
from src.input_handlers import handle_keys
from src.render_functions import clear_all, render_all, RenderOrder
from src.map import GameMap
from src.fov import initialize_fov, recompute_fov
from src.game_states import GameStates
from src.fighter import Fighter
from src.death import kill_monster, kill_player
from src.messages import MessageLog
print('# engine files imported')

# import data files
from data.colors import Colors
print('# data files imported')

print('# imports completed')


# MAIN GAME LOOP
print('# starting main')
def main():
    print('# initializing variables')
    # set dimensions of main window and subconsoles
    screen_width = 120
    screen_height = 70
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

    # set positions of subconsoles
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

    # eventually move these colors out to their own file in data/colors
    colors = {
            'dark_wall_fg': Colors.black,
            'dark_wall_bg': Colors.darkGray,
            'dark_ground': Colors.darkGray,
            'light_wall_fg': Colors.black,
            'light_wall_bg': Colors.lightGray,
            'light_ground': Colors.lightGray
            }
    print('# variables initialized')

    # initialize entities
    # TODO: possibly change '@' to a variable referenced from a symbols file
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', Colors.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)

    # store list of entities
    entities = [player]

    # assign font
    libtcod.console_set_custom_font('fonts/terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # variables holding key components for the engine
    print('# initialize compoent variables')
    # assign subconsoles and set dimensions
    con = libtcod.console_new(screen_width, screen_height)
    bars = libtcod.console_new(bars_width, bars_height)
    msgs = libtcod.console_new(msg_width, msg_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    msg_log = MessageLog(msg_x, msg_width, msg_height)
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    game_state = GameStates.PLAYERS_TURN
    print('# components initialized')

    # initialize root console
    libtcod.console_init_root(screen_width, screen_height, 'pyrl', False)


    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # check if the fov needs to be updated
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # renders entities to the screen
        render_all(con, bars, msgs, entities, player, game_map, fov_map, fov_recompute, msg_log, screen_width, screen_height, bars_width, bars_height, bars_y, msg_width, msg_height, msg_y, mouse, colors)

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

        player_turn_results = []

        # handle the player's turn
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

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

        # process the results of the player's turn
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                msg_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)

                else:
                    message = kill_monster(dead_entity)

                msg_log.add_message(message)

        # handle the enemies turns
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            msg_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)

                            else:
                                message = kill_monster(dead_entity)

                            msg_log.add_message(message)

                            # break statement prevents the engine from changing the state back to player turn
                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                # after processing enemies, return game state to player's turn
                game_state = GameStates.PLAYERS_TURN
                print('# enemy turns complete')

if __name__ == '__main__':
    main()
