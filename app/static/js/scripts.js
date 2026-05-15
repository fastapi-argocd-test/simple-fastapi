/*!
* Start Bootstrap - Resume v7.0.6 (https://startbootstrap.com/theme/resume)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
*/
//
// Scripts
// 


window.addEventListener("DOMContentLoaded", () => {
  const navRoot = document.querySelector("#sideNav");
  const navbarToggler = document.querySelector(".navbar-toggler");

  const tocRoot = document.querySelector("#navbarResponsive .toc");
  if (tocRoot) {
    tocRoot.querySelectorAll("ul").forEach((ul) => ul.classList.add("navbar-nav"));
    tocRoot.querySelectorAll("li").forEach((li) => li.classList.add("nav-item"));
    tocRoot.querySelectorAll("a").forEach((a) => a.classList.add("nav-link", "js-scroll-trigger"));
    tocRoot.classList.add("w-100");
  }

  const links = Array.from(document.querySelectorAll("#navbarResponsive a.nav-link"))
    .filter((a) => a.getAttribute("href") && a.getAttribute("href").startsWith("#"));

  const targets = links
    .map((a) => {
      const id = decodeURIComponent(a.getAttribute("href").slice(1));
      const el = document.getElementById(id);
      return el ? { a, el, id } : null;
    })
    .filter(Boolean);

  if (!targets.length) return;

  function setActive(activeId) {
    links.forEach((a) => a.classList.remove("active"));
    const item = targets.find((t) => t.id === activeId);
    if (item) item.a.classList.add("active");
  }

  const OFFSET = 120;

  let ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;

    window.requestAnimationFrame(() => {
      const y = window.scrollY + OFFSET;

      let current = targets[0].id;

      for (const t of targets) {
        const top = t.el.getBoundingClientRect().top + window.scrollY;
        if (top <= y) current = t.id;
        else break;
      }

      setActive(current);
      ticking = false;
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);

  onScroll();

  links.forEach((a) => {
    a.addEventListener("click", () => {
      if (navbarToggler && window.getComputedStyle(navbarToggler).display !== "none") {
        navbarToggler.click();
      }
    });
  });
});
