import classNames from 'classnames';
import React from 'react';

import './shape.css';


function Shape({coords, terrain, onHover, className}) {
    return Array.from(coords).map(coord => {
        const placement = {
            gridColumn: `${coord.x + 1} / span 1`,
            gridRow: `${coord.y + 1} / span 1`,
        };
        return (
            <div
                key={coord.flat()}
                className={className}
                styleName={classNames('shape', terrain ? `terrain--${terrain}` : '')}
                style={placement}
                onMouseOver={() => onHover([coord.x, coord.y])}
            ></div>
        );
    });
}

export default Shape;
