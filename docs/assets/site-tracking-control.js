/**
 * Central control for GA4 on this site: opt-in by default, local opt-out in localStorage.
 * Loads gtag only when tracking is allowed. Exposes window.FptpSiteTracking (singleton).
 */
(function (w, d) {
  "use strict";

  var STORAGE_NO_TRACKING = "fptp_no_tracking";
  var MEASUREMENT_ID = "G-2B0R9F8EFJ";

  function readNoTrackingFlag() {
    try {
      return localStorage.getItem(STORAGE_NO_TRACKING) === "1";
    } catch (err) {
      void err;
      return false;
    }
  }

  function clearFirstPartyGaCookies() {
    var expire = "max-age=0;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    var raw = d.cookie || "";
    var names = raw.split(";").map(function (c) {
      return c.split("=")[0].trim();
    });
    var hn = d.location.hostname || "";
    var dotHost = hn.indexOf(".") > -1 ? "." + hn.replace(/^www\./, "") : "";
    for (var i = 0; i < names.length; i++) {
      var n = names[i];
      if (!n || n.indexOf("_ga") !== 0) continue;
      d.cookie = n + "=;" + expire + ";path=/";
      if (hn) d.cookie = n + "=;" + expire + ";path=/;domain=" + hn;
      if (dotHost) d.cookie = n + "=;" + expire + ";path=/;domain=" + dotHost;
    }
  }

  function noopGtag() {}

  function SiteTrackingControl() {}

  SiteTrackingControl.prototype.isAllowed = function () {
    return !readNoTrackingFlag();
  };

  SiteTrackingControl.prototype.trackEvent = function (eventName, params) {
    if (!this.isAllowed()) return;
    if (typeof w.gtag !== "function") return;
    var p = params && typeof params === "object" ? params : {};
    w.gtag("event", String(eventName), p);
  };

  SiteTrackingControl.prototype.optOut = function () {
    try {
      localStorage.setItem(STORAGE_NO_TRACKING, "1");
    } catch (err) {
      void err;
    }
    clearFirstPartyGaCookies();
    try {
      if (typeof w.gtag === "function" && w.gtag !== noopGtag) {
        w.gtag("consent", "update", {
          analytics_storage: "denied",
          ad_storage: "denied",
        });
      }
    } catch (err2) {
      void err2;
    }
    w.gtag = noopGtag;
    w.location.reload();
  };

  SiteTrackingControl.prototype.optIn = function () {
    try {
      localStorage.removeItem(STORAGE_NO_TRACKING);
    } catch (err) {
      void err;
    }
    w.location.reload();
  };

  SiteTrackingControl.prototype._installGtagIfAllowed = function () {
    if (readNoTrackingFlag()) {
      w.gtag = noopGtag;
      return;
    }
    w.dataLayer = w.dataLayer || [];
    w.gtag = function () {
      w.dataLayer.push(arguments);
    };
    w.gtag("js", new Date());
    w.gtag("config", MEASUREMENT_ID);
    var s = d.createElement("script");
    s.async = true;
    s.src =
      "https://www.googletagmanager.com/gtag/js?id=" +
      encodeURIComponent(MEASUREMENT_ID);
    (d.head || d.documentElement).appendChild(s);
  };

  var singleton = new SiteTrackingControl();
  w.FptpSiteTracking = singleton;
  singleton._installGtagIfAllowed();
})(window, document);
