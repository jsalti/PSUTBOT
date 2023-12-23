const chatlog = document.getElementById('chatlog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const micButton = document.getElementById('micButton');

function appendMessage(message, isUser) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';

    if (isUser) {
        messageContainer.className += ' user-message-container';
    } else {
        messageContainer.className += ' bot-message-container';
    }

    messageContainer.innerHTML = `
        ${isUser? '':`<img src='assets/bot_logo.png' class='bot-logo' />`}
        <div class="message-text ${isUser ? 'user-message' : 'bot-message'}">${message}</div>
    `;

    chatlog.appendChild(messageContainer);
    chatlog.scrollTop = chatlog.scrollHeight;
}

function handleUserInput() {
    const userMessage = userInput.value;
    if (userMessage.trim() === '') return;

    appendMessage(userMessage, true);

    // Add your chatbot logic here
    const botResponse = getBotResponse(userMessage);
    appendMessage(botResponse, false);

    userInput.value = '';
}

function getBotResponse(userMessage) {
    // You can customize the bot's responses here based on user input
    const greetings = ['Hello!', 'Hi there!', 'Greetings!'];
    const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];

    if (userMessage.toLowerCase().includes('how are you')) {
        return 'I am just a bot, but thanks for asking!';
    } else if (userMessage.toLowerCase().includes('help')) {
        return 'I can help you with basic information.';
    } else {
        return 'I didn\'t understand that. Can you please rephrase?';
    }
}

function handleMicButton() {
    // Handle voice recognition here (using SpeechRecognition API)
    // You can add code to start and stop voice recognition when the "Mic" button is clicked.
    // Note: Implementing voice recognition requires additional JavaScript code not included here.
}

sendButton.addEventListener('click', handleUserInput);
micButton.addEventListener('click', handleMicButton);

userInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        handleUserInput();
    }
});