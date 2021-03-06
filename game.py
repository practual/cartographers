import os
import random
from uuid import uuid4


SEASONS = [{
    'name': 'Spring',
    'time': 8,
}, {
    'name': 'Summer',
    'time': 8,
}, {
    'name': 'Fall',
    'time': 7,
}, {
    'name': 'Winter',
    'time': 6,
}]

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


def _make_coord_adjacents(coord):
    adjacents = set()
    x, y = coord
    if x > 0:
        adjacents.add((x - 1, y))
    if y > 0:
        adjacents.add((x, y - 1))
    if x < 10:
        adjacents.add((x + 1, y))
    if y < 10:
        adjacents.add((x, y + 1))
    return adjacents


def sentinel_wood(coords_to_terrain, terrain_to_coords):
    score = 0
    for col in range(11):
        if coords_to_terrain.get((col, 0)) == 'forest':
            score += 1
        if coords_to_terrain.get((col, 10)) == 'forest':
            score += 1
    for row in range(11):
        if coords_to_terrain.get((0, row)) == 'forest':
            score += 1
        if coords_to_terrain.get((10, row)) == 'forest':
            score += 1
    return score


def greenbough(coords_to_terrain, terrain_to_coords):
    rows = set()
    cols = set()
    for forest_space in terrain_to_coords['forest']:
        cols.add(forest_space[0])
        rows.add(forest_space[1])
    return len(cols) + len(rows)


def treetower(coords_to_terrain, terrain_to_coords):
    score = 0
    for forest_space in terrain_to_coords['forest']:
        surrounded = True
        for adjacent in _make_coord_adjacents(forest_space):
            if adjacent not in coords_to_terrain:
                surrounded = False
        if surrounded:
            score += 1
    return score


def _stoneside_forest_find_mountain(coords_to_terrain, coord, checked_coords):
    found_mountain = False
    for adjacent in _make_coord_adjacents(coord):
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == 'mountain':
            return True
        if coords_to_terrain[adjacent] == 'forest':
            found_mountain = (
                found_mountain or
                _stoneside_forest_find_mountain(coords_to_terrain, adjacent, checked_coords)
            )
    return found_mountain


def stoneside_forest(coords_to_terrain, terrain_to_coords):
    score = 0
    for mountain_space in terrain_to_coords['mountain']:
        checked_coords = {mountain_space}
        if _stoneside_forest_find_mountain(coords_to_terrain, mountain_space, checked_coords):
            score += 3
    return score


def canal_lake(coords_to_terrain, terrain_to_coords):
    score = 0
    for water_space in terrain_to_coords['water']:
        for adjacent in _make_coord_adjacents(water_space):
            if coords_to_terrain.get(adjacent) == 'farm':
                score += 1
                break
    for farm_space in terrain_to_coords['farm']:
        for adjacent in _make_coord_adjacents(farm_space):
            if coords_to_terrain.get(adjacent) == 'water':
                score += 1
                break
    return score


def mages_valley(coords_to_terrain, terrain_to_coords):
    score = 0
    for mountain_space in terrain_to_coords['mountain']:
        for adjacent in _make_coord_adjacents(mountain_space):
            if adjacent not in coords_to_terrain:
                continue
            if coords_to_terrain[adjacent] == 'water':
                score += 2
            elif coords_to_terrain[adjacent] == 'farm':
                score += 1
    return score


def the_golden_granary(coords_to_terrain, terrain_to_coords):
    # To be implemented as part of ruins
    return 0


def _shoreside_expanse_check_cluster(terrain_type, coords_to_terrain, coord, checked_coords):
    opposite_terrain = 'water' if terrain_type == 'farm' else 'farm'
    adjacent_coords = _make_coord_adjacents(coord)
    if len(adjacent_coords) < 4:
        # On the edge of the map
        return False
    not_touching_opposite = True
    for adjacent in adjacent_coords:
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == opposite_terrain:
            return False
        if coords_to_terrain[adjacent] == terrain_type:
            not_touching_opposite = (
                not_touching_opposite and
                _shoreside_expanse_check_cluster(terrain_type, coords_to_terrain, adjacent, checked_coords)
            )
    return not_touching_opposite


