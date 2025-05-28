const CACHE_NAME = 'openlibrary-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/static/manifest.json',
  '/imgs/icon-192.png',
  '/imgs/icon-512.png',
  'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
