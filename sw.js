/* ═══════════════════════════════════════════════════════════════
   v1.0.1 2026-10-30 — 아이콘 교체(업로드 로고 ARCHITECT) · 설치 이름 「건축 통합포털」 · 캐시명 v1.0.1
   v1.0.0 2026-10-30 — 신설 (기계설비 통합 포털 mech-portal v1.0.2 sw 구조 계승)
   Service Worker — 건축 계산서 통합 포털 · Engineer Kim Manmin
═══════════════════════════════════════════════════════════════ */

const PREFIX       = 'manmin-arch-portal-';   /* 다른 도구 캐시와 분리(동일 origin 40여 종) */
/* ═ R25 (2026-09-04) — SW 캐시 origin 오염 차단 (S10 · 지시서 §21-1 R25)
   전역 caches 의 match 는 origin 전체를 검색한다. manminkim-eng.github.io 는 34종이 한 origin 이라
   다른 도구 캐시의 opaque 응답이 <script crossorigin>(cors) 요청에 돌아가 스크립트가 폐기됐다
   (30 #root 빈 화면 · 40 html2canvas undefined). 자기 접두어 캐시만 조회하고, cross-origin
   프리캐시는 cors 로 받으며, opaque↔cors 불일치 시 캐시를 쓰지 않는다. */
const MM_EXCLUDE = [];   /* 내 접두어로 시작하지만 남의 캐시인 이름 (§17-1 충돌) */
const mmOwn   = (k) => k.indexOf(PREFIX) === 0 && !MM_EXCLUDE.some((x) => k.indexOf(x) === 0);
const mmReq   = (u) => (typeof u === 'string' && u.indexOf('http') === 0) ? new Request(u, { mode: 'cors' }) : u;
const mmMatch = (req, opt) => caches.keys()
  .then((ks) => ks.filter(mmOwn))
  .then((ks) => ks.reduce((p, k) => p.then((r) => r || caches.open(k).then((c) => c.match(req, opt))), Promise.resolve(undefined)))
  .then((r) => (r && r.type === 'opaque' && req && req.mode === 'cors') ? undefined : r);

const CACHE_NAME   = 'manmin-arch-portal-v1.0.1';
const STATIC_CACHE = 'manmin-arch-portal-static-v1.0.1';

const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png',
  './icons/favicon-32.png',
  './icons/favicon-16.png',
  './icons/favicon.ico',
  /* 로컬 폴백 폰트 — CDN 차단·오프라인 시 한글 깨짐 방지 */
  './assets/fonts/manmin-fonts.css',
  './assets/fonts/NotoSansKR-var.woff2',
];

/* ── INSTALL ── */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing arch-portal-v1.0.1...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => Promise.allSettled(PRECACHE_URLS.map((u) => cache.add(mmReq(u)).catch((e) => console.warn('[SW] precache skip:', u, e)))).catch((e) => console.warn('[SW] Pre-cache 일부 실패:', e)))
      .then(() => self.skipWaiting())
  );
});

/* ── ACTIVATE : 구버전 캐시 정리 ── */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k !== CACHE_NAME && k !== STATIC_CACHE && mmOwn(k))
            .map((k) => { console.log('[SW] 구버전 삭제:', k); return caches.delete(k); })
        )
      )
      .then(() => self.clients.claim())
  );
});

/* ── FETCH : Network-First, 오프라인 시 Cache 폴백 ── */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  if (url.pathname.indexOf('/manual/') !== -1) return;   /* 매뉴얼은 온라인 전용 · 캐시 제외 */

  /* 외부 CDN (Google Fonts, jsDelivr 등) */
  if (url.origin !== location.origin) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(request, copy));
          return res;
        })
        .catch(() => mmMatch(request))
    );
    return;
  }

  /* 로컬 리소스 */
  event.respondWith(
    fetch(request)
      .then((res) => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const copy = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(request, copy));
        return res;
      })
      .catch(() =>
        mmMatch(request).then(
          (cached) => cached || mmMatch('./index.html')
        )
      )
  );
});

/* ── MESSAGE : SKIP_WAITING ── */
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] SKIP_WAITING → 즉시 활성화');
    self.skipWaiting();
  }
});
