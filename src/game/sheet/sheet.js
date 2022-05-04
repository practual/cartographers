import React, {useState} from 'react';

import {Coordinate} from '../coords';
import Terrain from '../terrain/terrain';

import './sheet.css';


function Sheet({terrain, onHover, onClick, children}) {
    const spaces = [];
    for (let y = 0; y < 11; y++) {
        for (let x = 0; x < 11; x++) {
            const placement = {
                gridColumn: `${x + 1} / span 1`,
                gridRow: `${y + 1} / span 1`,
            };
            spaces.push(
                <div
                    key={[x, y]}
                    styleName="space"
                    style={placement}
                    onMouseOver={() => onHover([x, y])}
                    onClick={() => onClick([x, y])}
                />
            );
        }
    }

    return (
        <div styleName="sheet">
            {spaces}
            {terrain.map(terrainConfig => {
                const coords = new Coordinate(...terrainConfig.coords);
                return (
                    <Terrain
                        key={coords.flat()}
                        coords={coords}
                        terrain={terrainConfig.terrain}
                        onMouseOver={() => onHover(coords.toArray())}
                        onClick={(() => onClick(coords.toArray()))}
                    />
                );
            })}
            {React.Children.map(children, child => React.cloneElement(child, {
                onHover,
                onClick,
            }))}
        </div>
    );
}

export default Sheet;
