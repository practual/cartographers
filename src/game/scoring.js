import React from 'react';


function Scoring({scoringData, onClose}) {
    return (
        <>
            <h1>Scorecards</h1>
            {scoringData.map(scoring => (
                <div key={scoring.id}>
                    <h2>{scoring.name}</h2>
                    <p>{scoring.description}</p>
                </div>
            ))}
            <button onClick={onClose}>Close</button>
        </>
    );
}

export default Scoring;
