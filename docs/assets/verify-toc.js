/**
 * Self-check page: active TOC link from scroll + keep active link visible in sidebar.
 * No dependencies; only loaded on /verify/
 */
(function () {
  "use strict";

  const nav = document.querySelector("#site-toc .on-this-page");
  const main = document.getElementById("main");
  if (!nav || !main) return;

  const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
  if (links.length === 0) return;

  /** @type {{ id: string, link: HTMLAnchorElement, el: HTMLElement }[]} */
  const sections = [];
  for (const a of links) {
    const id = a.getAttribute("href")?.slice(1);
    if (!id) continue;
    const el = document.getElementById(id);
    if (el) sections.push({ id, link: a, el });
  }
  if (sections.length === 0) return;

  function readHeaderOffset() {
    const h = document.querySelector(".site-header");
    return h ? h.getBoundingClientRect().height + 10 : 72;
  }

  let activeId = "";

  function setActive(id) {
    if (id === activeId) return;
    if (!sections.some((s) => s.id === id)) return;
    activeId = id;

    for (const s of sections) {
      const on = s.id === id;
      s.link.classList.toggle("is-active", on);
      if (on) {
        s.link.setAttribute("aria-current", "true");
        try {
          s.link.scrollIntoView({ block: "nearest", behavior: "auto" });
        } catch {
          s.link.scrollIntoView(false);
        }
      } else {
        s.link.removeAttribute("aria-current");
      }
    }
  }

  function computeActiveFromScroll() {
    const y = window.scrollY + readHeaderOffset();
    let current = sections[0];
    for (const s of sections) {
      const top = s.el.getBoundingClientRect().top + window.pageYOffset;
      if (top <= y) current = s;
    }
    setActive(current.id);
  }

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      computeActiveFromScroll();
      ticking = false;
    });
  }

  function applyHash() {
    const hid = (location.hash || "").slice(1);
    if (hid && document.getElementById(hid) && sections.some((s) => s.id === hid)) {
      setActive(hid);
      return;
    }
    computeActiveFromScroll();
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", () => {
    applyHash();
  });
  window.addEventListener("hashchange", applyHash);

  if (location.hash) {
    applyHash();
  } else {
    computeActiveFromScroll();
  }
})();
