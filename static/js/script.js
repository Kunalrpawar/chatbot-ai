document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendMessage = document.getElementById('send-message');

    function loadChatHistory() {
        fetch('/get_chat_history')
            .then(response => response.json())
            .then(history => {
                chatMessages.innerHTML = '';
                history.forEach(message => {
                    appendMessage(message[0], message[1]);
                });
            });
    }

    function sendUserMessage() {
        const message = userInput.value.trim();
        if (message) {
            appendMessage('You', message);
            userInput.value = '';
            
            fetch('/chat_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                appendMessage('AI', data.response);
            })
            .catch((error) => {
                console.error('Error:', error);
                appendMessage('AI', 'Sorry, there was an error processing your request.');
            });
        }
    }

    function appendMessage(sender, text) {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    if (sendMessage) {
        sendMessage.addEventListener('click', sendUserMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendUserMessage();
            }
        });

        loadChatHistory();
    }
});
