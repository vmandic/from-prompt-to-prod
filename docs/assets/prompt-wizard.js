/**
 * Self-audit page: build starter prompt from #prompt-wizard-data (JSON from build).
 */
(function () {
  "use strict";

  function text(el, s) {
    if (el) el.textContent = s;
  }

  function show(el, on) {
    if (!el) return;
    if (on) el.removeAttribute("hidden");
    else el.setAttribute("hidden", "hidden");
  }

  function init() {
    var dataEl = document.getElementById("prompt-wizard-data");
    if (!dataEl || !dataEl.textContent) return;

    var cfg;
    try {
      cfg = JSON.parse(dataEl.textContent);
    } catch (e) {
      void e;
      return;
    }

    var start = document.getElementById("prompt-wizard-start");
    var panel = document.getElementById("prompt-wizard-panel");
    var modeCw = document.getElementById("prompt-wizard-mode-cw");
    var modeProj = document.getElementById("prompt-wizard-mode-proj");
    var modeHint = document.getElementById("prompt-wizard-mode-hint");
    var pathLabel = document.getElementById("prompt-wizard-path-label");
    var pathInput = document.getElementById("prompt-wizard-path");
    var toolsRoot = document.getElementById("prompt-wizard-tools");
    var otherInput = document.getElementById("prompt-wizard-other-tools");
    var yearsRoot = document.getElementById("prompt-wizard-years");
    var skillsRoot = document.getElementById("prompt-wizard-skills");
    var genBtn = document.getElementById("prompt-wizard-generate");
    var errEl = document.getElementById("prompt-wizard-err");
    var result = document.getElementById("prompt-wizard-result");
    var outCode = document.getElementById("prompt-wizard-output-code");
    var live = document.getElementById("prompt-wizard-live");

    if (!start || !panel || !toolsRoot || !yearsRoot || !skillsRoot || !genBtn || !outCode) return;

    var mode = "computer";

    function setMode(next) {
      mode = next;
      var isCw = mode === "computer";
      if (modeCw && modeProj) {
        modeCw.classList.toggle("prompt-wizard__mode-btn--active", isCw);
        modeProj.classList.toggle("prompt-wizard__mode-btn--active", !isCw);
        modeCw.setAttribute("aria-pressed", isCw ? "true" : "false");
        modeProj.setAttribute("aria-pressed", isCw ? "false" : "true");
      }
      if (modeHint) {
        text(
          modeHint,
          isCw
            ? "Audit across your machine; put your usual source root (for example $HOME/work) in the path field."
            : "One project only; put an absolute path to the repo root in the path field."
        );
      }
      if (pathLabel) {
        text(
          pathLabel,
          isCw ? "Source(s) path" : "Project checkout path"
        );
      }
      if (pathInput) {
        pathInput.placeholder = isCw
          ? "$HOME/work, or several roots separated by spaces or commas"
          : "/absolute/path/to/your/repo";
      }
    }

    if (modeCw) modeCw.addEventListener("click", function () { setMode("computer"); });
    if (modeProj) modeProj.addEventListener("click", function () { setMode("project"); });

    function fillYears() {
      yearsRoot.innerHTML = "";
      var ys = cfg.years || [];
      var name = "prompt-wizard-years";
      ys.forEach(function (y, i) {
        var id = "prompt-wizard-year-" + y.value;
        var wrap = document.createElement("div");
        wrap.className = "prompt-wizard__year";
        var rd = document.createElement("input");
        rd.type = "radio";
        rd.name = name;
        rd.id = id;
        rd.value = y.value;
        if (i === 0) rd.checked = true;
        var lab = document.createElement("label");
        lab.htmlFor = id;
        lab.textContent = y.label;
        wrap.appendChild(rd);
        wrap.appendChild(lab);
        yearsRoot.appendChild(wrap);
      });
    }

    function fillTools() {
      toolsRoot.innerHTML = "";
      (cfg.tools || []).forEach(function (t) {
        var id = "prompt-wizard-tool-" + t.id;
        var wrap = document.createElement("div");
        wrap.className = "prompt-wizard__tool";
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.id = id;
        cb.value = t.id;
        cb.dataset.toolId = t.id;
        var lab = document.createElement("label");
        lab.htmlFor = id;
        lab.textContent = t.label;
        wrap.appendChild(cb);
        wrap.appendChild(lab);
        toolsRoot.appendChild(wrap);
      });
    }

    function fillSkills() {
      skillsRoot.innerHTML = "";
      var presets = cfg.skillsPresets || [];
      var name = "prompt-wizard-skills";
      presets.forEach(function (p, i) {
        var id = "prompt-wizard-skill-" + p.id;
        var wrap = document.createElement("div");
        wrap.className = "prompt-wizard__preset";
        var rd = document.createElement("input");
        rd.type = "radio";
        rd.name = name;
        rd.id = id;
        rd.value = p.id;
        if (i === 0) rd.checked = true;
        var lab = document.createElement("label");
        lab.htmlFor = id;
        lab.textContent = p.label;
        wrap.appendChild(rd);
        wrap.appendChild(lab);
        skillsRoot.appendChild(wrap);
      });
    }

    function selectedToolIds() {
      var order = {};
      (cfg.tools || []).forEach(function (t, idx) {
        order[t.id] = idx;
      });
      var ids = [];
      toolsRoot.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
        if (cb.checked) ids.push(cb.dataset.toolId || cb.value);
      });
      ids.sort(function (a, b) {
        return (order[a] != null ? order[a] : 99) - (order[b] != null ? order[b] : 99);
      });
      return ids;
    }

    function toolsPhrase() {
      var ids = selectedToolIds();
      var extra = otherInput ? otherInput.value.trim() : "";
      var fromBoxes = ids.length ? ids.join(", ") : "";
      if (fromBoxes && extra) return fromBoxes + ", " + extra;
      if (fromBoxes) return fromBoxes;
      return extra;
    }

    function selectedYearPhrase() {
      var rd = yearsRoot.querySelector('input[name="prompt-wizard-years"]:checked');
      var v = rd ? rd.value : "";
      var ys = cfg.years || [];
      for (var i = 0; i < ys.length; i++) {
        if (ys[i].value === v) return ys[i].phrase || "";
      }
      return ys.length && ys[0].phrase ? ys[0].phrase : "less than 1 year";
    }

    function selectedSkillsText() {
      var rd = skillsRoot.querySelector('input[name="prompt-wizard-skills"]:checked');
      if (!rd) return "";
      var ps = cfg.skillsPresets || [];
      for (var j = 0; j < ps.length; j++) {
        if (ps[j].id === rd.value) return ps[j].text || "";
      }
      return "";
    }

    function compose() {
      var opening =
        mode === "project" ? cfg.openingProject : cfg.openingComputerWide;
      var dir = (pathInput && pathInput.value) ? pathInput.value.trim() : "";
      var tools = toolsPhrase();
      var nYears = selectedYearPhrase();
      var skillsMcp = selectedSkillsText();
      var tpl = cfg.bodyTemplate || "";
      return (
        opening +
        tpl
          .replace(/__DIR__/g, dir)
          .replace(/__TOOLS__/g, tools)
          .replace(/__N_YEARS__/g, nYears)
          .replace(/__SKILLS_MCP__/g, skillsMcp)
          .replace(/__RUBRIC_URL__/g, cfg.rubricRawUrl || "")
      );
    }

    start.addEventListener("click", function () {
      if (typeof window.fptpTrack === "function") {
        window.fptpTrack("prompt_wizard_start", {});
      }
      fillYears();
      fillTools();
      fillSkills();
      setMode(mode);
      show(panel, true);
      show(start, false);
      if (pathInput) pathInput.focus();
    });

    genBtn.addEventListener("click", function () {
      show(errEl, false);
      if (pathInput) pathInput.value = pathInput.value.trim();
      var dir = pathInput ? pathInput.value : "";
      if (!dir) {
        if (errEl) {
          text(errEl, "Enter a path (source root or project checkout).");
          show(errEl, true);
        }
        return;
      }
      var tools = toolsPhrase();
      if (!tools) {
        if (errEl) {
          text(
            errEl,
            "Pick at least one daily tool checkbox, or type your tools in Other tools (or both)."
          );
          show(errEl, true);
        }
        return;
      }
      var out = compose();
      text(outCode, out);
      show(result, true);
      if (typeof window.fptpTrack === "function") {
        var skillRd = skillsRoot.querySelector('input[name="prompt-wizard-skills"]:checked');
        window.fptpTrack("prompt_wizard_generate", {
          wizard_mode: mode,
          tools_count: selectedToolIds().length,
          skills_preset: skillRd ? String(skillRd.value).slice(0, 64) : "",
        });
      }
      if (live) text(live, "Starter prompt generated. Use Copy to place it in your agent.");
      try {
        outCode.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } catch (e) {
        void e;
      }
    });

    setMode("computer");

    var exDetails = document.querySelector(".prompt-wizard__examples-details");
    if (exDetails && typeof window.fptpTrack === "function") {
      exDetails.addEventListener("toggle", function () {
        if (exDetails.open) {
          window.fptpTrack("prompt_wizard_examples_open", {});
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
