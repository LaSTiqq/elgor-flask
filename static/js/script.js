// Arrow to the top of the page
const arrow = document.getElementById("arrow");

arrow.classList.add("d-none");

const scrollFunction = () => {
  const scrolled =
    document.body.scrollTop > 50 || document.documentElement.scrollTop > 50;

  if (scrolled && window.innerWidth >= 768) {
    arrow.classList.remove("d-none");
    arrow.classList.add("d-md-block");
  } else {
    arrow.classList.remove("d-md-block");
    arrow.classList.add("d-none");
  }
};

window.addEventListener("scroll", scrollFunction);

// Lighthouse audit low score fix
const carousel = document.querySelector(".main-carousel");

document.addEventListener("DOMContentLoaded", () => {
  let flkty = new Flickity(carousel, {
    wrapAround: true,
    pageDots: false,
    cellAlign: "left",
    autoPlay: true,
    pauseAutoPlayOnHover: false,
    setGallerySize: false,
  });
});

// AJAX form submission
document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  const form = document.getElementById("form");
  const loader = document.getElementById("loader");
  const alertBox = document.getElementById("alert");
  const fields = form.querySelectorAll("input, textarea");

  fields.forEach((field) => {
    field.addEventListener("input", () => {
      if (!field.checkValidity()) {
        field.classList.add("is-invalid");
        field.classList.remove("is-valid");
      } else {
        field.classList.remove("is-invalid");
        field.classList.add("is-valid");
      }
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (!form.checkValidity()) {
      form.classList.add("was-validated");

      const firstInvalid = form.querySelector(":invalid");
      if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
        firstInvalid.focus({ preventScroll: true });
      }
      return;
    }

    form.classList.add("was-validated");
    loader.classList.remove("d-none");

    grecaptcha.ready(() => {
      grecaptcha
        .execute("6LfKamonAAAAAIR7O00Dq36sOQ3OePxh1TkZ8oQu", {
          action: "contact",
        })
        .then(async (token) => {
          document.getElementById("g-recaptcha-response").value = token;

          const formData = new FormData(form);

          try {
            const response = await fetch("/send-ajax", {
              method: "POST",
              headers: {
                "X-CSRFToken": formData.get("csrf_token"),
              },
              body: formData,
            });

            const result = await response.json();
            showAlert(result.message, result.status);

            if (result.status !== "info") {
              form.reset();
              form.classList.remove("was-validated");
              fields.forEach((f) =>
                f.classList.remove("is-valid", "is-invalid")
              );
            }
          } catch (err) {
            showAlert("Something went wrong! Please try again.", "danger");
          } finally {
            loader.classList.add("d-none");
          }
        });
    });
  });

  function showAlert(message, type) {
    alertBox.className = `alert alert-${type} alert-dismissible rounded-pill fw-bold d-block`;
    alertBox.innerHTML = `
      ${message}
      <button type="button" class="btn-close" aria-label="Close"></button>
    `;

    const closeBtn = alertBox.querySelector(".btn-close");
    closeBtn.addEventListener("click", () => {
      alertBox.className = "alert d-none";
    });

    setTimeout(() => {
      alertBox.className = "alert d-none";
    }, 4000);
  }
});


// Working form alert close button without Bootstrap JS
const closeButton = document.querySelector(".btn-close");
const alertElement = document.querySelector(".alert");

if (closeButton && alertElement) {
  closeButton.addEventListener("click", () => {
    alertElement.style.display = "none";
  });
}
