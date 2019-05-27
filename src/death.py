import tcod as libtcod
from src.game_states import GameStates
from src.render_functions import RenderOrder
from src.messages import Message

def kill_player(player):
    # eventually move player character and color to main config file
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died', libtcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message('{0} is dead.'.format(monster.name.capitalize()), libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'corpse of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
