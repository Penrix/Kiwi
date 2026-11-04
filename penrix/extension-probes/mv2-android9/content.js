// On example.com, visibly prove that a desktop-style Chrome content script executes.
(function () {
  if (!document.body || document.getElementById("penrix-mv2-probe")) return;
  var badge = document.createElement("div");
  badge.id = "penrix-mv2-probe";
  badge.style.cssText = "position:fixed;z-index:2147483647;bottom:8px;left:8px;padding:8px;background:#083;color:#fff;font:13px sans-serif";
  badge.textContent = "Penrix MV2: content script active";
  document.body.appendChild(badge);

  // This image URL must be canceled by chrome.webRequest.onBeforeRequest in background.js.
  // Its failure alone is NOT proof of blocking: inspect the popup's blocked count too.
  var image = new Image();
  image.style.display = "none";
  image.src = "https://example.com/penrix-mv2-block-probe/" + Date.now() + ".png";
  document.body.appendChild(image);
})();
