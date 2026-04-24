/**
 * Self-audit page: active TOC link from scroll + keep active link visible in sidebar.
 * Desktop only (min-width: 64em) — on narrow viewports the ToC is hidden; without this,
 * scrollIntoView on hidden ToC links breaks mobile scrolling.
 * No dependencies; only loaded on /self-audit/ (legacy /verify/ redirects).
 */
(function () {
  "use strict";

  /**
   * Mobile “pivot” tables: set data-label on each body cell from the thead row so CSS can stack rows.
   * Runs for all .md-body tables with a single header row; no effect if thead is missing.
   */
  (function initMdResponsiveTables() {
    function normText(s) {
      return String(s).replace(/\s+/g, " ").trim();
    }
    for (const table of document.querySelectorAll(".md-body table")) {
      const headerRow = table.querySelector("thead tr");
      if (!headerRow) continue;
      const thEls = headerRow.querySelectorAll("th");
      if (thEls.length === 0) continue;
      const labels = Array.from(thEls, (th) => normText(th.textContent));
      for (const tr of table.querySelectorAll("tbody tr")) {
        tr.querySelectorAll("td").forEach((td, i) => {
          if (i < labels.length) td.setAttribute("data-label", labels[i]);
        });
      }
    }
  })();

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

  /**
   * Y-offset from the top of the viewport: the “reading line” for scroll-spy and hash scroll.
   * Must be >= the resolved scroll-margin on `.md-body` headings (base.css) or the sticky header
   * wins and the *previous* section stays highlighted/“active” after clicking the ToC.
   */
  function readHeaderOffset() {
    const h = document.querySelector(".site-header");
    const headerH = h ? Math.ceil(h.getBoundingClientRect().height) : 72;
    let marginPx = 0;
    const sample = sections[0]?.el;
    if (sample) {
      const sm = getComputedStyle(sample).scrollMarginTop;
      if (sm) marginPx = Math.ceil(parseFloat(sm) || 0);
    }
    if (!marginPx) {
      const rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
      marginPx = Math.ceil(5 * rem);
    }
    return Math.max(headerH + SCROLL_SPY_GUTTER_PX, marginPx);
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
    const ro = readHeaderOffset();
    let current = sections[0];
    for (const s of sections) {
      // Viewport space: last heading whose top is at/above the spy line (same as document logic).
      if (s.el.getBoundingClientRect().top <= ro) current = s;
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
