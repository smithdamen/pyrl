# eventually move this file to data to contain each function that items can utilize
import tcod as libtcod
from src.ai import ConfusedMonster
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

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'used': True, 'target': target, 'message': Message('Lightning hits the {0} and deals {1} damage.'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'used': False, 'target': None, 'message': Message('No enemies in range.', libtcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'used': False, 'message': Message('You cannot see the target.', libtcod.yellow)})
        return results

    results.append({'used': True, 'message': Message('You burn everything within {0} tiles.'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} is burned for {1} damage.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'used': False, 'message': Message('Target outside field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)
            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'used': True, 'message': Message('{0} looks confused.'.format(entity.name), libtcod.light_green)})

            break

    else:
        results.append({'used': False, 'message': Message('No available target at that location.', libtcod.yellow)})

    return results
