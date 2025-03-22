function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();

  if (message) {
    // Afficher le message de l'utilisateur
    addMessage("user", message);

    // Envoyer la requête au serveur
    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Afficher la réponse du chatbot
        addMessage("bot", data.response);

        // Ajouter les liens si présents
        if (data.response.links) {
          addLinks(data.response.links);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        addMessage("bot", "Désolé, une erreur est survenue.");
      });

    // Vider l'input
    input.value = "";
  }
}

function addMessage(type, message) {
  const messagesDiv = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}-message`;

  if (typeof message === "string") {
    messageDiv.textContent = message;
  } else if (message.text) {
    messageDiv.textContent = message.text;
  }

  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addLinks(links) {
  const messagesDiv = document.getElementById("chat-messages");
  const linksDiv = document.createElement("div");
  linksDiv.className = "suggested-links";

  links.forEach((link) => {
    const button = document.createElement("button");
    button.textContent = link.title;
    button.onclick = () => window.open(link.url, "_blank");
    linksDiv.appendChild(button);
  });

  messagesDiv.appendChild(linksDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function askQuestion(question) {
  const input = document.getElementById("user-input");
  input.value = question;
  sendMessage();
}

// Activer l'envoi avec la touche Entrée
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
