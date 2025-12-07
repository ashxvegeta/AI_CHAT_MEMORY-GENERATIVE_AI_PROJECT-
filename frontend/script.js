const API_URL = "http://127.0.0.1:8000";

async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    addMessage("user", message);
    input.value = "";

    const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage("bot", data.reply);
}

async function clearHistory() {
    await fetch(`${API_URL}/clear_history`);
    document.getElementById("chat-box").innerHTML = "";
}

function addMessage(role, text) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");

    div.className = role === "user" ? "user" : "bot";
    div.textContent = text;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
