import React from 'react';
import * as ReactDOM from 'react-dom/client';
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import Game from './game/game';
import Home from './home';

import './global.css';
import styles from './index.css';


const App = () => (
    <div>
        <BrowserRouter>
            <Routes>
                <Route path=":gameId" element={<Game />} />
                <Route path=":gameId/:playerId" element={<Game />} />
                <Route path="*" element={<Home />} />
            </Routes>
        </BrowserRouter>
    </div>
);

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
