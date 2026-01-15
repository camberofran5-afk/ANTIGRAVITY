// Service Worker for ERP Ganadero V2
// Provides offline capability and caching

const CACHE_NAME = 'erp-ganadero-v2-1.0.0';
const API_CACHE_NAME = 'erp-ganadero-api-v1';

// Static assets to cache immediately
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/index.css',
    '/src/main.tsx',
    '/src/App.tsx',
    '/manifest.json'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installing...');

    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Caching static assets');
            return cache.addAll(STATIC_ASSETS);
        }).then(() => {
            // Force the waiting service worker to become the active service worker
            return self.skipWaiting();
        })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activating...');

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
                        console.log('[Service Worker] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            // Take control of all pages immediately
            return self.clients.claim();
        })
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // API requests - Network first, fallback to cache
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // Clone the response before caching
                    const responseClone = response.clone();

                    // Cache successful GET requests
                    if (request.method === 'GET' && response.status === 200) {
                        caches.open(API_CACHE_NAME).then((cache) => {
                            cache.put(request, responseClone);
                        });
                    }

                    return response;
                })
                .catch(() => {
                    // Network failed, try cache
                    return caches.match(request).then((cachedResponse) => {
                        if (cachedResponse) {
                            console.log('[Service Worker] Serving API from cache:', request.url);
                            return cachedResponse;
                        }

                        // Return offline fallback for API
                        return new Response(
                            JSON.stringify({ error: 'Offline', message: 'No hay conexión a internet' }),
                            {
                                status: 503,
                                headers: { 'Content-Type': 'application/json' }
                            }
                        );
                    });
                })
        );
        return;
    }

    // Static assets - Cache first, fallback to network
    event.respondWith(
        caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
                console.log('[Service Worker] Serving from cache:', request.url);
                return cachedResponse;
            }

            // Not in cache, fetch from network
            return fetch(request).then((response) => {
                // Don't cache non-successful responses
                if (!response || response.status !== 200 || response.type === 'error') {
                    return response;
                }

                // Clone the response
                const responseClone = response.clone();

                // Cache the new resource
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(request, responseClone);
                });

                return response;
            }).catch(() => {
                // Network failed and not in cache
                // Return offline page for navigation requests
                if (request.mode === 'navigate') {
                    return caches.match('/index.html');
                }

                // Return empty response for other requests
                return new Response('Offline', { status: 503 });
            });
        })
    );
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    console.log('[Service Worker] Background sync:', event.tag);

    if (event.tag === 'sync-offline-data') {
        event.waitUntil(syncOfflineData());
    }
});

// Sync offline data when connection is restored
async function syncOfflineData() {
    try {
        // Get offline data from IndexedDB
        const db = await openDatabase();
        const offlineData = await getOfflineData(db);

        if (offlineData.length === 0) {
            console.log('[Service Worker] No offline data to sync');
            return;
        }

        console.log('[Service Worker] Syncing', offlineData.length, 'offline records');

        // Send each offline record to the server
        for (const record of offlineData) {
            try {
                const response = await fetch(record.url, {
                    method: record.method,
                    headers: record.headers,
                    body: JSON.stringify(record.data)
                });

                if (response.ok) {
                    // Remove from offline queue
                    await removeOfflineRecord(db, record.id);
                    console.log('[Service Worker] Synced record:', record.id);
                }
            } catch (error) {
                console.error('[Service Worker] Failed to sync record:', record.id, error);
            }
        }

        // Notify all clients that sync is complete
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'SYNC_COMPLETE',
                count: offlineData.length
            });
        });

    } catch (error) {
        console.error('[Service Worker] Sync failed:', error);
    }
}

// IndexedDB helpers (simplified - full implementation needed)
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('erp-ganadero-offline', 1);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);

        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('offline-queue')) {
                db.createObjectStore('offline-queue', { keyPath: 'id', autoIncrement: true });
            }
        };
    });
}

function getOfflineData(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['offline-queue'], 'readonly');
        const store = transaction.objectStore('offline-queue');
        const request = store.getAll();

        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
    });
}

function removeOfflineRecord(db, id) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['offline-queue'], 'readwrite');
        const store = transaction.objectStore('offline-queue');
        const request = store.delete(id);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve();
    });
}

// Push notification support (future feature)
self.addEventListener('push', (event) => {
    console.log('[Service Worker] Push received');

    const data = event.data ? event.data.json() : {};
    const title = data.title || 'ERP Ganadero';
    const options = {
        body: data.body || 'Nueva notificación',
        icon: '/icon-192.png',
        badge: '/icon-72.png',
        vibrate: [200, 100, 200],
        data: data.url || '/'
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
    console.log('[Service Worker] Notification clicked');

    event.notification.close();

    event.waitUntil(
        clients.openWindow(event.notification.data || '/')
    );
});

console.log('[Service Worker] Loaded');
