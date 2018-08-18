def action(name, texture, repeats, duration, actions, conditions):
    action = dict()
    action['name'] = name
    action['texture'] = texture
    action['repeats'] = repeats
    action['performed'] = 0
    action['duration'] = duration
    for i in range(len(actions)):
        if actions[i][0] != 'loot' and len(actions[i]) == 3:
            actions[i] = (*actions[i], 0)
    action['actions'] = actions
    action['conditions'] = conditions
    return action

x = dict()
x['grass'] = dict()
x['grass']['walken'] = 1
x['grass']['actions'] = []
x['grass']['actions'].append(action(name = 'findsticks', texture = 'resources/actions/findsticks.png', repeats = 2, duration = 2, actions = [('give', 'sticks', 3, -2)], conditions = []))
x['grass']['actions'].append(action(name = 'findrocks', texture = 'resources/actions/findrocks.png', repeats = 2, duration = 2, actions = [('give', 'rocks', 3, -2)], conditions = []))
x['tree'] = dict()
x['tree']['walken'] = 2
x['tree']['health'] = 100
x['tree']['death_voice'] = dict()
x['tree']['death_voice']['turninto'] = 'log'
x['tree']['death_voice']['loot'] = [('sticks', 10)]
x['tree']['actions'] = []
x['tree']['actions'].append(action(name = 'findsticks', texture = 'resources/actions/findsticks.png', repeats = 2, duration = 2, actions = [('give', 'sticks', 3, -2)], conditions = []))
x['tree']['actions'].append(action(name = 'findrocks', texture = 'resources/actions/findrocks.png', repeats = 2, duration = 2, actions = [('give', 'rocks', 3, -2)], conditions = []))
x['tree']['actions'].append(action(name = 'cuttree', texture = 'resources/actions/cuttree.png', repeats = 100, duration = 1,
                                   actions = [('break', 'wooden_axe', -10), ('damage', 5, -20)], conditions = [('have', 'wooden_axe', 1)]))
x['bush'] = dict()
x['bush']['walken'] = 3
x['bush']['actions'] = []
x['bush']['actions'].append(action(name = 'findsticks', texture = 'resources/actions/findsticks.png', repeats = 2, duration = 2, actions = [('give', 'sticks', 3, -2)], conditions = []))
x['bush']['actions'].append(action(name = 'findfood', texture = 'resources/actions/findfood.png', repeats = 2, duration = 3, actions = [('give', 'food', 3, -2)], conditions = []))
x['log'] = dict()
x['log']['walken'] = 2
x['log']['health'] = 100
x['log']['death_voice'] = dict()
x['log']['death_voice']['turninto'] = 'grass'
x['log']['death_voice']['loot'] = []
x['log']['actions'] = []
x['log']['actions'].append(action(name = 'findsticks', texture = 'resources/actions/findsticks.png', repeats = 2, duration = 2, actions = [('give', 'sticks', 3, -2)], conditions = []))
x['log']['actions'].append(action(name = 'cutlog', texture = 'resources/actions/cuttree.png', repeats = 100, duration = 2,
                                   actions = [('break', 'wooden_axe', -10), ('damage', 5, -10)], conditions = [('have', 'wooden_axe', 1)]))

import json
with open('resources/cells/properties.json', 'w') as f:
    json.dump(x, f)