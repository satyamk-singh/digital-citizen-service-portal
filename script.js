const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
const contrastToggle = document.getElementById("contrastToggle");
const increaseText = document.getElementById("increaseText");
const decreaseText = document.getElementById("decreaseText");
const serviceSearchForm = document.getElementById("serviceSearchForm");
const serviceSearch = document.getElementById("serviceSearch");
const searchMessage = document.getElementById("searchMessage");
const documentUpload = document.getElementById("documentUpload");
const documentMessage = document.getElementById("documentMessage");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const loginMessage = document.getElementById("loginMessage");
const registerMessage = document.getElementById("registerMessage");
const serviceCards = document.querySelectorAll(".service-card");

const services = [
  "income certificate",
  "residence certificate",
  "birth certificate",
  "appointment booking",
  "document upload",
  "application tracking",
  "public grievance",
  "citizen login",
];

menuToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
});

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
  });
});

document.getElementById("appointmentForm").addEventListener("submit", (event) => {
  event.preventDefault();
  document.getElementById("appointmentMessage").textContent =
    "Appointment request saved in the prototype dashboard.";
});

document.getElementById("trackingForm").addEventListener("submit", (event) => {
  event.preventDefault();
  document.getElementById("trackingResult").classList.add("highlight");
});

contrastToggle.addEventListener("click", () => {
  const isActive = document.body.classList.toggle("high-contrast");
  contrastToggle.setAttribute("aria-pressed", String(isActive));
});

increaseText.addEventListener("click", () => {
  document.body.classList.remove("small-text");
  const isActive = document.body.classList.toggle("large-text");
  increaseText.setAttribute("aria-pressed", String(isActive));
  decreaseText.setAttribute("aria-pressed", "false");
});

decreaseText.addEventListener("click", () => {
  document.body.classList.remove("large-text");
  const isActive = document.body.classList.toggle("small-text");
  decreaseText.setAttribute("aria-pressed", String(isActive));
  increaseText.setAttribute("aria-pressed", "false");
});

serviceSearchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = serviceSearch.value.trim().toLowerCase();
  if (!query) {
    searchMessage.textContent = "Type a service name to search.";
    serviceCards.forEach((card) => card.classList.remove("is-hidden"));
    return;
  }

  let visibleCount = 0;
  serviceCards.forEach((card) => {
    const keywords = card.dataset.search || card.textContent.toLowerCase();
    const isMatch = keywords.includes(query);
    card.classList.toggle("is-hidden", !isMatch);
    if (isMatch) {
      visibleCount += 1;
    }
  });

  const matches = services.filter((service) => service.includes(query));
  searchMessage.textContent = visibleCount
    ? `Showing ${visibleCount} matching service card(s): ${matches.join(", ") || query}`
    : "No exact prototype match found. Try certificate, appointment, document, tracking, or grievance.";
});

documentUpload.addEventListener("change", () => {
  const file = documentUpload.files[0];
  documentMessage.textContent = file
    ? `${file.name} selected for upload simulation.`
    : "";
});

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  loginMessage.textContent = "Login simulation successful. Dashboard access would open in a full system.";
});

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  registerMessage.textContent = "Registration simulation successful. Account verification would happen in a full system.";
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".auth-form").forEach((form) => form.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});
