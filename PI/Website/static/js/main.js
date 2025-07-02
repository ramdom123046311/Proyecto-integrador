document.addEventListener('DOMContentLoaded', () => {
    let page = 1;
    const importanceContent = document.getElementById('importance-content');
    const infiniteScrollTrigger = document.getElementById('infinite-scroll-trigger');
    const bannerImage = document.querySelector('.banner img');
    const menuIcon = document.getElementById('menu-icon');
    const navMenu = document.getElementById('nav-menu');
    const images = document.getElementById('images').dataset;

    const staticData = [
        {
            image: images.img1,
            title: "1. Reducción de la mortalidad materna:",
            description: "Sin duda alguna ha habido avances significativos, sin embargo, todavía mueren alrededor de 295,000 mujeres durante o después del embarazo y el parto cada año. Las causas más comunes incluyen la pérdida excesiva de sangre, infecciones, alta presión arterial, abortos peligrosos y partos obstruidos. La mayoría de estas muertes son prevenibles con la atención adecuada de profesionales."
        },
        {
            image: images.img2,
            title: "2. Beneficios para la madre y el bebé:",
            description: "La atención materna adecuada asegura el pleno potencial de salud y bienestar tanto para las mujeres como para sus bebés. Además, invertir tiempo en planificación familiar y cuidado materno y del recién nacido puede reducir significativamente las muertes."
        },
        {
            image: images.img3,
            title: "3. Lactancia materna:",
            description: "Amamantar a los bebés tiene múltiples beneficios. Los niños amamantados tienden a tener un mejor desempeño en pruebas de inteligencia, son menos propensos al sobrepeso u obesidad y, más adelante, a padecer diabetes. Además, las mujeres que amamantan tienen un menor riesgo de cáncer de mama y ovario."
        }
    ];

    const loadMoreContent = () => {
        if (page > staticData.length) return;
        const item = staticData[page - 1];
        const article = document.createElement('div');
        article.className = 'importance-item';
        article.innerHTML = `
            <img src="${item.image}" alt="${item.title}">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
        `;
        importanceContent.insertBefore(article, infiniteScrollTrigger);
        setTimeout(() => {
            article.classList.add('visible');
        }, 100);
        page++;
    };

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            loadMoreContent();
        }
    }, {
        rootMargin: '0px',
        threshold: 1.0
    });

    observer.observe(infiniteScrollTrigger);

    window.addEventListener('scroll', () => {
        const scrollPosition = window.pageYOffset;
        bannerImage.style.transform = `translateY(${scrollPosition * 0.5}px)`;
    });

    menuIcon.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
});
