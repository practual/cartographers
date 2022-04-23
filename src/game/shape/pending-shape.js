import React from 'react';

import './shape.css';


function PendingShape({coords, onHover}) {
    return Array.from(coords).map(coord => {
        const placement = {
            gridColumn: `${coord.x + 1} / span 1`,
            gridRow: `${coord.y + 1} / span 1`,
        };
        return (
            <div
                key={coord.flat()}
                styleName="shape"
                style={placement}
                onMouseOver={() => onHover([coord.x, coord.y])}
            ></div>
        );
    });
}

export default PendingShape;