def shoreside_expanse(coords_to_terrain, terrain_to_coords):
    score = 0
    checked_coords = set()
    for water_space in terrain_to_coords['water']:
        if water_space in checked_coords:
            continue
        if _shoreside_expanse_check_cluster('water', coords_to_terrain, water_space, checked_coords):
            score += 3
    checked_coords = set()
    for farm_space in terrain_to_coords['farm']:
        if farm_space in checked_coords:
            continue
        if _shoreside_expanse_check_cluster('farm', coords_to_terrain, farm_space, checked_coords):
            score += 3
    return score


def _wildholds_find_cluster(coords_to_terrain, coord, checked_coords, cluster_coords):
    for adjacent in _make_coord_adjacents(coord):
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == 'village':
            cluster_coords.add(adjacent)
            _wildholds_find_cluster(coords_to_terrain, adjacent, checked_coords, cluster_coords)


def wildholds(coords_to_terrain, terrain_to_coords):
    score = 0
    checked_coords = set()
    for village_space in terrain_to_coords['village']:
        if village_space in checked_coords:
            continue
        village_cluster = {village_space}
        _wildholds_find_cluster(coords_to_terrain, village_space, checked_coords, village_cluster)
        if len(village_cluster) >= 6:
            score += 8
    return score


def _great_city_check_mountains(coords_to_terrain, coord, checked_coords, village_spaces):
    not_touching_mountain = True
    for adjacent in _make_coord_adjacents(coord):
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == 'mountain':
            return False
        elif coords_to_terrain[adjacent] == 'village':
            village_spaces.add(adjacent)
            not_touching_mountain = (
                not_touching_mountain and
                _great_city_check_mountains(coords_to_terrain, adjacent, checked_coords)
            )
    return not_touching_mountain


def great_city(coords_to_terrain, terrain_to_coords):
    village_sizes = []
    checked_coords = set()
    for village_space in terrain_to_coords['village']:
        if village_space in checked_coords:
            continue
        village_spaces = {village_space}
        if _great_city_check_mountains(coords_to_terrain, village_space, checked_coords, village_spaces):
            village_sizes.append(len(village_spaces))
    return max(village_spaces)


def _greengold_plains_count_adjacent(coords_to_terrain, coord, checked_coords, terrain_found):
    for adjacent in _make_coord_adjacents(coord):
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == 'village':
            _greengold_plains_count_adjacent(coords_to_terrain, adjacent, checked_coords, terrain_found)
        else:
            terrain_found.add(coords_to_terrain[adjacent])


def greengold_plains(coords_to_terrain, terrain_to_coords):
    score = 0
    checked_coords = set()
    for village_space in terrain_to_coords['village']:
        if village_space in checked_coords:
            continue
        terrain_found = set()
        _greengold_plains_count_adjacent(coords_to_terrain, village_space, checked_coords, terrain_found)
        if len(terrain_found) >= 3:
            score += 3
    return score


def _shieldgate_count_cluster(coords_to_terrain, coord, checked_coords, cluster_coords):
    for adjacent in _make_coord_adjacents(coord):
        if adjacent in checked_coords or adjacent not in coords_to_terrain:
            continue
        checked_coords.add(adjacent)
        if coords_to_terrain[adjacent] == 'village':
            cluster_coords.add(adjacent)
            _shieldgate_count_cluster(coords_to_terrain, adjacent, checked_coords, cluster_coords)


def shieldgate(coords_to_terrain, terrain_to_coords):
    village_cluster_sizes = []
    checked_coords = set()
    for village_space in terrain_to_coords['village']:
        if village_space in checked_coords:
            continue
        cluster_coords = set()
        _shieldgate_count_cluster(coords_to_terrain, village_space, checked_coords, cluster_coords)
        village_cluster_sizes.append(len(cluster_coords))
    village_cluster_sizes = sorted(village_cluster_sizes)
    try:
        return 2 * village_cluster_sizes[1]
    except IndexError:
        return 0


def borderlands(coords_to_terrain, terrain_to_coords):
    filled_coords = set(coords_to_terrain.keys())
    score = 0
    for row in range(11):
        row_coords = {(x, row) for x in range(11)}
        if not len(row_coords - filled_coords):
            score += 6
    for col in range(11):
        col_coords = {(col, y) for y in range(11)}
        if not len(col_coords - filled_coords):
            score += 6
    return score


