import os
import random
from uuid import uuid4


EXPLORATIONS = [{
    'name': 'Orchard',
    'coords': {(0, 0), (1, 0), (2, 0), (2, 1)},
    'options': [{
        'terrain': 'forest',
    }, {
        'terrain': 'farm',
    }],
}]


def update_log(game_id, action, data):
    with open(os.path.join('./log', game_id), 'a+') as game_log:
        game_log.write(action + '\n')
        game_log.write(str(data) + '\n')


def create_game():
    game_id = str(uuid4())
    update_log(game_id, 'CREATE', {'game_id': game_id})
    return {
        'game_id': game_id
    }


def add_player(game, name):
    player_id = str(uuid4())
    update_log(game['game_id'], 'ADD PLAYER', {'id': player_id, 'name': name})
    if 'players' not in game:
        game['players'] = []
    game['players'].append({
        'id': player_id,
        'name': name,
    })
    return game


def toggle_player_ready(game, player_id):
    update_log(game['game_id'], 'READY PLAYER', {'id': player_id})
    all_players_ready = True
    for player in game['players']:
        if player['id'] == player_id:
            player['ready'] = not player.get('ready')
        if not player.get('ready'):
            all_players_ready = False
    if all_players_ready:
        game = start_game(game)
    return game


def start_game(game):
    game['season'] = 1
    random.shuffle(EXPLORATIONS)
    game['explorations'] = [EXPLORATIONS[0]]
    game['sheets'] = {player['id']: [] for player in game['players']}
    return game


def place_shape_on_sheet(game, player_id, terrain, coords):
    for coord in coords:
        game['sheets'][player_id].append({'coords': coord, 'terrain': terrain})
    return game
