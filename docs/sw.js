// Otomatik üretildi (scripts/build_web.py) — elle düzenleme.
const CACHE = 'ppl-offline-937b9d2ec85e';
const FONT_CACHE = 'ppl-fonts-v1';
const CORE = ["./", "./index.html", "./site.webmanifest", "./favicon.svg", "./favicon.ico", "./apple-touch-icon.png", "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png"];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(CORE.map(async url => {
      const res = await fetch(new Request(url, { cache: 'reload' }));
      if (!res.ok) throw new Error('Precache failed: ' + url + ' (' + res.status + ')');
      await cache.put(url, res);
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter(k => k.startsWith('ppl-offline-') && k !== CACHE)
      .map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  const msg = event.data;
  if (!msg || typeof msg !== 'object') return;
  if (msg.type === 'SKIP_WAITING') {
    self.skipWaiting();
    return;
  }
  if (msg.type === 'CACHE_CHECK' && event.ports && event.ports[0]) {
    event.waitUntil((async () => {
      try {
        const cache = await caches.open(CACHE);
        const hit = await cache.match('./index.html', { ignoreSearch: true });
        const keys = await cache.keys();
        event.ports[0].postMessage({ ready: !!hit, version: CACHE, count: keys.length });
      } catch (e) {
        event.ports[0].postMessage({ ready: false, version: CACHE, count: 0 });
      }
    })());
  }
});

function fetchWithTimeout(request, ms) {
  return new Promise((resolve, reject) => {
    let done = false;
    const timer = setTimeout(() => {
      if (!done) { done = true; reject(new Error('timeout')); }
    }, ms);
    fetch(request).then(res => {
      if (!done) { done = true; clearTimeout(timer); resolve(res); }
    }, err => {
      if (!done) { done = true; clearTimeout(timer); reject(err); }
    });
  });
}

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Google Fonts: önbellekten anında sun; çevrimdışıysa hiç bekletme
  if (url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com') {
    event.respondWith((async () => {
      const cache = await caches.open(FONT_CACHE);
      const cached = await cache.match(req);
      if (cached) return cached;
      try {
        const res = await fetchWithTimeout(req, 3000);
        if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone());
        return res;
      } catch (e) {
        return new Response('', { status: 504, statusText: 'Offline' });
      }
    })());
    return;
  }

  // Firebase Auth/Firestore ve diğer dış kaynaklara müdahale etme
  if (url.origin !== self.location.origin) return;
  // sw.js güncelleme denetimi her zaman ağa gitsin
  if (url.pathname.endsWith('/sw.js')) return;

  // Sayfa açılışı: uçak/kötü Wi-Fi'da takılmamak için 2 sn ağ, düşerse anında önbellek
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const res = await fetchWithTimeout(req, 2000);
        if (res && res.ok && res.type === 'basic' && !res.redirected) {
          cache.put('./index.html', res.clone());
          return res;
        }
      } catch (e) {}
      return (await cache.match('./index.html', { ignoreSearch: true }))
        || (await cache.match('./', { ignoreSearch: true }))
        || Response.error();
    })());
    return;
  }

  // Aynı kaynaklı statik dosyalar (ikonlar, manifest, HTML indirme): önce önbellek
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(req, { ignoreSearch: true });
    if (cached) return cached;
    try {
      const res = await fetch(req);
      if (res && res.ok && res.type === 'basic') cache.put(req, res.clone());
      return res;
    } catch (e) {
      return (await cache.match('./index.html', { ignoreSearch: true })) || Response.error();
    }
  })());
});
