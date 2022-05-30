import React, {useEffect, useState} from 'react';
import * as ReactDOM from 'react-dom/client';
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import Game from './game/game';
import Home from './home';

import './global.css';
import styles from './index.css';
import socket from './socket';


const App = () => {
    const [socketLog, setSocketLog] = useState('');

    useEffect(() => {
        socket.on('connect', () => setSocketLog(socketLog + 'connect ' + socket.io.engine.transport.name + '\n'));
        socket.io.engine.on('upgrade', () => setSocketLog(socketLog + 'upgrade\n'));
        socket.on('connect_error', () => setSocketLog(socketLog + 'connect_error\n'));
        socket.on('disconnect', () => setSocketLog(socketLog + 'disconnect\n'));
    });
    return (
    <div>
        {socketLog}
        <BrowserRouter>
            <Routes>
                <Route path=":gameId" element={<Game />} />
                <Route path=":gameId/:playerId" element={<Game />} />
                <Route path="*" element={<Home />} />
            </Routes>
        </BrowserRouter>
    </div>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
