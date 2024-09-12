import './App.css';
import Chat from './Chat';
import { contains } from 'cheerio';
import { useState } from 'react';

const suggestedPrompts = [
    "How old is the university of Basel?",
    "What do i have to do to take part in the exam for dental medicine?",
];



function App() {
    const [showChat, setShow] = useState(false);
    const content =  ( <Chat /> )


    return (
        <div className="app">
            <div style={{ zIndex: -1, position: 'absolute', top: 0, right: 0, bottom: 0, width: 100 + 'vw' }}>
                <img style={{ width: 100 + 'vw' }} src="background.png" alt="Suggested Prompts" />
            </div>
            {content}
        </div>
    );
}

export default App;
