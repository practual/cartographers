import React from 'react';

import {CoordinateSet} from '../coords';
import ShapeGrid from '../shape/shape-grid';

import styles from './exploration.css';


function Exploration({exploration}) {
    return (
        <div>
            <h2>{exploration.name}</h2>
            {exploration.coords && (
                <ShapeGrid
                    coords={CoordinateSet.fromArray(exploration.coords)}
                    expand={false}
                    shapeClassName={styles.shape}
                />
            )}
            <div styleName="options">
                {exploration.options.map(option => (
                    <ShapeGrid
                        coords={CoordinateSet.fromArray([[0, 0]])}
                        expand={false}
                        shapeClassName={styles.shape}
                        terrain={option.terrain}
                    />
                ))}
            </div>
        </div>
    );
}

export default Exploration;
