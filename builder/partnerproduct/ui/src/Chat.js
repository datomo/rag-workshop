import './App.css';
import Chatbot, {
    InputBarTrigger,
    ModalView,
} from "mongodb-chatbot-ui";

const suggestedPrompts = [
    "Wie alt ist die Universität Basel?",
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
                            initialMessageText="Willkommen beim Unibas-Chatbot! 🤖 Ich helfe Ihnen gerne weiter. Sollte ich keine passenden Dokumente in meiner Datenbank finden, kann ich Ihre Frage leider nicht beantworten. Bitte beachten Sie, keine persönlichen oder sensiblen Informationen mit mir zu teilen. Wie kann ich Ihnen weiterhelfen? 😊"
                            initialMessageSuggestedPrompts={suggestedPrompts}
                        />
                    </>
                </Chatbot>
            </header>
        </div>
    );
}

export default Chat;
