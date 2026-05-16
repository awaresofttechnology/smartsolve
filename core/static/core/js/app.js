/* SmartSync – app.js */
"use strict";

/* ── Sticky nav ── */
const navbar = document.getElementById("navbar");
window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 20);
});

/* ── Mobile hamburger ── */
const hamburger = document.getElementById("hamburger");
const navLinks  = document.getElementById("navLinks");
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("open");
});
document.addEventListener("click", (e) => {
  if (!navbar.contains(e.target)) navLinks.classList.remove("open");
});

/* ── Smooth active-link highlight ── */
const sections = document.querySelectorAll("section[id]");
const navItems = document.querySelectorAll(".nav-links a");
window.addEventListener("scroll", () => {
  let current = "";
  sections.forEach((sec) => {
    if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
  });
  navItems.forEach((a) => {
    a.style.color = a.getAttribute("href") === `#${current}` ? "var(--blue)" : "";
  });
});

/* ── Scroll-reveal ── */
const revealEls = document.querySelectorAll(
  ".service-card, .ind-card, .process-step, .testi-card, .ap, .av-card, .stat-item"
);
revealEls.forEach((el) => el.classList.add("reveal"));

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.delay || 0;
        setTimeout(() => entry.target.classList.add("visible"), delay * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);
revealEls.forEach((el) => revealObserver.observe(el));

/* ── Counter animation ── */
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1800;
  const step = 16;
  const increments = Math.ceil(duration / step);
  let count = 0;
  const timer = setInterval(() => {
    count++;
    el.textContent = Math.round((count / increments) * target);
    if (count >= increments) {
      el.textContent = target;
      clearInterval(timer);
    }
  }, step);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll("[data-target]").forEach(animateCounter);
        counterObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.3 }
);
document.querySelectorAll(".hero-stats, .stats-section").forEach((sec) =>
  counterObserver.observe(sec)
);

/* ── Contact form (AJAX to Django view) ── */
const form = document.getElementById("contactForm");
if (form) {
  function clearFormErrors() {
    form.querySelectorAll(".field-error").forEach((el) => el.remove());
    form.querySelectorAll(".has-error").forEach((el) => el.classList.remove("has-error"));
  }

  function showFormErrors(errors) {
    Object.entries(errors || {}).forEach(([field, message]) => {
      const input = form.elements[field];
      if (!input) return;

      const group = input.closest(".cf-group");
      if (!group) return;

      group.classList.add("has-error");
      const error = document.createElement("p");
      error.className = "field-error";
      error.textContent = message;
      group.appendChild(error);
    });
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector("[type=submit]");
    const successEl = document.getElementById("formSuccess");
    clearFormErrors();
    successEl.classList.remove("show");

    const payload = {
      fname:   form.fname.value,
      lname:   form.lname.value,
      email:   form.email.value,
      service: form.service.value,
      message: form.message.value,
    };

    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
    const url = form.dataset.url;

    submitBtn.textContent = "Sending…";
    submitBtn.disabled = true;

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        successEl.classList.add("show");
        form.reset();
      } else {
        const data = await res.json().catch(() => ({}));
        if (data.errors) {
          showFormErrors(data.errors);
          return;
        }
        throw new Error("Server error");
      }
    } catch {
      alert("Something went wrong. Please try again or email us directly.");
    } finally {
      submitBtn.textContent = "Send Message →";
      submitBtn.disabled = false;
    }
  });
}