def lost_barony(coords_to_terrain, terrain_to_coords):
    biggest_squares = {}
    for y in range(11):
        for x in range(11):
            if not x or not y:
                biggest_squares[(x, y)] = int(bool(coords_to_terrain.get((x, y))))
            elif not coords_to_terrain.get((x, y)):
                biggest_squares[(x, y)] = 0
            else:
                biggest_squares[(x, y)] = min(
                    biggest_squares[(x - 1, y)],
                    biggest_squares[(x, y - 1)],
                    biggest_squares[(x - 1, y - 1)]
                ) + 1
    return max(biggest_squares.values()) * 3


def the_broken_road(coords_to_terrain, terrain_to_coords):
    score = 0
    for i in range(11):
        for j in range(11 - i):
            if (j, i + j) not in coords_to_terrain:
                break
        score += 3
    return score


def the_cauldrons(coords_to_terrain, terrain_to_coords):
    score = 0
    all_spaces = {(x, y) for x in range(11) for y in range(11)}
    empty_spaces = all_spaces - set(coords_to_terrain.keys())
    for empty_space in empty_spaces:
        surrounded = True
        for adjacent in _make_coord_adjacents(empty_space):
            if adjacent not in coords_to_terrain:
                surrounded = False
        if surrounded:
            score += 1
    return score


SCORING = {
    0: {
        26: {
            'name': 'Sentinel Wood',
            'description': 'Earn one reputation star for each forest space adjacent '
                'to the edge of the map.',
            'eval': sentinel_wood,
        },
        27: {
            'name': 'Greenbough',
            'description': 'Earn one reputation star for each row and column with at '
                'least one forest space. The same forest space may be scored in a row and a column.',
            'eval': greenbough,
        },
        28: {
            'name': 'Treetower',
            'description': 'Earn one reputation star for each forest space surrounded on all '
                'four sides by filled spaces or the edge of the map.',
            'eval': treetower,
        },
        29: {
            'name': 'Stoneside Forest',
            'description': 'Earn three reputation stars for each mountain space connected '
                'to another mountain space by a cluster of forest spaces.',
            'eval': stoneside_forest,
        },
    },
    1: {
        30: {
            'name': 'Canal Lake',
            'description': 'Earn one reputation star for each water space adjacent to at least '
                'one farm space. Earn one reputation star for each farm space adjacent to at '
                'least one water space.',
            'eval': canal_lake,
        },
        31: {
            'name': 'Mages Valley',
            'description': 'Earn two reputation stars for each water space adjacent to a mountain '
                'space. Earn one reputation star for each farm space adjacent to a mountain space.',
            'eval': mages_valley,
        },
        # 32: {
        #     'name': 'The Golden Granary',
        #     'description': 'Earn one reputation star for each water space adjacent to a ruins space. '
        #         'Earn three reputation stars for each farm space on a ruins space.',
        #     'eval': the_golden_granary,
        # },
        33: {
            'name': 'Shoreside Expanse',
            'description': 'Earn three reputation stars for each cluster of farm spaces not adjacent '
                'to a water space or the edge of the map. Earn three reputation stars for each '
                'cluster of water spaces not adjacent to a farm space or the edge of the map.',
            'eval': shoreside_expanse,
        },
    },
    2: {
        34: {
            'name': 'Wildholds',
            'description': 'Earn eight reputation stars for each cluster of six or more village '
                'spaces.',
            'eval': wildholds,
        },
        35: {
            'name': 'Great City',
            'description': 'Earn one reputation star for each village space in the largest '
                'cluster of village spaces that is not adjacent to a mountain space.',
            'eval': great_city,
        },
        36: {
            'name': 'Greengold Plains',
            'description': 'Earn three reputation stars for each cluster of village spaces that '
                'is adjacent to three or more different terrain types.',
            'eval': greengold_plains,
        },
        37: {
            'name': 'Shieldgate',
            'description': 'Earn two reputation stars for each village space in the second '
                'largest cluster of village spaces.',
            'eval': shieldgate,
        },
    },
    3: {
        38: {
            'name': 'Borderlands',
            'description': 'Earn six reputation stars for each complete row or complete column '
                'of filled spaces.',
            'eval': borderlands,
        },
        39: {
            'name': 'Lost Barony',
            'description': 'Earn three reputation stars for each space along one edge of the '
                'largest square of filled spaces.',
            'eval': lost_barony,
        },
        40: {
            'name': 'The Broken Road',
            'description': 'Earn three reputation stars for each complete diagonal line of '
                'filled spaces that touches the left and bottom edges of the map.',
            'eval': the_broken_road,
        },
        41: {
            'name': 'The Cauldrons',
            'description': 'Earn one reputation star for each empty space surrounded on all four '
                'sides by filled spaces or the edge of the map.',
            'eval': the_cauldrons,
        },
    },
}

