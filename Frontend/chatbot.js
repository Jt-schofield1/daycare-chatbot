const chatForm = document.getElementById("chat-form");
const chatWindow = document.getElementById("chat-window");

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userInput = document.getElementById("user-input").value;

    // Display user message in the chat window
    addMessage("user", userInput);

    // Send user input to the backend and get the bot's response
    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput }),
        });
        const data = await response.json();
        addMessage("bot", data.reply || "Sorry, something went wrong.");
    } catch (error) {
        console.error("Error:", error);
        addMessage("bot", "Sorry, I'm having trouble right now.");
    }

    document.getElementById("user-input").value = "";
});

function addMessage(sender, message) {
    const messageElem = document.createElement("div");
    messageElem.className = sender;
    messageElem.innerText = message;
    chatWindow.appendChild(messageElem);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
