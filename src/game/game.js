import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

import ReadyPlayers from '../ready-players';
import socket from '../socket';
import ActiveGame from './active-game';
import {INTERSTITIAL_STATE} from './constants';
import Results from './results';
import Scoring from './scoring';
import SeasonStart from './season-start';


export default function Game(props) {
    const [isLoading, setIsLoading] = useState(true);
    const [game, setGameState] = useState({});
    const [interstitialState, setInterstitialState] = useState(INTERSTITIAL_STATE.SCORING);
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

    if (!game.season) {
        return <ReadyPlayers players={game.players} />;
    } else if (game.season.id === 4) {
        return <Results game={game} />;
    } else if (interstitialState === INTERSTITIAL_STATE.SCORING) {
        return <Scoring scoringData={game.scoring} onClose={() => setInterstitialState(INTERSTITIAL_STATE.SEASON_START)} />
    } else if (interstitialState === INTERSTITIAL_STATE.SEASON_START) {
        return <SeasonStart season={game.season} onEnd={() => setInterstitialState(INTERSTITIAL_STATE.NONE)} />
    } else {
        return <ActiveGame game={game} />;
    }
}