SCORING_ID_TO_EVAL = {
    scoring_id: scoring_card['eval']
    for scoring_details in SCORING.values()
    for scoring_id, scoring_card in scoring_details.items()
}


def update_log(game_id, action, data):
    with open(os.path.join('./log', game_id), 'a+') as game_log:
        game_log.write(action + '\n')
        game_log.write(str(data) + '\n')


def create_game(num_players):
    game_id = str(uuid4())
    update_log(game_id, 'CREATE', {'game_id': game_id})
    return {
        'game_id': game_id,
        'num_players': num_players,
        'players': {},
        'explorations': [],
        'scoring': [],
    }


def add_player(game, name):
    player_id = str(uuid4())
    update_log(game['game_id'], 'ADD PLAYER', {'id': player_id, 'name': name})
    game['players'][player_id] = {
        'id': player_id,
        'name': name,
        'ready': False,
        'num_explorations': 0,
        'scores': [],
    }
    return game, player_id


def toggle_player_ready(game, player_id):
    update_log(game['game_id'], 'READY PLAYER', {'id': player_id})
    game['players'][player_id]['ready'] = not game['players'][player_id]['ready']
    if len([player for player in game['players'].values() if player['ready']]) == game['num_players']:
        game = start_game(game)
    return game


def _advance_season(game):
    current_season_id = game.get('season', {}).get('id', -1)
    next_season_id = current_season_id + 1
    try:
        game['season'] = SEASONS[next_season_id]
        game['season']['id'] = next_season_id
    except IndexError:
        # End of the game - use a pseudo season to indicate to the client
        # that the game is over.
        game['season'] = {'id': next_season_id}
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
    scoring_types = [0, 1, 2, 3]
    random.shuffle(scoring_types)
    for i in scoring_types:
        scoring = list(SCORING[i].keys())
        random.shuffle(scoring)
        game['scoring'].append({
            'id': scoring[0],
            'name': SCORING[i][scoring[0]]['name'],
            'description': SCORING[i][scoring[0]]['description'],
        })

    game = _advance_season(game)
    game = deal_exploration(game)
    game['sheets'] = {player_id: [
        {'coords': coords, 'terrain': 'mountain'} for coords in MOUNTAIN_COORDS
    ] for player_id in game['players']}
    return game


def _get_score_for_card(sheet, scoring_id):
    coords_to_terrain = {}
    terrain_to_coords = {}
    for space in sheet:
        coords_to_terrain[tuple(space['coords'])] = space['terrain']
        if space['terrain'] not in terrain_to_coords:
            terrain_to_coords[space['terrain']] = set()
        terrain_to_coords[space['terrain']].add(tuple(space['coords']))
    return SCORING_ID_TO_EVAL[scoring_id](coords_to_terrain, terrain_to_coords)


def place_shape_on_sheet(game, player_id, terrain, coords):
    current_coord_set = {
        tuple(space['coords']) for space in game['sheets'][player_id]
    }
    for coord in coords:
        if tuple(coord) in current_coord_set:
            raise ValueError('Overlapping terrain')
        game['sheets'][player_id].append({'coords': coord, 'terrain': terrain})
    game['players'][player_id]['num_explorations'] += 1

    if not all(
        player['num_explorations'] == len(game['explorations'])
        for player in game['players'].values()
    ):
        return game

    if sum(exploration['time'] for exploration in game['explorations']) < game['season']['time']:
        game = deal_exploration(game)
        return game

    for player_id in game['players']:
        game['players'][player_id]['scores'].append({
            'first': _get_score_for_card(
                game['sheets'][player_id],
                game['scoring'][game['season']['id']]['id']
            ),
            'second': _get_score_for_card(
                game['sheets'][player_id],
                game['scoring'][(game['season']['id'] + 1) % 4]['id']
            ),
            'coins': 0,
            'monsters': 0,
        })

    game = _advance_season(game)

    if game['season']['id'] < 4:
        game['explorations'] = []
        for player_id in game['players']:
            game['players'][player_id]['num_explorations'] = 0
        game = deal_exploration(game)

    return game
