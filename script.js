const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

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

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".auth-form").forEach((form) => form.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});
