const root = document.documentElement;
const storedTheme = localStorage.getItem("quizforge-theme");
if (storedTheme) root.dataset.theme = storedTheme;

function toast(message) {
  const stack = document.querySelector("[data-toast-stack]");
  if (!stack) return;
  const item = document.createElement("div");
  item.className = "toast";
  item.textContent = message;
  stack.appendChild(item);
  setTimeout(() => item.remove(), 3200);
}

document.addEventListener("click", (event) => {
  const navButton = event.target.closest("[data-nav-toggle]");
  if (navButton) {
    const menu = document.querySelector("[data-nav-menu]");
    const expanded = navButton.getAttribute("aria-expanded") === "true";
    navButton.setAttribute("aria-expanded", String(!expanded));
    menu?.classList.toggle("open");
  }

  const themeButton = event.target.closest("[data-theme-toggle]");
  if (themeButton) {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    localStorage.setItem("quizforge-theme", root.dataset.theme);
    toast(`${root.dataset.theme === "dark" ? "Dark" : "Light"} mode enabled`);
  }

  const passwordButton = event.target.closest("[data-password-toggle]");
  if (passwordButton) {
    const field = passwordButton.parentElement.querySelector("input");
    field.type = field.type === "password" ? "text" : "password";
    passwordButton.textContent = field.type === "password" ? "Show" : "Hide";
  }

  
});

document.querySelectorAll("[data-strength-input]").forEach((input) => {
  input.addEventListener("input", () => {
    const value = input.value;
    let score = 0;
    if (value.length >= 8) score += 25;
    if (/[A-Z]/.test(value)) score += 25;
    if (/[0-9]/.test(value)) score += 25;
    if (/[^A-Za-z0-9]/.test(value)) score += 25;
    const bar = input.closest("form")?.querySelector("[data-strength-bar]");
    if (bar) {
      bar.style.width = `${score}%`;
      bar.style.background = score > 70 ? "var(--success)" : score > 40 ? "var(--gold)" : "var(--danger)";
    }
  });
});

document.querySelectorAll("[data-validate-form]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!form.checkValidity()) {
      event.preventDefault();
      toast("Please complete the highlighted fields.");
      form.reportValidity();
    }
  });
});

document.querySelectorAll("[data-live-search]").forEach((input) => {
  input.addEventListener("input", () => {
    const term = input.value.trim().toLowerCase();
    document.querySelectorAll("[data-search-item]").forEach((item) => {
      item.style.display = item.textContent.toLowerCase().includes(term) ? "" : "none";
    });
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add("visible");
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((item) => revealObserver.observe(item));

function startQuizTimer() {
  const timer = document.querySelector("[data-timer]");
  if (!timer) return;
  const quizShell = document.querySelector("[data-quiz]");
  let remaining = Number(quizShell?.dataset.duration || 1500);
  const progress = document.querySelector("[data-quiz-progress]");
  const total = remaining;
  const interval = setInterval(() => {
    remaining -= 1;
    const minutes = String(Math.floor(remaining / 60)).padStart(2, "0");
    const seconds = String(remaining % 60).padStart(2, "0");
    timer.textContent = `${minutes}:${seconds}`;
    if (progress) progress.style.width = `${Math.max(0, (remaining / total) * 100)}%`;
    if (remaining <= 0) {
      clearInterval(interval);
      toast("Time is up. Your quiz is being submitted.");
      setTimeout(() => {
        const form = document.getElementById("quiz-submit-form");
        if (form) form.submit();
      }, 1200);
    }
  }, 1000);
}
startQuizTimer();
