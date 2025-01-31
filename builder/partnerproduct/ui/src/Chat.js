import './App.css';
import Chatbot, {
    InputBarTrigger,
    ModalView,
} from "mongodb-chatbot-ui";

const suggestedPrompts = [
    "How old is the University of Basel?",
    "Wie muss ich mich für ein Examen (Prüfung zu einer Hauptvorlesung) anmelden?",
    "Welche Schritte muss ich unternehmen, um sicherzustellen, dass meine Bachelor- oder Masterarbeit den Anforderungen der Erklärung zur wissenschaftlichen Integrität entspricht, insbesondere in Bezug auf die Kennzeichnung von Quellen und die Verwendung von KI-unterstützter Technologie?",
];

function Chat() {
    return (
        <div className="chat">

            <header className="App-header">
                <Chatbot darkMode={true} serverBaseUrl="http://localhost:9000/api/v1" shouldStream={false} isExperimental={false}>
                    <>
                        <InputBarTrigger suggestedPrompts={suggestedPrompts} />
                        <ModalView
                            initialMessageText="Willkommen beim Chatbot der Fakultät für Naturwissenschaften! 🤖 Ich bin hier, um zuverlässige Antworten zu geben, die auf den offiziellen Informationen der Fakultät basieren. Welche Informationen suchen Sie?"
                            initialMessageSuggestedPrompts={suggestedPrompts}
                        />
                    </>
                </Chatbot>
            </header>
        </div>
    );
}

export default Chat;
