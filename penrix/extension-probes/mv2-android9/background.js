// Background event page + blocking webRequest API probe.
chrome.runtime.onInstalled.addListener(function () {
  chrome.storage.local.set({ blockedCount: 0, lastBlockedUrl: "" });
});
chrome.webRequest.onBeforeRequest.addListener(
  function (details) {
    chrome.storage.local.get({ blockedCount: 0 }, function (state) {
      chrome.storage.local.set({
        blockedCount: state.blockedCount + 1,
        lastBlockedUrl: details.url
      });
    });
    return { cancel: true };
  },
  { urls: ["https://example.com/penrix-mv2-block-probe/*"], types: ["image"] },
  ["blocking"]
);
