// Arrow to the top of the page
const arrow = document.getElementById("arrow");

arrow.style.display = "none";

const scrollFunction = () => {
  const scrolled =
    document.body.scrollTop > 50 || document.documentElement.scrollTop > 50;

  if (scrolled) {
    arrow.style.display = "block";
  } else {
    arrow.style.display = "none";
  }
};

window.onscroll = () => {
  scrollFunction();
};

// Working form alert button without Bootstrap JS
const closeButton = document.querySelector(".btn-close");
const alertElement = document.querySelector(".alert");

if (closeButton && alertElement) {
  closeButton.addEventListener("click", () => {
    alertElement.style.display = "none";
  });
}

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
