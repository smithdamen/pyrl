# IMPORT STATEMENTS
print('# running imports')
# import system files
import tcod as libtcod
print('# system files imported')

# import engine files
from src.death import kill_monster, kill_player
from src.entity import get_blocking_entities_at_location
from src.fov import initialize_fov, recompute_fov
from src.messages import Message
from src.game_states import GameStates
from src.input_handlers import handle_keys, handle_mouse, handle_main_menu
from data.init_game import get_constants, get_game_variables
from src.data_loaders import load_game, save_game
from src.menus import main_menu, message_box
from src.render_functions import clear_all, render_all 
from data.colors import Colors

print('# imports completed')


# MAIN FUNCTION THAT SETS UP THE GAME AND STARTS THE GAME LOOP
print('# starting main')
def main():
    # import game data and set variables
    constants = get_constants()

    # assign font
    libtcod.console_set_custom_font(constants['game_font'], libtcod.FONT_LAYOUT_CP437)

    # initialize root console
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    # assign subconsoles and set dimensions
    con = libtcod.console_new(constants['map_width'], constants['map_height'])
    bars = libtcod.console_new(constants['bars_width'], constants['bars_height'])
    msgs = libtcod.console_new(constants['msg_width'], constants['msg_height'])

    player = None
    entities = []
    game_map = None
    msg_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.jpg')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save to load.', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False

            elif new_game:
                player, entities, game_map, msg_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False

            elif load_saved_game:
                try:
                    player, entities, game_map, msg_log, game_state = load_game()
                    
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            
            elif exit_game:
                break


        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, msg_log, game_state, con, bars, constants)

            show_main_menu = True


# MAIN GAME LOOP
def play_game(player, entities, game_map, msg_log, game_state, con, bars, constants):
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    
    targeting_item = None

    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # check if the fov needs to be updated
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])

        # renders entities to the screen
        render_all(con, bars, msgs, entities, player, game_map, fov_map, fov_recompute, msg_log, constants['screen_width'], constants['screen_height'], constants['map_width'], constants['map_height'], constants['bars_width'], constants['bars_height'], constants['map_x'], constants['map_y'], constants['bars_y'], constants['msg_width'], constants['msg_height'], constants['msg_y'], mouse, constants['colors'], game_state)

        #after rendering, tell loop it no longer needs to recompute the FOV
        fov_recompute = False

        libtcod.console_flush()

        # clears entities from screen when they move or are destroyed
        clear_all(con, entities)

        # listen for keypresses
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)
        
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

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

        # handle results of adding items to inventory
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                msg_log.add_message(Message('Nothing to pick up.', libtcod.yellow))

        # set game state when player shows inventory
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # set game state when player wants to drop items
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # use item when player selects it from the inventory
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # set up using the mouse for targeting
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        # set game state back to player turn when closing a menu
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, msg_log, game_state)

                return True

        # set console to fullscreen mode if pressing the correct keybinding
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # process the results of the player's turn
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('used')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')

            if message:
                msg_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                msg_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            # using an item takes a turn
            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting
                msg_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                msg_log.add_message(Message('Targeting cancelled.'))

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
