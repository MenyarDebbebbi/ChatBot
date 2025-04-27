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

function switchLanguage(lang) {
  // Stockez la langue sélectionnée
  localStorage.setItem("preferred_language", lang);

  // Rechargez la page pour appliquer le changement
  location.reload();
}

// Ajoutez ceci au début du fichier
document.addEventListener("DOMContentLoaded", function () {
  const preferredLanguage = localStorage.getItem("preferred_language") || "fr";
  // Vous pouvez utiliser cette valeur pour adapter l'interface

  // Charger le thème sauvegardé
  const savedTheme = localStorage.getItem("theme") || "light";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    updateThemeButton();
  }
});

function toggleTheme() {
  const body = document.body;
  const button = document.getElementById("theme-toggle");

  body.classList.toggle("dark-mode");

  // Sauvegarder la préférence
  const isDarkMode = body.classList.contains("dark-mode");
  localStorage.setItem("theme", isDarkMode ? "dark" : "light");

  updateThemeButton();
}

function updateThemeButton() {
  const button = document.getElementById("theme-toggle");
  const icon = button.querySelector("i");
  const text = button.querySelector("span");

  if (document.body.classList.contains("dark-mode")) {
    icon.className = "fas fa-sun";
    text.textContent = "Mode clair";
  } else {
    icon.className = "fas fa-moon";
    text.textContent = "Mode sombre";
  }
}

let recognition;
let isListening = false;

function initSpeechRecognition() {
  if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "fr-FR";

    recognition.onresult = function (event) {
      const transcript = event.results[0][0].transcript;
      document.getElementById("user-input").value = transcript;
      stopVoiceInput();
      sendMessage();
    };

    recognition.onerror = function (event) {
      console.error("Erreur de reconnaissance vocale:", event.error);
      stopVoiceInput();
    };

    recognition.onend = function () {
      stopVoiceInput();
    };
  } else {
    console.error(
      "La reconnaissance vocale n'est pas supportée par ce navigateur."
    );
    document.getElementById("voice-button").style.display = "none";
  }
}

function toggleVoiceInput() {
  if (!recognition) {
    initSpeechRecognition();
  }

  if (isListening) {
    stopVoiceInput();
  } else {
    startVoiceInput();
  }
}

function startVoiceInput() {
  if (recognition) {
    recognition.start();
    isListening = true;
    document.getElementById("voice-button").classList.add("active");
    document.getElementById("user-input").placeholder = "Parlez maintenant...";
  }
}

function stopVoiceInput() {
  if (recognition) {
    recognition.stop();
    isListening = false;
    document.getElementById("voice-button").classList.remove("active");
    document.getElementById("user-input").placeholder =
      "Tapez votre question ici...";
  }
}

// Initialize speech recognition when the page loads
document.addEventListener("DOMContentLoaded", initSpeechRecognition);
