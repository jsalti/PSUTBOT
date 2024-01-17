const chatlog = document.getElementById("chatlog");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");

function appendMessage(message, isUser) {
  const messageContainer = document.createElement("div");
  messageContainer.className = "message-container";

  if (isUser) {
    messageContainer.className += " user-message-container";
  } else {
    messageContainer.className += " bot-message-container";
  }

  messageContainer.innerHTML = `
        ${isUser ? "" : `<img src='assets/bot_logo.png' class='bot-logo' />`}
        <div class="message-text ${
          isUser ? "user-message" : "bot-message"
        }">${message}</div>
    `;

  chatlog.appendChild(messageContainer);
  chatlog.scrollTop = chatlog.scrollHeight;
}

function appendInitialBotMessage() {
  const initialMessage = "Hello! I'm PSUTBOT How can I help you?";
  appendMessage(initialMessage, false);
}

async function getBotResponse(userMessage) {
  try {
    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    return data.answer; // assuming the Flask server responds with a JSON containing an 'answer' field
  } catch (error) {
    console.error("Error fetching response:", error);
    return "Sorry, I am having trouble responding right now.";
  }
}

async function handleUserInput() {
  const userMessage = userInput.value;
  if (userMessage.trim() === "") return;

  appendMessage(userMessage, true);

  const botResponse = await getBotResponse(userMessage);
  appendMessage(botResponse, false);

  userInput.value = "";
}

function handleMicButton() {
  // Handle voice recognition here (using SpeechRecognition API)
  // You can add code to start and stop voice recognition when the "Mic" button is clicked.
  // Note: Implementing voice recognition requires additional JavaScript code not included here.
}

document.addEventListener("DOMContentLoaded", appendInitialBotMessage);
sendButton.addEventListener("click", handleUserInput);
micButton.addEventListener("click", handleMicButton);

userInput.addEventListener("keyup", function (event) {
  if (event.key === "Enter") {
    handleUserInput();
  }
});
