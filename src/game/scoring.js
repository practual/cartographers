import React from 'react';


function Scoring({scoringData, onClose}) {
    return (
        <>
            <dl>
                {scoringData.map(scoring => (
                    <React.Fragment key={scoring.id}>
                        <dt>{scoring.name}</dt>
                        <dd>{scoring.description}</dd>
                    </React.Fragment>
                ))}
            </dl>
            <button onClick={onClose}>Close</button>
        </>
    );
}

export default Scoring;
