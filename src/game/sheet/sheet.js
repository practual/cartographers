import React, {useState} from 'react';

import {Coordinate} from '../coords';
import Terrain from '../terrain/terrain';

import './sheet.css';


function getCoordsFromTouchEvent(ev) {
    const {clientX: touchX, clientY: touchY} = ev.changedTouches[0];
    const {
        left: sheetX,
        top: sheetY,
        width: sheetWidth,
        height: sheetHeight
    } = ev.changedTouches[0].target.getBoundingClientRect();
    return [
        Math.floor((touchX - sheetX) / sheetWidth * 11),
        Math.floor((touchY - sheetY) / sheetHeight * 11),
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
                <div
                    onTouchStart={ev => onMove && onMove(getCoordsFromTouchEvent(ev))}
                    onTouchMove={ev => onMove && onMove(getCoordsFromTouchEvent(ev))}
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
    );
}

export default Sheet;
