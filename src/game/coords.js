export class Coordinate {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    add(other) {
        return new Coordinate(this.x + other.x, this.y + other.y);
    }

    subtract(other) {
        return new Coordinate(this.x - other.x, this.y - other.y);
    }

    flat() {
        return this.x * 11 + this.y;
    }

    toArray() {
        return [this.x, this.y];
    }
}
Coordinate.fromArray = function(coords) {
    return new Coordinate(...coords);
};
Coordinate.fromFlat = function(flat) {
    const y = flat % 11;
    const x = (flat - y) / 11;
    return new Coordinate(x, y);
};


export class CoordinateSet {
    constructor() {
        this.flatSet = new Set();
    }

    add(coordinate) {
        this.flatSet.add(coordinate.flat());
    }

    has(coordinate) {
        return this.flatSet.has(coordinate.flat());
    }

    *[Symbol.iterator]() {
        for (const flatCoord of this.flatSet) {
            yield Coordinate.fromFlat(flatCoord);
        }
    }

    toArray() {
        return Array.from(this).map(coord => coord.toArray());
    }
}
CoordinateSet.fromArray = function(coords) {
    const cs = new CoordinateSet();
    for (const coord of coords) {
        cs.add(new Coordinate(...coord));
    }
    return cs;
};


export function rotateCoord(coord, rotation) {
    switch (rotation) {
        case 0:
            return coord;
        case 1:
            return new Coordinate(-coord.y, coord.x);
        case 2:
            return new Coordinate(-coord.x, -coord.y);
        case 3:
            return new Coordinate(coord.y, -coord.x);
        case 4:
            return new Coordinate(coord.y, coord.x);
    }
}

export function rotateSet(coordSet, rotation) {
    let minX = Infinity;
    let minY = Infinity;
    const rotatedSet = new CoordinateSet();
    for (const coord of coordSet) {
        const rotatedCoord = rotateCoord(coord, rotation);
        minX = Math.min(minX, rotatedCoord.x);
        minY = Math.min(minY, rotatedCoord.y);
        rotatedSet.add(rotatedCoord);
    }
    const adjustment = new Coordinate(-minX, -minY);
    const normalisedSet = new CoordinateSet();
    for (const coord of rotatedSet) {
        normalisedSet.add(coord.add(adjustment));
    }
    return normalisedSet;
}
