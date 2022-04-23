import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';


export default function Home(props) {
    const [numPlayers, setNumPlayers] = useState(1);
    const navigate = useNavigate();

    function createGame() {
        const search = new URLSearchParams({players: numPlayers}).toString();
        fetch(`/api/game?${search}`, {method: 'POST'}).then(response => response.text()).then(gameId => {
            navigate(gameId);
        });
    }

    return (
        <div>
            <label>
                Number of players:
                <input type="number" value={numPlayers} onChange={ev => setNumPlayers(ev.target.value)} />
            </label>
            <button onClick={createGame}>Create game</button>
        </div>
    );
}
