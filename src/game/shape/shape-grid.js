import React from 'react';

import Shape from './shape';

import './shape-grid.css';


function ShapeGrid({coords, expand, terrain, shapeClassName}) {
    let numCols = 0;
    let numRows = 0;
    Array.from(coords).forEach(coord => {
        numCols = Math.max(numCols, coord.x + 1);
        numRows = Math.max(numRows, coord.y + 1);
    });
    let itemSize;
    if (expand) {
        // The grid will expand to fit its container. Therefore
        // the grid items should be evenly distributed.
        itemSize = '1fr';
    } else {
        // The grid size will be determined by the item size.
        itemSize = 'min-content';
    }
    return (
        <div styleName="shape-grid" style={{
            gridTemplateColumns: `repeat(${numCols}, ${itemSize})`,
            gridTemplateRows: `repeat(${numRows}, ${itemSize})`,
        }}>
            <Shape coords={coords} terrain={terrain} className={shapeClassName} />
        </div>
    );
}

export default ShapeGrid;
