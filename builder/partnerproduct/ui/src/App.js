import './App.css';
import Chatbot, {
  InputBarTrigger,
  ModalView,
} from "mongodb-chatbot-ui";

const suggestedPrompts = [
  "How old is the university of Basel?",
  "What do i have to do to take part in the exam for dental medicine?",
];

function App() {
  return (
    <div className="App">
      
      <header className="App-header">
      <Chatbot darkMode={true} serverBaseUrl="http://localhost:9000/api/v1" shouldStream={false} isExperimental={false}>
        <>
          <InputBarTrigger suggestedPrompts={suggestedPrompts} />
          <ModalView
            initialMessageText="Welcome to UniBot your digital resource all things university Basel. What do you wana learn today?"
            initialMessageSuggestedPrompts={suggestedPrompts}
          />
        </>
      </Chatbot>
      </header>
    </div>
  );
}

export default App;
