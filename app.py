from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

import serializer
from cache import cache
from game import add_player, create_game, place_shape_on_sheet, toggle_player_ready


app = Flask(__name__)
socketio = SocketIO(app, path='/api/socket.io', json=serializer)


@app.route('/<string:game_id>/<string:player_id>')
@app.route('/<string:game_id>')
@app.route('/')
def index(**kwargs):
    return render_template('index.html')


@app.route('/api/game', methods=['POST'])
def start_game():
    num_players = int(request.args.get('players', 1))
    game = create_game()
    cache.set(game['game_id'], game)
    return game['game_id'], 201


@app.route('/api/game/<string:game_id>')
def get_game(game_id):
    return cache.get(game_id)


@socketio.on('add_player')
def create_player(game_id, name):
    game, cas = cache.gets(game_id)
    game, player_id = add_player(game, name)
    cache.cas(game_id, game, cas)
    emit('game_state', game, broadcast=True)
    return player_id


@socketio.on('ready_player')
def ready_player(game_id, player_id):
    game, cas = cache.gets(game_id)
    game = toggle_player_ready(game, player_id)
    cache.cas(game_id, game, cas)
    emit('game_state', game, broadcast=True)


@socketio.on('place_shape')
def place_shape(game_id, player_id, exploration_option, shape_coords):
    game, cas = cache.gets(game_id)
    game = place_shape_on_sheet(game, player_id, exploration_option['terrain'], shape_coords)
    cache.cas(game_id, game, cas)
    emit('game_state', game, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
