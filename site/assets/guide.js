// Theme, citation proofs, contents highlighting and copy buttons.
// Every page works without this file: citations fall back to links into sources.html.
(function () {
  "use strict";

  var root = document.documentElement;

  function store(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, value);
    } catch (e) {
      return null;
    }
  }

  // Theme: follows the system until the reader picks one.
  var saved = store("daf-theme");
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  var themeBtn = document.querySelector(".theme");
  function currentTheme() {
    var set = root.getAttribute("data-theme");
    if (set) return set;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function labelTheme() {
    if (themeBtn) themeBtn.textContent = currentTheme() === "dark" ? "Light" : "Dark";
  }
  if (themeBtn) {
    labelTheme();
    themeBtn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store("daf-theme", next);
      labelTheme();
    });
  }

  function toast(text) {
    var el = document.querySelector(".toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = text;
    el.classList.add("show");
    clearTimeout(el._t);
    el._t = setTimeout(function () { el.classList.remove("show"); }, 1800);
  }

  // Citations: show the exact passage under the paragraph it supports.
  var dataEl = document.getElementById("evidence-data");
  var data = dataEl ? JSON.parse(dataEl.textContent) : null;

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  }

  function buildProof(ids) {
    var box = el("div", "proof");
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Source passages");
    var close = el("button", "close", "close");
    close.type = "button";
    box.appendChild(close);
    ids.forEach(function (id) {
      var ev = data.evidence[id];
      if (!ev) return;
      var src = data.sources[ev.s];
      var q = el("blockquote");
      q.appendChild(document.createTextNode("“" + ev.q + "”"));
      var cite = el("span", "psrc");
      cite.appendChild(document.createTextNode("[" + ev.s + "] " + src.publisher + ", " + src.title + " · " + ev.at + " · "));
      var a = el("a", null, "open source");
      a.href = src.url;
      a.rel = "noopener";
      cite.appendChild(a);
      cite.appendChild(document.createTextNode(" · "));
      var copy = el("a", null, "saved copy");
      copy.href = "source-copies/" + src.file;
      cite.appendChild(copy);
      q.appendChild(cite);
      box.appendChild(q);
    });
    return box;
  }

  if (data) {
    document.addEventListener("click", function (e) {
      var btn = e.target.closest(".cite");
      var closer = e.target.closest(".proof .close");
      if (closer) {
        var p = closer.parentNode;
        if (p._btn) { p._btn.setAttribute("aria-expanded", "false"); p._btn.focus(); }
        p.remove();
        return;
      }
      if (!btn) return;
      e.preventDefault();
      var host = btn.closest("p, li, td, dd, .qa li") || btn.parentNode;
      if (btn._proof && btn._proof.isConnected) {
        btn._proof.remove();
        btn.setAttribute("aria-expanded", "false");
        return;
      }
      var box = buildProof(btn.getAttribute("data-ev").split(" "));
      box._btn = btn;
      btn._proof = box;
      btn.setAttribute("aria-expanded", "true");
      if (host.tagName === "TD") host.appendChild(box);
      else host.parentNode.insertBefore(box, host.nextSibling);
    });
  }

  // Contents: mark the chapter being read.
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (links.length && "IntersectionObserver" in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove("on"); });
        var a = byId[entry.target.id];
        if (a) a.classList.add("on");
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(byId).forEach(function (id) {
      var s = document.getElementById(id);
      if (s) obs.observe(s);
    });
  }

  // Copy buttons on the summary page.
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var t = el("textarea");
      t.value = text;
      t.setAttribute("readonly", "");
      t.style.position = "absolute";
      t.style.left = "-9999px";
      document.body.appendChild(t);
      t.select();
      try { document.execCommand("copy") ? resolve() : reject(); } catch (err) { reject(err); }
      t.remove();
    });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    var src = document.getElementById(b.getAttribute("data-copy"));
    if (!src) return;
    copyText(src.getAttribute("data-text") || src.innerText).then(
      function () { toast("Copied"); },
      function () { toast("Copy failed. Select the text instead."); }
    );
  });
})();
