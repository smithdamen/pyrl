import tcod as libtcod
from enum import Enum

# tell the renderer what order to draw tiles in
class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

# draws all the entities in the list
# takes console, map, list of entities, width and height, and colors
def render_all(con, bars, msgs, entities, player, game_map, fov_map, fov_recompute, msg_log, screen_width, screen_height, bars_width, bars_height, bars_y, msg_width, msg_height, msg_y, mouse, colors):
    if fov_recompute:
        # draw tiles in game map
        # this will eventually be moved into individual map generator files
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                # tell the renderer what to draw if the tile is visible
                if visible:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('light_wall_fg'), colors.get('light_wall_bg'))

                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                    # set tile to explored once it's been seen
                    game_map.tiles[x][y].explored = True

                # tell the renderer what to draw if tiles are not visible
                elif game_map.tiles[x][y].explored:
                    # assigns the symbol, colors, and positions of map tiles
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('dark_wall_fg'), colors.get('dark_wall_bg'))
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    # blit main console to screen
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    # set up bars subconsole
    libtcod.console_set_default_background(bars, libtcod.black)
    libtcod.console_clear(bars)

    # render the health bar
    # TODO: add mana and stamina bars here
    render_bar(bars, 1, 1, bars_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)

    # render names under the mouse and print to the bars subconsole
    libtcod.console_set_default_foreground(bars, libtcod.light_gray)
    libtcod.console_print_ex(bars, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))

    # set up msgs subconsole
    libtcod.console_set_default_background(msgs, libtcod.black)
    libtcod.console_clear(msgs)

    # print messages one line at a time
    y = 1
    for message in msg_log.messages:
        libtcod.console_set_default_foreground(msgs, message.color)
        libtcod.console_print_ex(msgs, msg_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    # blit bars console to screen
    libtcod.console_blit(bars, 0, 0, bars_width, bars_height, 0, 0, bars_y)

    # blit msgs console to screen
    libtcod.console_blit(msgs, 0, 0, msg_width, msg_height, 0, 0, msg_y)

# used to clear all entities after drawing to screen
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# does the drawing of the entities to the screen
# takes console, x and y coords, character, and color
def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# erases the character that represents this entity and makes it so it does not leave a trail when it moves
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

# use the mouse to get tooltips
def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    names = ', '.join(names)

    return names.capitalize()

# create a bar to be put in the bars section of the window
def render_bar(bars, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(bars, back_color)
    libtcod.console_rect(bars, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(bars, bar_color)

    if bar_width > 0:
        libtcod.console_rect(bars, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(bars, libtcod.white)
    libtcod.console_print_ex(bars, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
            '{0}: {1}/{2}'.format(name, value, maximum))

# create msgs window


