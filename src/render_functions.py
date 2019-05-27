import tcod as libtcod
from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

# draws all the entities in the list
# takes console, map, list of entities, width and height, and colors
def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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

    # draw temporary health bar
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                         'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

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

