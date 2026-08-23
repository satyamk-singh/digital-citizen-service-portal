const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
const contrastToggle = document.getElementById("contrastToggle");
const increaseText = document.getElementById("increaseText");
const decreaseText = document.getElementById("decreaseText");
const serviceSearchForm = document.getElementById("serviceSearchForm");
const serviceSearch = document.getElementById("serviceSearch");
const searchMessage = document.getElementById("searchMessage");

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
  document.body.classList.toggle("high-contrast");
});

increaseText.addEventListener("click", () => {
  document.body.classList.remove("small-text");
  document.body.classList.toggle("large-text");
});

decreaseText.addEventListener("click", () => {
  document.body.classList.remove("large-text");
  document.body.classList.toggle("small-text");
});

serviceSearchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = serviceSearch.value.trim().toLowerCase();
  if (!query) {
    searchMessage.textContent = "Type a service name to search.";
    return;
  }

  const matches = services.filter((service) => service.includes(query));
  searchMessage.textContent = matches.length
    ? `Found: ${matches.join(", ")}`
    : "No exact prototype match found. Try certificate, appointment, document, tracking, or grievance.";
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".auth-form").forEach((form) => form.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});
