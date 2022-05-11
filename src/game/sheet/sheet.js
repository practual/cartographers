import React, {useState} from 'react';

import {Coordinate} from '../coords';
import Terrain from '../terrain/terrain';

import './sheet.css';


function getCoordsFromEvent(ev) {
    let eventDetails;
    if (ev.changedTouches) {
        eventDetails = ev.changedTouches[0];
    } else {
        eventDetails = ev;
    }
    const {clientX: targetX, clientY: targetY, target} = eventDetails;
    const {
        left: sheetX,
        top: sheetY,
        width: sheetWidth,
        height: sheetHeight,
    } = target.getBoundingClientRect();
    return [
        Math.floor((targetX - sheetX) / sheetWidth * 11),
        Math.floor((targetY - sheetY) / sheetHeight * 11),
    ];
}


function Sheet({terrain, onMove, children}) {
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
                />
            );
        }
    }

    return (
        <div styleName="sheet-outer">
            <div styleName="sheet-wrapper">
                <div styleName="sheet-inner">
                    <div
                        onClick={ev => onMove && onMove(getCoordsFromEvent(ev))}
                        onTouchStart={ev => onMove && onMove(getCoordsFromEvent(ev))}
                        onTouchMove={ev => onMove && onMove(getCoordsFromEvent(ev))}
                        styleName="sheet"
                    >
                        {spaces}
                        {terrain.map(terrainConfig => {
                            const coords = new Coordinate(...terrainConfig.coords);
                            return (
                                <Terrain
                                    key={coords.flat()}
                                    coords={coords}
                                    terrain={terrainConfig.terrain}
                                />
                            );
                        })}
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Sheet;
