import './App.css';
import Chatbot, {
    InputBarTrigger,
    ModalView,
} from "mongodb-chatbot-ui";

const suggestedPrompts = [
    "Wie viele Transferable Skills Kurse darf ich pro Semester besuchen?",
    "Wie kann ich mich für ein Doktoratsstudium an der Uni Basel anmelden?",
    "Was ist eine Cotutelle?",
];

function Chat() {
    return (
        <div className="chat">

            <header className="App-header">
                <Chatbot darkMode={true} serverBaseUrl="https://rag-grace-backend.xreco-retrieval.ch/api/v1" shouldStream={false} isExperimental={false}>
                        <InputBarTrigger suggestedPrompts={suggestedPrompts} />
                        <ModalView
                            initialMessageText="Willkommen beim Unibas-Chatbot! 🤖 Ich helfe Ihnen gerne weiter. Sollte ich keine passenden Dokumente in meiner Datenbank finden, kann ich Ihre Frage leider nicht beantworten. Bitte beachten Sie, keine persönlichen oder sensiblen Informationen mit mir zu teilen. Wie kann ich Ihnen weiterhelfen? 😊"
                            initialMessageSuggestedPrompts={suggestedPrompts}
                        />
                </Chatbot>
            </header>
        </div>
    );
}

export default Chat;
