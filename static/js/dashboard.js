document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".nav-link");
    const sections = document.querySelectorAll(".content-section");

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            const target = link.getAttribute("data-page");

            sections.forEach(section => section.classList.add("d-none"));
            const sectionToShow = document.getElementById(target);
            if (sectionToShow) sectionToShow.classList.remove("d-none");
        });
    });

    document.querySelector(".nav-link.active").click();
});
