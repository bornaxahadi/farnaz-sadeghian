const CACHE = 'tsi-v31';
const ASSETS = ['./', 'index.html', 'manifest.webmanifest', 'img/farnaz-hero.jpg', 'img/farnaz-portrait.jpg', 'img/farnaz-rugs.jpg', 'img/icon-192.png', 'img/icon.svg', 'img/tsi-mark.svg'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); if (new URL(e.request.url).origin === location.origin) caches.open(CACHE).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request)));
});
