import React from 'react';


function Scoring({scoringData, onClose}) {
    const cardLabels = ['A', 'B', 'C', 'D'];

    return (
        <>
            <h1>Scorecards</h1>
            {scoringData.map((scoring, idx) => (
                <div key={scoring.id}>
                    <h2>{cardLabels[idx]}: {scoring.name}</h2>
                    <p>{scoring.description}</p>
                </div>
            ))}
            <button onClick={onClose}>Close</button>
        </>
    );
}

export default Scoring;
