import classNames from 'classnames';
import React from 'react';

import './terrain.css';


function Terrain({coords, terrain, className, ...props}) {
    const placement = {
        gridColumn: `${coords.x + 1} / span 1`,
        gridRow: `${coords.y + 1} / span 1`,
    };
    return (
        <div
            styleName={classNames('terrain', terrain ? `terrain--${terrain}` : '')}
            style={placement}
            className={className}
            {...props}
        ></div>
    );
}

export default Terrain;
