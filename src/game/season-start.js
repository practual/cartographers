import React, {useEffect, useState} from 'react';


function SeasonStart({season, onEnd}) {
    const [numPips, setNumPips] = useState(0);
    useEffect(() => {
        const countdown = setTimeout(() => {
            if (numPips === 2) {
                onEnd();
                return;
            } else {
                setNumPips(numPips + 1);
            }
        }, 1000);
        return () => clearTimeout(countdown);
    });

    return (
        <>
            <h1>{season.name} starting</h1>
            {3 - numPips}...
        </>
    );
}

export default SeasonStart;
