import tcod as libtcod

def handle_keys(key):
    # movement keys
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}
    # TODO: change to vi-keys and add 8-directional movement

    # toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # if no key was pressed
    return {}
