/**
 * Copy-to-clipboard for .copy-block (home + self-audit page).
 * Expects: .copy-block > .copy-block__btn + pre > code
 * Uses event delegation so blocks filled after load (prompt wizard) still work.
 */
(function () {
  "use strict";

  function copySourceForAnalytics(wrap) {
    if (!wrap) return "unknown";
    if (wrap.closest("#prompt-wizard-result")) return "generated_prompt";
    if (wrap.closest(".prompt-wizard__examples-inner")) return "example_prompt";
    if (wrap.closest(".md-body")) return "rubric";
    return "other";
  }

  function copyFromButton(btn) {
    var wrap = btn.closest(".copy-block");
    if (!wrap) return;
    var pre = wrap.querySelector("pre");
    if (!pre) return;
    var code = pre.querySelector("code");
    var text = code ? code.textContent : pre.textContent;
    var defaultLabel = btn.getAttribute("aria-label") || "Copy to clipboard";
    var defaultTitle = btn.getAttribute("title") || "Copy";

    function done(ok) {
      if (ok && typeof window.fptpTrack === "function") {
        window.fptpTrack("code_copy", { copy_source: copySourceForAnalytics(wrap) });
      }
      btn.classList.toggle("copy-block__btn--copied", ok);
      if (wrap) wrap.classList.toggle("copy-block--copied", Boolean(ok));
      btn.setAttribute("aria-label", ok ? "Copied" : "Copy failed");
      btn.setAttribute("title", ok ? "Copied!" : "Copy failed");
      window.setTimeout(function () {
        btn.setAttribute("aria-label", defaultLabel);
        btn.setAttribute("title", defaultTitle);
        btn.classList.remove("copy-block__btn--copied");
        if (wrap) wrap.classList.remove("copy-block--copied");
      }, ok ? 1800 : 2400);
    }
    function copyViaExecCommand() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try {
        ok = document.execCommand("copy");
      } catch (e) {
        void e;
        ok = false;
      }
      document.body.removeChild(ta);
      return ok;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () {
          done(true);
        },
        function () {
          done(copyViaExecCommand());
        }
      );
    } else {
      done(copyViaExecCommand());
    }
  }

  function onDocClick(ev) {
    var btn = ev.target && ev.target.closest ? ev.target.closest(".copy-block__btn") : null;
    if (!btn || !document.body.contains(btn)) return;
    ev.preventDefault();
    copyFromButton(btn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      document.addEventListener("click", onDocClick);
    });
  } else {
    document.addEventListener("click", onDocClick);
  }
})();
