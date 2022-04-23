from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from cache import cache
from game import add_player, create_game, toggle_player_ready


app = Flask(__name__)
socketio = SocketIO(app, path='/api/socket.io')


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
    game = add_player(game, name)
    cache.cas(game_id, game, cas)
    emit('game_state', game, broadcast=True)
    return game['players'][-1]['id']


@socketio.on('ready_player')
def ready_player(game_id, player_id):
    game, cas = cache.gets(game_id)
    game = toggle_player_ready(game, player_id)
    cache.cas(game_id, game, cas)
    emit('game_state', game, broadcast=True)


@socketio.on('use_action')
def action(game_id, player_id, action_id, data):
    game_state, cas = cache.gets(game_id)
    game = Game.deserialize(game_state, update_log)
    game.use_action(action_id, data)
    game_state = game.serialize()
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
