import React, {useState} from 'react';

import './sheet.css';


function Sheet({setHoverSpace, children}) {
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
                    onMouseOver={() => setHoverSpace([x, y])}
                />
            );
        }
    }

    return (
        <div styleName="sheet">
            {spaces}
            {React.Children.map(children, child => React.cloneElement(child, {
                onHover: setHoverSpace,
            }))}
        </div>
    );
}

export default Sheet;
