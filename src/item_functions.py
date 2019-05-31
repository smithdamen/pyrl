# eventually move this file to data to contain each function that items can utilize
import tcod as libtcod
from src.messages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'used': False, 'message': Message('Health is already full.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'used': True, 'message': Message('You feel better.', libtcod.green)})

    return results
