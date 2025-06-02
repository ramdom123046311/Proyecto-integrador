let currentIndex = 0;

const items = document.querySelectorAll('.carousel-item');
const totalItems = items.length;
const carouselInner = document.querySelector('.carousel-inner');

function updateCarousel() {
  carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % totalItems;
  updateCarousel();
}

// Avanza automáticamente cada 3 segundos
setInterval(nextSlide, 5000);

// También se pueden mantener los controles manuales si deseas:
const nextButton = document.querySelector('.carousel-control.next');
const prevButton = document.querySelector('.carousel-control.prev');

nextButton.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % totalItems;
  updateCarousel();
});

prevButton.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + totalItems) % totalItems;
  updateCarousel();
});
