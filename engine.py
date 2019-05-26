# IMPORT STATEMENTS
print('# running imports')
import tcod as libtcod

from src.input_handlers import handle_keys
print('# imports completed')

# MAIN GAME LOOP
print('# starting main')
def main():
    print('# initializing variables')
    screen_width = 120
    screen_height = 70
    print('# variables initialized')

    # store player location and set to center of screen
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # assign font
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # variables to hold keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # initialize root console
    libtcod.console_init_root(screen_width, screen_height, 'pyrl', False)

    con = libtcod.console_new(screen_width, screen_height)

    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # set variables for root console (console printing to, color)
        libtcod.console_set_default_foreground(con, libtcod.white)
        # (console printing to, x coord, y coord, symbol to use, background color)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        # draws everything to screen
        libtcod.console_flush()
        # puts an empty space where the player used to be
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)


        # listen for keypresses
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
