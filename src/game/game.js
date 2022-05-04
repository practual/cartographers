import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

import ReadyPlayers from '../ready-players';
import socket from '../socket';
import ActiveGame from './active-game';
import Results from './results';


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
    } else if (gameState.season <= 4) {
        return <ActiveGame game={gameState} />;
    } else {
        return <Results game={gameState} />;
    }
}
