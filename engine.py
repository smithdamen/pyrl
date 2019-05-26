# IMPORT STATEMENTS
print('# running imports')
import tcod as libtcod
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

    # game loop
    while not libtcod.console_is_window_closed():
        # listen for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # set variables for root console (console printing to, color)
        libtcod.console_set_default_foreground(0, libtcod.white)
        # (console printing to, x coord, y coord, symbol to use, background color)
        libtcod.console_put_char(0, player_x, player_y, '@', libtcod.BKGND_NONE)
        # draws everything to screen
        libtcod.console_flush()

        # listen for keypresses
        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True

if __name__ == '__main__':
    main()
