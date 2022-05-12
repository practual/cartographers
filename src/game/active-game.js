import React, {useState} from 'react';
import {useParams} from 'react-router-dom';

import socket from '../socket';
import {Coordinate, CoordinateSet, rotateSet} from './coords';
import Exploration from './exploration/exploration';
import Sheet from './sheet/sheet';
import Terrain from './terrain/terrain';


function ActiveGame({game}) {
    const [pendingShape, setPendingShape] = useState(null);
    const [hoverSpace, setHoverSpace] = useState(null);
    const [rotation, setRotation] = useState(0);
    const [mirror, setMirror] = useState(0);
    const {gameId, playerId} = useParams();

    const onPlacePendingShape = () => {
        socket.emit('place_shape', gameId, playerId, pendingShape, pendingShapeCoords.toArray());
        setPendingShape(null);
        setRotation(0);
        setMirror(0);
    };

    let pendingShapeCoords;
    if (pendingShape && hoverSpace) {
        let pendingShapeOffsets = CoordinateSet.fromArray(pendingShape.coords);
        pendingShapeOffsets = rotateSet(pendingShapeOffsets, mirror ? 4 : 0);
        pendingShapeOffsets = rotateSet(pendingShapeOffsets, rotation);

        pendingShapeCoords = new CoordinateSet();
        for (const coord of pendingShapeOffsets) {
            pendingShapeCoords.add(coord.add(hoverSpace));
        }
    }

    return (
        <>
            <dl>
                {game.scoring.map(scoring => (
                    <React.Fragment key={scoring.id}>
                        <dt>{scoring.name}</dt>
                        <dd>{scoring.description}</dd>
                    </React.Fragment>
                ))}
            </dl>
            <h1>
                {game.season.name} ({game.explorations.reduce((acc, el) => acc + el.time, 0)} of {game.season.time})
            </h1>
            <Exploration
                exploration={game.explorations[game.explorations.length - 1]}
                onSelectOption={setPendingShape}
            />
            <button onClick={() => setRotation((rotation + 3) % 4)}>&lt; Rotate</button>
            <button onClick={() => setRotation((rotation + 1) % 4)}>Rotate &gt;</button>
            <button onClick={() => setMirror(mirror ? 0 : 1)}>Mirror</button>
            {pendingShapeCoords && <button onClick={onPlacePendingShape}>Confirm</button>}
            <Sheet
                terrain={game.sheets[playerId]}
                onMove={([x, y]) => setHoverSpace(new Coordinate(x, y))}
            >
                {pendingShapeCoords && Array.from(pendingShapeCoords).map(coord => (
                    <Terrain
                        key={coord.flat()}
                        coords={coord}
                        terrain={pendingShape.terrain}
                    />
                ))}
            </Sheet>
            <div>
                {game.players[playerId].scores.map((scoreCard, idx) => (
                    <div key={idx}>
                        First: {scoreCard.first}, Second: {scoreCard.second}
                    </div>
                ))}
            </div>
        </>
    );
}

export default ActiveGame;
