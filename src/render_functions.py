import tcod as libtcod

# draws all the entities in the list
# takes console, map, list of entities, width and height, and colors
def render_all(con, entities, game_map, screen_width, screen_height, colors):
    # draw tiles in game map
    # this will eventually be moved into individual map generator files
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            # assigns the symbol, colors, and positions of map tiles
            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# used to clear all entities after drawing to screen
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# does the drawing of the entities to the screen
# takes console, x and y coords, character, and color
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# erases the character that represents this entity and makes it so it does not leave a trail when it moves
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

