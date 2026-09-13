/* =========================================
   CardioAI — main.js
   Professional Medical Application JS
========================================= */

document.addEventListener("DOMContentLoaded", () => {

  /* ===============================
     RIPPLE EFFECT ON BUTTONS
  =============================== */
  document.querySelectorAll("button, .btn, .action-card, .quick-link").forEach(el => {
    el.style.position = "relative";
    el.style.overflow = "hidden";

    el.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      Object.assign(ripple.style, {
        position: "absolute",
        width: "6px",
        height: "6px",
        borderRadius: "50%",
        background: "rgba(255,255,255,0.3)",
        transform: "scale(0)",
        animation: "rippleAnim 0.55s ease-out",
        left: (e.clientX - this.getBoundingClientRect().left - 3) + "px",
        top: (e.clientY - this.getBoundingClientRect().top - 3) + "px",
        pointerEvents: "none"
      });
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  /* ===============================
     FORM SUBMIT LOADING STATE
  =============================== */
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function () {
      const btn = this.querySelector("button[type='submit'], .submit-btn");
      if (btn) {
        const original = btn.innerHTML;
        btn.innerHTML = '<span style="opacity:0.8">⏳ Processing...</span>';
        btn.disabled = true;
        btn.style.opacity = "0.8";
        // Restore after 10s if something fails
        setTimeout(() => {
          btn.innerHTML = original;
          btn.disabled = false;
          btn.style.opacity = "1";
        }, 10000);
      }
    });
  });

  /* ===============================
     AUTO-DISMISS ALERTS
  =============================== */
  document.querySelectorAll(".alert").forEach((alert, i) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 4000 + i * 500);
  });

  /* ===============================
     NAVBAR SCROLL EFFECT
  =============================== */
  const navbar = document.querySelector(".navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 20) {
        navbar.style.background = "rgba(5,13,26,0.96)";
        navbar.style.boxShadow = "0 2px 30px rgba(0,0,0,0.4)";
      } else {
        navbar.style.background = "rgba(5,13,26,0.85)";
        navbar.style.boxShadow = "none";
      }
    }, { passive: true });
  }

  /* ===============================
     ANIMATED COUNTERS (stat numbers)
  =============================== */
  const counters = document.querySelectorAll(".stat-number, .stat-block-num, .hero-stat-num");
  counters.forEach(counter => {
    const text = counter.textContent.trim();
    const num = parseFloat(text.replace(/[^0-9.]/g, ""));
    if (!isNaN(num) && num > 0 && num < 10000) {
      counter.textContent = "0";
      let current = 0;
      const step = num / 40;
      const timer = setInterval(() => {
        current += step;
        if (current >= num) {
          counter.textContent = text; // restore original with any suffix
          clearInterval(timer);
        } else {
          counter.textContent = Math.floor(current).toLocaleString();
        }
      }, 30);
    }
  });

  /* ===============================
     STAGGER FADE-UP FOR CARDS
  =============================== */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }, i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll(".feature-card, .action-card, .history-card, .testimonial-card").forEach(card => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "opacity 0.55s ease, transform 0.55s ease";
    observer.observe(card);
  });

  /* ===============================
     INPUT FOCUS ENHANCEMENT
  =============================== */
  document.querySelectorAll(".form-control").forEach(input => {
    const wrapper = input.closest(".form-group");
    if (!wrapper) return;

    input.addEventListener("focus", () => {
      wrapper.querySelector(".form-label") &&
        (wrapper.querySelector(".form-label").style.color = "var(--clr-primary)");
    });

    input.addEventListener("blur", () => {
      wrapper.querySelector(".form-label") &&
        (wrapper.querySelector(".form-label").style.color = "");
    });
  });

});

/* ===============================
   RIPPLE ANIMATION INJECTION
=============================== */
const rippleCSS = document.createElement("style");
rippleCSS.textContent = `
  @keyframes rippleAnim {
    to { transform: scale(40); opacity: 0; }
  }
`;
document.head.appendChild(rippleCSS);

/* ===============================
   VOICE OUTPUT (RESULT PAGE)
=============================== */
function speakResult(text) {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
    const speech = new SpeechSynthesisUtterance(text);
    speech.rate = 0.9;
    speech.pitch = 1;
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  } else {
    alert("Voice output not supported in this browser.");
  }
}

/* ===============================
   LOGOUT CONFIRMATION
=============================== */
function confirmLogout() {
  return confirm("Are you sure you want to sign out of CardioAI?");
}
