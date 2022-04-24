import React, {useState} from 'react';

import {Coordinate, CoordinateSet, rotateSet} from './coords';
import Exploration from './exploration/exploration';
import Shape from './shape/shape';
import Sheet from './sheet/sheet';


const SEASON = {
    1: 'Spring',
    2: 'Summer',
    3: 'Autumn',
    4: 'Winter',
};


function ActiveGame({game}) {
    const [hoverSpace, setHoverSpace] = useState(null);
    const [rotation, setRotation] = useState(0);
    const [mirror, setMirror] = useState(0);

    let pendingShapeOffsets = new CoordinateSet();
    pendingShapeOffsets.add(new Coordinate(0, 0));
    pendingShapeOffsets.add(new Coordinate(1, 0));
    pendingShapeOffsets.add(new Coordinate(2, 0));
    pendingShapeOffsets.add(new Coordinate(2, 1));

    pendingShapeOffsets = rotateSet(pendingShapeOffsets, mirror ? 4 : 0);
    pendingShapeOffsets = rotateSet(pendingShapeOffsets, rotation);

    let pendingShapeCoords;
    if (hoverSpace) {
        pendingShapeCoords = new CoordinateSet();
        for (const coord of pendingShapeOffsets) {
            pendingShapeCoords.add(coord.add(hoverSpace));
        }
    }

    return (
        <>
            <h1>
                {SEASON[game.season]}
            </h1>
            <Exploration exploration={game.explorations[game.explorations.length - 1]} />
            <button onClick={() => setRotation((rotation + 3) % 4)}>&lt; Rotate</button>
            <button onClick={() => setRotation((rotation + 1) % 4)}>Rotate &gt;</button>
            <button onClick={() => setMirror(mirror ? 0 : 1)}>Mirror</button>
            <Sheet setHoverSpace={([x, y]) => setHoverSpace(new Coordinate(x, y))}>
                {pendingShapeCoords && <Shape coords={pendingShapeCoords} />}
            </Sheet>
        </>
    );
}

export default ActiveGame;
