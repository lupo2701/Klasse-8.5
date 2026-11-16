/* Offline-Speicher der Lern-App. Erst Netz, sonst Kopie aus dem Speicher: so kommen Updates sofort an. */
const CACHE = "klasse85-v3";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-180.png", "mathe/index.html", "mathe/css/style.css", "mathe/js/app.js", "mathe/js/content.js", "mathe/js/core.js", "mathe/js/tasks.js", "nawi/index.html", "nawi/css/style.css", "nawi/js/app.js", "nawi/js/data.js", "nawi/js/figures.js", "nawi/js/zucker.js", "englisch/index.html"];
self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).catch(() => {}));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  e.respondWith(
    fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then((hit) => hit || (req.mode === "navigate" ? caches.match("index.html") : Response.error())))
  );
});
