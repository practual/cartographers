import React from 'react';
import {useParams} from 'react-router';

import socket from './socket';

const Player = props => {
    const params = useParams();
    const {gameId, playerId} = params;

    const emitPlayerReady = () => {
        socket.emit('ready_player', gameId, playerId);
    };

    let markReady;
    if (props.player.id === playerId) {
        markReady = (
            <button onClick={emitPlayerReady}>
                {props.player.ready ? 'Not Ready' : 'Ready'}
            </button>
        );
    }

    return (
        <li>
            {props.player.name}{' - '}
            {props.player.ready ? 'Ready' : 'Not Ready'}
            {markReady}
        </li>
    );
};

export default Player;
