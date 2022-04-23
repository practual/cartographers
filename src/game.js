import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

import ActiveGame from './game/active-game';
import ReadyPlayers from './ready-players';
import socket from './socket';


export default function Game(props) {
    const [isLoading, setIsLoading] = useState(true);
    const [gameState, setGameState] = useState({});
    const params = useParams();

    useEffect(() => {
        if (!isLoading) {
            return;
        }
        fetch(`/api/game/${params.gameId}`).then(response => response.json()).then(response => {
            setGameState(response);
            setIsLoading(false);
        });
    }, [isLoading]);

    useEffect(() => {
        socket.on('game_state', setGameState);
        return () => {
            socket.off('game_state', setGameState);
        };
    });

    if (isLoading) {
        return null;
    }

    if (!gameState.season) {
        return <ReadyPlayers players={gameState.players} />;
    } else {
        return <ActiveGame game={gameState} />;
    }
}
