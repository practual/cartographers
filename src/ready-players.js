import PropTypes from 'prop-types';
import React, {useState} from 'react';
import {useNavigate, useParams} from 'react-router-dom';

import socket from './socket';
import Player from './player';

const ReadyPlayers = props => {
    const params = useParams();
    const gameId = params.gameId;
    const playerId = params.playerId;
    const [name, setName] = useState('');
    const navigate = useNavigate();

    const addPlayer = () => {
        socket.emit('add_player', gameId, name, playerId => {
            navigate(`/${gameId}/${playerId}`);
        });
    };

    return (
        <div>
            {!playerId && (
                <div>
                    <label>
                        Your name:
                        <input type="text" value={name} onChange={ev => setName(ev.target.value)} />
                    </label>
                    <button type="submit" onClick={addPlayer}>
                        Join game
                    </button>
                </div>
            )}
            <div>
                <h2>Players</h2>
                <ul>
                    {props.players.map(
                        player => <Player key={player.id} player={player} />
                    )}
                </ul>
            </div>
        </div>
    );
};
ReadyPlayers.propTypes = {
    players: PropTypes.array,
};
ReadyPlayers.defaultProps = {
    players: [],
};

export default ReadyPlayers;
