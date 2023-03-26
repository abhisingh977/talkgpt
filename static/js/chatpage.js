

// Initialize the previous model response variable with an empty string
let previousResponse = '';

// Get the input field and form element from the HTML
const form = document.querySelector('#chat-form');
const inputField = document.querySelector('#chat-input');



// Add an event listener to the form to handle user input
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent form submission

    // Get the user input from the input field
    const userInput = inputField.value;

    // Combine the previous response and the new user input
    const text = userInput + " ";

    // Send the text to the server for processing
    const response = await fetch('/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text })
    });

    // Get the response from the server
    const data = await response.json();

    // Update the previous response with the new response
    previousResponse = data.response;

    const chatContainer = document.querySelector('#chat-container');
    const chatBubble = document.createElement('div');
    chatBubble.classList.add('chat-bubble');
    chatBubble.innerHTML = `<p><strong>Your Input: </strong> ${userInput}</p><p><strong>WriteGPT: </strong> ${previousResponse}</p>`;
    chatContainer.appendChild(chatBubble);
    

    // Clear the input field
    inputField.value = '';
});