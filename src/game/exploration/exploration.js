import React from 'react';

import {CoordinateSet} from '../coords';
import ShapeGrid from '../shape/shape-grid';
import Terrain from '../terrain/terrain';

import styles from './exploration.css';


function Exploration({exploration, onSelectOption}) {
    return (
        <div>
            <h2>{exploration.name}</h2>
            {exploration.terrain && (
                <Terrain terrain={exploration.terrain} styleName="terrain" />
            )}
            {exploration.coords && (
                <ShapeGrid
                    coords={CoordinateSet.fromArray(exploration.coords)}
                    expand={false}
                    shapeClassName={styles.terrain}
                />
            )}
            <div styleName="options">
                {exploration.options.map((option, idx) => (
                    <div
                        key={idx}
                        onClick={() => onSelectOption({
                            'coords': option.coords || exploration.coords,
                            'terrain': option.terrain || exploration.terrain,
                        })}
                    >
                        {option.coords ? (
                            <ShapeGrid
                                key={idx}
                                coords={CoordinateSet.fromArray(option.coords)}
                                expand={false}
                                shapeClassName={styles.terrain}
                                terrain={option.terrain}
                            />
                        ) : <Terrain key={idx} styleName="terrain" />}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Exploration;
