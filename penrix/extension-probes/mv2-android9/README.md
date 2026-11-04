# MV2 extension smoke probe for Android 9 / Kiwi

This is an unpacked **Manifest V2 Chrome extension** included in the Penrix source solely to test real Android extension behavior. The code uses real `chrome.webRequest.onBeforeRequest` with `["blocking"]`, a persistent MV2 background script, a content script, `browser_action` popup and `chrome.storage.local`.

1. Load the unpacked folder with the browser's extension developer UI *if available*, or package/install a CRX with an independent Chromium toolchain. A ZIP file alone is not guaranteed to be installable in Kiwi.
2. Visit `https://example.com/`. A green badge should say **"Penrix MV2: content script active"**.
3. Open the probe's extension popup and press **Refresh**. The **Blocked by MV2 webRequest** counter should be at least 1.
4. Restart the browser. Visit example.com again, confirm badge and counter persistence. Compare behavior on the independently built Penrix APK.
5. Separately test real **uBlock Origin MV2**, **Tampermonkey/Violentmonkey**, their popups, permissions and script injection.

The image deliberately uses a non-existent URL. An image error is **not proof** of a blocking API: the background counter is the indicator. This test does not assert full compatibility with every Chrome extension.
