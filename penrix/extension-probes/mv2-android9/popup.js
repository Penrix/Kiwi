function refresh() {
  chrome.storage.local.get({ blockedCount: 0, lastBlockedUrl: "" }, function (result) {
    document.getElementById("status").textContent =
      "Blocked by MV2 webRequest: " + result.blockedCount +
      "\nLast URL: " + (result.lastBlockedUrl || "(none)");
  });
}
document.getElementById("refresh").addEventListener("click", refresh);
refresh();
