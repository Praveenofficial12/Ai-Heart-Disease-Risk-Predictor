/* =========================================
   AI Heart Disease Risk Predictor - main.js
========================================= */

document.addEventListener("DOMContentLoaded", () => {

  /* ===============================
     BUTTON RIPPLE EFFECT
  =============================== */
  const buttons = document.querySelectorAll("button, .btn");

  buttons.forEach(btn => {
    btn.style.position = "relative";
    btn.style.overflow = "hidden";

    btn.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      ripple.classList.add("ripple");

      const rect = this.getBoundingClientRect();
      ripple.style.left = `${e.clientX - rect.left}px`;
      ripple.style.top = `${e.clientY - rect.top}px`;

      this.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });
  });


  /* ===============================
     FORM SUBMIT LOADING EFFECT
  =============================== */
  const forms = document.querySelectorAll("form");

  forms.forEach(form => {
    form.addEventListener("submit", () => {
      const submitBtn = form.querySelector("button[type='submit']");
      if (submitBtn) {
        submitBtn.innerText = "Please wait...";
        submitBtn.disabled = true;
      }
    });
  });

});


/* ===============================
   LOGOUT CONFIRMATION
=============================== */
function confirmLogout() {
  return confirm("Are you sure you want to sign out?");
}


/* ===============================
   VOICE OUTPUT (RESULT PAGE)
=============================== */
function speakResult(text) {
  if ("speechSynthesis" in window) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.rate = 0.95;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
  } else {
    alert("Voice output not supported in this browser.");
  }
}


/* ===============================
   MANUAL LOADING (OPTIONAL)
=============================== */
function showLoading(btn) {
  btn.innerText = "Analyzing...";
  btn.disabled = true;
}
