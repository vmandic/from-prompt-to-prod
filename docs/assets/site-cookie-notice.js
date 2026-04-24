/**
 * Fixed cookie / analytics control (lower right). Depends on FptpSiteTracking from site-tracking-control.js.
 */
(function (w, d) {
  "use strict";

  var NS = "fptp-cookie";

  function trackSafe(name, params) {
    var t = w.FptpSiteTracking;
    if (t && typeof t.trackEvent === "function") t.trackEvent(name, params);
  }

  function init() {
    var track = w.FptpSiteTracking;
    if (!track || typeof track.isAllowed !== "function") return;

    var root = d.createElement("div");
    root.className = NS + "-widget";

    var toggle = d.createElement("button");
    toggle.type = "button";
    toggle.className = NS + "__fab";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", NS + "-panel");
    toggle.setAttribute("title", "Cookie and analytics choices");
    toggle.setAttribute("aria-label", "Cookie and analytics choices");
    toggle.innerHTML =
      '<svg class="' +
      NS +
      '__icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<circle cx="12" cy="12" r="9.25" fill="none" stroke="currentColor" stroke-width="1.35"/>' +
      '<circle cx="8.5" cy="9" r="1.15" fill="currentColor"/>' +
      '<circle cx="13.5" cy="8.5" r="0.95" fill="currentColor"/>' +
      '<circle cx="11" cy="13" r="0.9" fill="currentColor"/>' +
      '<circle cx="15" cy="13.5" r="0.85" fill="currentColor"/>' +
      '<circle cx="9.5" cy="15" r="0.75" fill="currentColor"/>' +
      "</svg>";

    var panel = d.createElement("div");
    panel.id = NS + "-panel";
    panel.className = NS + "__panel";
    panel.setAttribute("role", "region");
    panel.setAttribute("aria-label", "Analytics and cookies");
    panel.hidden = true;

    var text = d.createElement("div");
    text.className = NS + "__text";

    var optInBtn = d.createElement("button");
    optInBtn.type = "button";
    optInBtn.className = NS + "__action " + NS + "__action--primary";

    var close = d.createElement("button");
    close.type = "button";
    close.className = NS + "__close";
    close.setAttribute("aria-label", "Close");
    close.textContent = "\u00d7";

    function wireInlineOptOut() {
      var inline = text.querySelector("#" + NS + "-inline-opt");
      if (inline) {
        inline.addEventListener("click", function () {
          trackSafe("cookie_notice_opt_out_click", {});
          track.optOut();
        });
      }
    }

    function refreshCopy() {
      text.textContent = "";
      var allowed = track.isAllowed();
      if (allowed) {
        text.innerHTML =
          "Using this site uses <strong>cookies</strong> for anonymous analytics (Google Analytics). " +
          "If you wish not to use tracking cookies, " +
          '<button type="button" class="' +
          NS +
          '__inline-opt" id="' +
          NS +
          '-inline-opt">click here</button>.';
        optInBtn.hidden = true;
        wireInlineOptOut();
      } else {
        text.textContent =
          "Analytics tracking is off for this browser. Your choice is saved locally. " +
          "You can turn analytics cookies back on below.";
        optInBtn.hidden = false;
        optInBtn.textContent = "Allow analytics cookies";
      }
    }

    refreshCopy();

    optInBtn.addEventListener("click", function () {
      trackSafe("cookie_notice_opt_in_click", {});
      track.optIn();
    });

    function setOpen(open) {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) trackSafe("cookie_notice_open", {});
    }

    toggle.addEventListener("click", function () {
      setOpen(panel.hidden);
    });
    close.addEventListener("click", function () {
      setOpen(false);
    });
    d.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && !panel.hidden) setOpen(false);
    });

    panel.appendChild(close);
    panel.appendChild(text);
    panel.appendChild(optInBtn);

    root.appendChild(panel);
    root.appendChild(toggle);
    d.body.appendChild(root);
  }

  if (d.readyState === "loading") {
    d.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(window, document);
