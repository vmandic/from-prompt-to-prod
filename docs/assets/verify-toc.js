/**
 * Self-check page: active TOC link from scroll + keep active link visible in sidebar.
 * Desktop only (min-width: 64em) — on narrow viewports the ToC is hidden; without this,
 * scrollIntoView on hidden ToC links breaks mobile scrolling.
 * No dependencies; only loaded on /verify/
 */
(function () {
  "use strict";

  const mql = window.matchMedia("(min-width: 64em)");
  const nav = document.querySelector("#site-toc .on-this-page");
  if (!nav) return;

  /** Pixels under sticky header for “which heading is current” (aligns with --site-toc-sticky-top + small gutter). */
  const SCROLL_SPY_GUTTER_PX = 8;

  const sections = [];

  /** Set --site-toc-sticky-top to measured .site-header height (px) so max-height = visible − header − gap. */
  function syncTocLayoutVars() {
    if (!mql.matches) {
      document.documentElement.style.removeProperty("--site-toc-sticky-top");
      return;
    }
    const el = document.querySelector(".site-header");
    if (!el) return;
    const h = Math.ceil(el.getBoundingClientRect().height);
    document.documentElement.style.setProperty("--site-toc-sticky-top", h + "px");
  }

  function buildSections() {
    sections.length = 0;
    const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
    for (const a of links) {
      const id = a.getAttribute("href")?.slice(1);
      if (!id) continue;
      const el = document.getElementById(id);
      if (el) sections.push({ id, link: a, el });
    }
  }

  function readHeaderOffset() {
    const h = document.querySelector(".site-header");
    if (!h) return 72;
    // Same source as syncTocLayoutVars (px height) + gutter to align with scroll spy vs sticky bar
    return Math.ceil(h.getBoundingClientRect().height) + SCROLL_SPY_GUTTER_PX;
  }

  let activeId = "";
  let bound = false;
  /** @type {ResizeObserver | null} */
  let headerResizeObserver = null;

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
    if (!mql.matches) return;
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      computeActiveFromScroll();
      ticking = false;
    });
  }

  function applyHash() {
    if (!mql.matches) return;
    const hid = (location.hash || "").slice(1);
    if (hid && document.getElementById(hid) && sections.some((s) => s.id === hid)) {
      setActive(hid);
      return;
    }
    computeActiveFromScroll();
  }

  function onResize() {
    syncTocLayoutVars();
    if (!mql.matches) return;
    applyHash();
  }

  function onHash() {
    applyHash();
  }

  const scrollOpts = { passive: true };

  function unbindToc() {
    if (!bound) return;
    if (headerResizeObserver) {
      headerResizeObserver.disconnect();
      headerResizeObserver = null;
    }
    window.removeEventListener("scroll", onScroll, scrollOpts);
    window.removeEventListener("resize", onResize);
    window.removeEventListener("hashchange", onHash);
    for (const s of sections) {
      s.link.classList.remove("is-active");
      s.link.removeAttribute("aria-current");
    }
    activeId = "";
    bound = false;
    syncTocLayoutVars();
  }

  function bindToc() {
    if (bound) return;
    buildSections();
    if (sections.length === 0) return;
    syncTocLayoutVars();
    const siteHeader = document.querySelector(".site-header");
    if (siteHeader && typeof ResizeObserver !== "undefined") {
      headerResizeObserver = new ResizeObserver(function () {
        if (mql.matches) {
          syncTocLayoutVars();
        }
      });
      headerResizeObserver.observe(siteHeader);
    }
    window.addEventListener("scroll", onScroll, scrollOpts);
    window.addEventListener("resize", onResize);
    window.addEventListener("hashchange", onHash);
    bound = true;
    if (location.hash) {
      applyHash();
    } else {
      computeActiveFromScroll();
    }
  }

  function applyMql() {
    if (mql.matches) {
      bindToc();
    } else {
      unbindToc();
    }
  }

  if (mql.addEventListener) {
    mql.addEventListener("change", applyMql);
  } else {
    mql.addListener(applyMql);
  }
  applyMql();
})();
