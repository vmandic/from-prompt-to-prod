/**
 * GA4 custom events for the static site. Requires gtag in <head>; no-op if absent.
 * Loaded with defer before other site scripts so fptpTrack exists for their init.
 */
(function (w) {
  "use strict";

  function fptpTrack(eventName, params) {
    if (typeof w.gtag !== "function") return;
    var p = params && typeof params === "object" ? params : {};
    w.gtag("event", eventName, p);
  }
  w.fptpTrack = fptpTrack;

  function initNavTracking() {
    var nav = document.querySelector(".site-nav");
    if (!nav) return;
    nav.addEventListener("click", function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest("a") : null;
      if (!a || !nav.contains(a)) return;
      var href = a.getAttribute("href") || "";
      var label = (a.textContent || "").replace(/\s+/g, " ").trim();
      if (!href) return;
      fptpTrack("nav_click", {
        nav_href: href.slice(0, 240),
        link_text: label.slice(0, 120),
      });
    });
  }

  /** One-shot when the self-audit article is mostly read (scroll) or fits in one screen. */
  function initAuditScrollEnd() {
    var main = document.getElementById("main");
    if (!main || !main.classList.contains("site-main--audit")) return;

    var fired = false;
    var opts = { passive: true };

    function fire(extra) {
      if (fired) return;
      fired = true;
      w.removeEventListener("scroll", onScroll, opts);
      fptpTrack("audit_page_scroll_end", extra || {});
    }

    function measure() {
      if (fired) return;
      var doc = document.documentElement;
      var total = doc.scrollHeight - w.innerHeight;
      if (total <= 24) {
        fire({ engagement_type: "full_page_visible" });
        return;
      }
      var y = w.scrollY || doc.scrollTop;
      if (y >= total * 0.92) {
        fire({
          engagement_type: "scrolled_near_end",
          scroll_depth_ratio: Math.round((y / Math.max(doc.scrollHeight, 1)) * 100) / 100,
        });
      }
    }

    var t = 0;
    function onScroll() {
      if (fired) return;
      if (t) return;
      t = w.requestAnimationFrame(function () {
        t = 0;
        measure();
      });
    }

    w.addEventListener("scroll", onScroll, opts);
    measure();
  }

  function boot() {
    initNavTracking();
    initAuditScrollEnd();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(window);
