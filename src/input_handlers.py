import tcod as libtcod
from src.game_states import GameStates

# main key handler
def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}

    # game controls
    if key_char == 'g' or key_char == ',':
        return {'pickup': True}

    # toggle inventory
    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    # toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # if no key was pressed
    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}

def handle_inventory_keys(key):
    # turn the list of keys associated with items into an index starting with 'a'
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

# controls the keys used on the main menu screen
def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'n':
        return {'new_game': True}

    elif key_char == 'c':
        return {'load_game': True}

    elif key_char == 'q' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
