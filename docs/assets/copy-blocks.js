/**
 * Copy-to-clipboard for .copy-block (home + self-audit page).
 * Expects: .copy-block > .copy-block__btn + pre > code
 * Uses event delegation so blocks filled after load (prompt wizard) still work.
 */
(function () {
  "use strict";

  function copyFromButton(btn) {
    var wrap = btn.closest(".copy-block");
    if (!wrap) return;
    var pre = wrap.querySelector("pre");
    if (!pre) return;
    var code = pre.querySelector("code");
    var text = code ? code.textContent : pre.textContent;
    var defaultLabel = btn.getAttribute("aria-label") || "Copy to clipboard";

    function done(ok) {
      btn.classList.toggle("copy-block__btn--copied", ok);
      btn.setAttribute("aria-label", ok ? "Copied" : "Copy failed");
      window.setTimeout(function () {
        btn.setAttribute("aria-label", defaultLabel);
        btn.classList.remove("copy-block__btn--copied");
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
