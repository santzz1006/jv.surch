/* H3X Search: runs in <head> on /, /en/ and /zh/ before first paint (a classic script file, no
   inline JS, so it passes the CSP script-src 'self').
   1. /en/ and /zh/ are language landings. On a first visit (no language saved yet) the landing's
      language is saved under the key the language switcher uses ("h3x.lang"), so detectLang() in
      src/i18n.tsx boots the app in it instead of the browser language (this is what crawlers get).
   2. The HTML holds a prerendered first frame of the app in the page's language. If this visit
      boots in another language, or straight into a search (?q=), that frame is hidden so React's
      first render never swaps visible content.
   The language order mirrors detectLang(): ?lang= > saved choice > browser language. Keep in sync. */
(function () {
  var d = document.documentElement;
  var pre = d.getAttribute("data-pre-lang");
  if (!pre) return;
  var ok = function (v) {
    return v === "pt" || v === "en" || v === "zh";
  };
  var p = new URLSearchParams(location.search);
  var seg = location.pathname.split("/")[1];
  var lang = p.get("lang");
  // Only when no language was chosen yet: otherwise picking PT on /en/ and reloading would flip
  // back to English. (Once detectLang() reads the path itself, this block can go.)
  if (!ok(lang) && ok(seg)) {
    try {
      if (!ok(localStorage.getItem("h3x.lang"))) localStorage.setItem("h3x.lang", seg);
    } catch (e) {
      /* storage blocked: the app falls back to the browser language */
    }
  }
  if (!ok(lang)) {
    try {
      lang = localStorage.getItem("h3x.lang");
    } catch (e) {
      lang = null;
    }
  }
  if (!ok(lang)) {
    var nav = navigator.languages && navigator.languages[0] ? navigator.languages[0] : navigator.language || "";
    nav = nav.toLowerCase();
    lang = nav.indexOf("pt") === 0 ? "pt" : nav.indexOf("zh") === 0 ? "zh" : "en";
  }
  if (lang !== pre) d.classList.add("pre-lang");
  if ((p.get("q") || "").trim()) d.classList.add("pre-q");
})();
