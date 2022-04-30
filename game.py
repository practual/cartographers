import os
import random
from uuid import uuid4


EXPLORATIONS = [{
    'id': 7,
    'name': 'Great River',
    'time': 1,
    'terrain': 'water',
    'options': [{
        'coords': {(0, 0), (0, 1), (0, 2)},
        'coin': True,
    }, {
        'coords': {(2, 0), (1, 1), (2, 1), (0, 2), (1, 2)},
    }],
}, {
    'id': 8,
    'name': 'Farmland',
    'time': 1,
    'terrain': 'farm',
    'options': [{
        'coords': {(0, 0), (0, 1)},
        'coin': True,
    }, {
        'coords': {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    }],
}, {
    'id': 9,
    'name': 'Hamlet',
    'time': 1,
    'terrain': 'village',
    'options': [{
        'coords': {(0, 0), (0, 1), (1, 1)},
        'coin': True,
    }, {
        'coords': {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)},
    }],
}, {
    'id': 10,
    'name': 'Forgotten Forest',
    'time': 1,
    'terrain': 'forest',
    'options': [{
        'coords': {(0, 0), (1, 1)},
        'coin': True,
    }, {
        'coords': {(0, 0), (0, 1), (1, 1), (1, 2)},
    }],
}, {
    'id': 11,
    'name': 'Hinterland Stream',
    'time': 2,
    'coords': {(0, 0), (1, 0), (2, 0), (0, 1), (0, 2)},
    'options': [{
        'terrain': 'farm',
    }, {
        'terrain': 'water',
    }],
}, {
    'id': 12,
    'name': 'Homestead',
    'time': 2,
    'coords': {(0, 0), (0, 1), (1, 1), (0, 2)},
    'options': [{
        'terrain': 'village',
    }, {
        'terrain': 'farm',
    }],
}, {
    'id': 13,
    'name': 'Orchard',
    'time': 2,
    'coords': {(0, 0), (1, 0), (2, 0), (2, 1)},
    'options': [{
        'terrain': 'forest',
    }, {
        'terrain': 'farm',
    }],
}, {
    'id': 14,
    'name': 'Treetop Village',
    'time': 2,
    'coords': {(2, 0), (3, 0), (0, 1), (1, 1), (2, 1)},
    'options': [{
        'terrain': 'forest',
    }, {
        'terrain': 'village',
    }],
}, {
    'id': 15,
    'name': 'Marshlands',
    'time': 2,
    'coords': {(0, 0), (0, 1), (1, 1), (2, 1), (0, 2)},
    'options': [{
        'terrain': 'forest',
    }, {
        'terrain': 'water',
    }],
}, {
    'id': 16,
    'name': 'Fishing Village',
    'time': 2,
    'coords': {(0, 0), (1, 0), (2, 0), (3, 0)},
    'options': [{
        'terrain': 'village',
    }, {
        'terrain': 'water',
    }],
}, {
    'id': 17,
    'name': 'Rift Lands',
    'time': 0,
    'coords': {(0, 0)},
    'options': [{
        'terrain': 'forest',
    }, {
        'terrain': 'village',
    }, {
        'terrain': 'farm',    
    }, {
        'terrain': 'water',    
    }, {
        'terrain': 'monster',
    }]
}]

EXPLORATIONS_BY_ID = {exploration['id']: exploration for exploration in EXPLORATIONS}

MOUNTAIN_COORDS = {(3, 1), (8, 2), (5, 5), (2, 8), (7, 9)}


def update_log(game_id, action, data):
    with open(os.path.join('./log', game_id), 'a+') as game_log:
        game_log.write(action + '\n')
        game_log.write(str(data) + '\n')


def create_game():
    game_id = str(uuid4())
    update_log(game_id, 'CREATE', {'game_id': game_id})
    return {
        'game_id': game_id,
        'players': {},
        'explorations': [],
    }


def add_player(game, name):
    player_id = str(uuid4())
    update_log(game['game_id'], 'ADD PLAYER', {'id': player_id, 'name': name})
    game['players'][player_id] = {
        'id': player_id,
        'name': name,
        'ready': False,
        'num_explorations': 0,
    }
    return game, player_id


def toggle_player_ready(game, player_id):
    update_log(game['game_id'], 'READY PLAYER', {'id': player_id})
    game['players'][player_id]['ready'] = not game['players'][player_id]['ready']
    if all(player['ready'] for p_id, player in game['players'].items()):
        game = start_game(game)
    return game


def deal_exploration(game):
    all_exploraton_ids = set(EXPLORATIONS_BY_ID.keys())
    used_exploration_ids = set(exploration['id'] for exploration in game['explorations'])
    available_exploration_ids = list(all_exploraton_ids - used_exploration_ids)
    random.shuffle(available_exploration_ids)
    next_exploration_id = available_exploration_ids[0]
    game['explorations'].append(EXPLORATIONS_BY_ID[next_exploration_id])
    return game


def start_game(game):
    game['season'] = 1
    game = deal_exploration(game)
    game['sheets'] = {player_id: [
        {'coords': coords, 'terrain': 'mountain'} for coords in MOUNTAIN_COORDS
    ] for player_id in game['players']}
    return game


def place_shape_on_sheet(game, player_id, terrain, coords):
    for coord in coords:
        game['sheets'][player_id].append({'coords': coord, 'terrain': terrain})
    game['players'][player_id]['num_explorations'] += 1
    if all(
        player['num_explorations'] == len(game['explorations'])
        for player in game['players'].values()
    ):
        game = deal_exploration(game)
    return game
