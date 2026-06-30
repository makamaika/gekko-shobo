/* 月光書房 — reader controls: theme, vertical writing, font size. Persisted in localStorage. */
(function () {
  "use strict";
  var KEY = "gekko-prefs";
  var prefs = { theme: "night", tategaki: false, fs: 1 };
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || "{}");
    if (saved && typeof saved === "object") {
      if (saved.theme) prefs.theme = saved.theme;
      if (typeof saved.tategaki === "boolean") prefs.tategaki = saved.tategaki;
      if (typeof saved.fs === "number") prefs.fs = saved.fs;
    }
  } catch (e) {}

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch (e) {}
  }

  function applyTheme() {
    document.documentElement.setAttribute("data-theme", prefs.theme === "sepia" ? "sepia" : "night");
    var b = document.querySelector('[data-action="theme"]');
    if (b) {
      b.setAttribute("aria-pressed", prefs.theme === "sepia" ? "true" : "false");
      b.textContent = prefs.theme === "sepia" ? "☾ 夜" : "☀ 紙";
    }
  }
  function applyTategaki() {
    var r = document.querySelector(".reader");
    if (r) r.classList.toggle("tategaki", !!prefs.tategaki);
    var b = document.querySelector('[data-action="tategaki"]');
    if (b) {
      b.setAttribute("aria-pressed", prefs.tategaki ? "true" : "false");
      b.textContent = prefs.tategaki ? "横書き" : "縦書き";
    }
  }
  function applyFs() {
    document.documentElement.style.setProperty("--fs", String(prefs.fs));
  }

  document.addEventListener("click", function (ev) {
    var t = ev.target.closest ? ev.target.closest("[data-action]") : null;
    if (!t) return;
    var a = t.getAttribute("data-action");
    if (a === "theme") { prefs.theme = prefs.theme === "sepia" ? "night" : "sepia"; applyTheme(); save(); }
    else if (a === "tategaki") { prefs.tategaki = !prefs.tategaki; applyTategaki(); save(); }
    else if (a === "fs-up") { prefs.fs = Math.min(1.5, Math.round((prefs.fs + 0.1) * 10) / 10); applyFs(); save(); }
    else if (a === "fs-down") { prefs.fs = Math.max(0.8, Math.round((prefs.fs - 0.1) * 10) / 10); applyFs(); save(); }
  });

  applyTheme();
  applyFs();
  document.addEventListener("DOMContentLoaded", applyTategaki);
  if (document.readyState !== "loading") applyTategaki();
})();
