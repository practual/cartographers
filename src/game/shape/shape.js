import classNames from 'classnames';
import React from 'react';

import Terrain from '../terrain/terrain';


function Shape({coords, terrain, onHover, onClick, className}) {
    return Array.from(coords).map(coord => {
        return (
            <Terrain
                key={coord.flat()}
                coords={coord}
                terrain={terrain}
                className={className}
                onMouseOver={() => onHover && onHover([coord.x, coord.y])}
                onClick={() => onClick && onClick([coord.x, coord.y])}
            />
        );
    });
}

export default Shape;
