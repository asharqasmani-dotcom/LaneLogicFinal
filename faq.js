(function () {
  "use strict";

  var PLUS_ICON = "assets/faq/faq-plus.png?v=1";

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatAnswer(answer) {
    return answer
      .split(/\n{2,}/)
      .map(function (block) {
        return "<p>" + escapeHtml(block.trim()).replace(/\n/g, " ") + "</p>";
      })
      .join("");
  }

  function renderItem(categoryId, item) {
    var panelId = "faq-" + categoryId + "-a" + item.number;
    return (
      '<div class="faq-item">' +
      '<button type="button" class="faq-item__trigger" aria-expanded="false" aria-controls="' +
      panelId +
      '">' +
      '<span class="faq-item__num">' +
      item.number +
      ".</span>" +
      '<span class="faq-item__q">' +
      escapeHtml(item.question) +
      "</span>" +
      '<img class="faq-item__plus" src="' +
      PLUS_ICON +
      '" alt="" width="20" height="20" />' +
      "</button>" +
      '<div class="faq-item__panel" id="' +
      panelId +
      '" hidden>' +
      '<div class="faq-item__answer">' +
      formatAnswer(item.answer) +
      "</div>" +
      "</div>" +
      "</div>"
    );
  }

  function renderCategory(category) {
    return (
      '<section class="faq-category" id="faq-' +
      category.id +
      '" aria-labelledby="faq-' +
      category.id +
      '-title">' +
      '<div class="faq-category__head">' +
      '<img class="faq-category__icon" src="' +
      category.icon +
      '?v=1" alt="' +
      escapeHtml(category.iconAlt) +
      '" width="120" height="120" loading="lazy" />' +
      '<div class="faq-category__intro">' +
      '<h2 class="faq-category__title" id="faq-' +
      category.id +
      '-title">' +
      escapeHtml(category.title) +
      "</h2>" +
      '<p class="faq-category__desc">' +
      escapeHtml(category.description) +
      "</p>" +
      "</div>" +
      "</div>" +
      '<div class="faq-category__list">' +
      category.items
        .map(function (item) {
          return renderItem(category.id, item);
        })
        .join("") +
      "</div>" +
      "</section>"
    );
  }

  function bindAccordions(root) {
    root.querySelectorAll(".faq-item__trigger").forEach(function (button) {
      button.addEventListener("click", function () {
        var expanded = button.getAttribute("aria-expanded") === "true";
        var panel = document.getElementById(button.getAttribute("aria-controls"));
        if (!panel) return;

        button.setAttribute("aria-expanded", expanded ? "false" : "true");
        panel.hidden = expanded;
        button.classList.toggle("faq-item__trigger--open", !expanded);
      });
    });
  }

  function injectJsonLd(data) {
    var entities = [];

    data.forEach(function (category) {
      category.items.forEach(function (item) {
        entities.push({
          "@type": "Question",
          name: item.question,
          acceptedAnswer: {
            "@type": "Answer",
            text: item.answer,
          },
        });
      });
    });

    var script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(
      {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        mainEntity: entities,
      },
      null,
      0
    );
    document.head.appendChild(script);
  }

  function init() {
    var mount = document.getElementById("faq-categories");
    if (!mount || !window.FAQ_DATA) return;

    mount.innerHTML = window.FAQ_DATA.map(renderCategory).join("");
    bindAccordions(mount);
    injectJsonLd(window.FAQ_DATA);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
