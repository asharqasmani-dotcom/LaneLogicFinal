(function () {
  var menuBtn = document.querySelector(".header__menu");
  var mobileNav = document.getElementById("mobile-nav");
  if (!menuBtn || !mobileNav) return;

  function closeMenu() {
    menuBtn.setAttribute("aria-expanded", "false");
    mobileNav.hidden = true;
    document.body.classList.remove("menu-open");
  }

  menuBtn.addEventListener("click", function () {
    var isOpen = menuBtn.getAttribute("aria-expanded") === "true";
    menuBtn.setAttribute("aria-expanded", isOpen ? "false" : "true");
    mobileNav.hidden = isOpen;
    document.body.classList.toggle("menu-open", !isOpen);
  });

  mobileNav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeMenu();
  });
})();
