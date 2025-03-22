document.addEventListener("DOMContentLoaded", function () {
  // Animation du compteur pour les stats
  const statNumbers = document.querySelectorAll(".stat-card h3");

  statNumbers.forEach((number) => {
    const target = parseInt(number.textContent);
    let count = 0;
    const duration = 2000; // 2 secondes
    const increment = target / (duration / 16); // 60fps

    function updateCount() {
      if (count < target) {
        count += increment;
        number.textContent = Math.ceil(count);
        requestAnimationFrame(updateCount);
      } else {
        number.textContent = target;
      }
    }

    updateCount();
  });

  // Gestion du mode sombre
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;
  const icon = themeToggle.querySelector("i");

  // Charger la préférence sauvegardée
  const savedTheme = localStorage.getItem("theme") || "light";
  if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    icon.className = "fas fa-sun";
  }

  // Gestionnaire de clic pour le bouton de thème
  themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    const isDark = body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    icon.className = isDark ? "fas fa-sun" : "fas fa-moon";
  });

  // Animation des compteurs
  const statNumbers = document.querySelectorAll(".counter");

  statNumbers.forEach((number) => {
    const target = parseInt(number.textContent);
    let count = 0;
    const duration = 2000;
    const increment = target / (duration / 16);

    function updateCount() {
      if (count < target) {
        count += increment;
        number.textContent = Math.ceil(count) + "+";
        requestAnimationFrame(updateCount);
      } else {
        number.textContent = target + "+";
      }
    }

    updateCount();
  });

  // Animation des barres de progression
  const progressBars = document.querySelectorAll(".progress-bar");
  progressBars.forEach((bar) => {
    const width = bar.style.width;
    bar.style.width = "0";
    setTimeout(() => {
      bar.style.width = width;
    }, 300);
  });
});

function updateThemeIcon(button) {
  const icon = button.querySelector("i");
  if (document.body.classList.contains("dark-mode")) {
    icon.className = "fas fa-sun";
  } else {
    icon.className = "fas fa-moon";
  }
}

// Ajoutez cette fonction pour l'animation des barres de progression
function animateProgressBars() {
  const progressBars = document.querySelectorAll(".progress-bar");
  progressBars.forEach((bar) => {
    const width = bar.style.width;
    bar.style.width = "0";
    setTimeout(() => {
      bar.style.width = width;
    }, 300);
  });
}
