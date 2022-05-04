import React from 'react';

import Sheet from './sheet/sheet';


function Results({game}) {
    const playerScores = Object.entries(game.players).map(([playerId, playerDetails]) => ({
        playerId,
        score: playerDetails.scores.reduce((acc, scoreCard) => acc + scoreCard.first + scoreCard.second, 0),
    })).sort((a, b) => a.score > b.score);

    return (
        <div>
            {playerScores.map(({playerId, score}) => (
                <React.Fragment key={playerId}>
                    <Sheet terrain={game.sheets[playerId]} />
                    <div>
                        {game.players[playerId].scores.map((scoreCard, idx) => (
                            <div key={idx}>
                                First: {scoreCard.first}, Second: {scoreCard.second}
                            </div>
                        ))}
                        <div>Total: {score}</div>
                    </div>
                </React.Fragment>
            ))}
        </div>
    );
}

export default Results;
