document.addEventListener('DOMContentLoaded', () => {
    let page = 1;
    const specialistsContent = document.querySelector('.specialists');
    const infiniteScrollTrigger = document.getElementById('infinite-scroll-trigger');
    const menuIcon = document.getElementById('menu-icon');
    const navMenu = document.getElementById('nav-menu');
    let lastScrollTop = 0;

    const staticData = [
        {
            image: "imagenes/draange.png",
            name: "Dra. Angelica Resendiz",
            specialization: "Especialista en Ginecología, Obstetricia y Perinatología",
            location: "Hospital Los Angeles",
            age: "39 años",
            experience: "5 años",
            details: [
                "Atención prenatal y posnatal",
                "Embarazos de alto riesgo",
                "Complicaciones fetales y maternas",
                "Diagnósticos y tratamientos para condiciones que pueden afectar el embarazo"
            ],
            contactPage: "contacange.html",
            buttonClass: "contact-button2"
        },
        {
            image: "imagenes/drdam.png",
            name: "Dr. Damián Gutierrez",
            specialization: "Especialista en Ginecología y Neonatología",
            location: "Hospital del Niño y la Mujer en Qro",
            age: "45 años",
            experience: "20 años",
            details: [
                "Atención prenatal y posnatal",
                "Cuidado de recién nacidos y prematuros o con problemas complejos",
                "Cuidados intensivos neonatales",
                "Diagnósticos y tratamientos para condiciones que pueden afectar el embarazo"
            ],
            contactPage: "contactodam.html",
            buttonClass: "contact-button1"
        },
        {
            image: "imagenes/drasusana.png",
            name: "Dra. Susana Moscoso",
            specialization: "Especialista en Ginecología y Consultora de Lactancia",
            location: "Hospital General de Qro",
            age: "34 años",
            experience: "3 años",
            details: [
                "Atención prenatal y posnatal",
                "Ayuda a las madres a iniciar y mantener la lactancia materna",
                "Apoyo y soluciones para el dolor al amamantar",
                "Salud reproductiva y fertilidad"
            ],
            contactPage: "contacsus.html",
            buttonClass: "contact-button2"
        }
    ];

    const loadMoreContent = () => {
        if (page > staticData.length) return;
        const item = staticData[page - 1];
        const specialist = document.createElement('div');
        specialist.className = 'specialist hidden';
        specialist.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="perfil-foto">
            <div class="specialist-info">
                <h2>${item.name}</h2>
                <p>${item.specialization}</p>
                <p>Actualmente en: ${item.location}</p>
                <p>Edad: ${item.age}</p>
                <p>Tiempo de experiencia: ${item.experience}</p>
                <ul>${item.details.map(detail => `<li>${detail}</li>`).join('')}</ul>
                <a href="${item.contactPage}"><button class="${item.buttonClass}">Contáctame</button></a>
            </div>
        `;
        specialistsContent.insertBefore(specialist, infiniteScrollTrigger);

        setTimeout(() => {
            specialist.classList.add('visible');
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
        let currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const specialistsItems = document.querySelectorAll('.specialist:not(.no-animation)');

        if (currentScrollTop > lastScrollTop) {
            specialistsItems.forEach(item => {
                item.classList.add('visible');
                item.classList.remove('hidden');
            });
        }
        lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
    });

    menuIcon.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
});
