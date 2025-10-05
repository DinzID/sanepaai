// sw.js - SERVICE WORKER SEDERHANA
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker Installed');
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('🔧 Service Worker Activated');
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', (event) => {
    console.log('🔔 Push Notification Received');
    
    try {
        const data = event.data ? event.data.json() : {
            title: 'Sanep AI',
            body: 'Pengingat jadwal pelajaran harian'
        };
        
        const options = {
            body: data.body || 'Pengingat jadwal harian',
            icon: 'https://files.catbox.moe/70gv96.png',
            badge: 'https://files.catbox.moe/70gv96.png',
            vibrate: [100, 50, 100],
            data: {
                url: data.url || self.location.origin
            }
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title || 'Sanep AI', options)
        );
    } catch (error) {
        console.error('Push error:', error);
        // Fallback notification
        event.waitUntil(
            self.registration.showNotification('Sanep AI', {
                body: 'Pengingat jadwal pelajaran harian',
                icon: 'https://files.catbox.moe/70gv96.png'
            })
        );
    }
});

self.addEventListener('notificationclick', (event) => {
    console.log('🔔 Notification Clicked');
    event.notification.close();
    
    event.waitUntil(
        clients.matchAll({ type: 'window' }).then(windowClients => {
            // Check if there is already a window/tab open with the target URL
            for (let client of windowClients) {
                if (client.url === event.notification.data.url && 'focus' in client) {
                    return client.focus();
                }
            }
            // Open new window if not found
            if (clients.openWindow) {
                return clients.openWindow(event.notification.data.url || self.location.origin);
            }
        })
    );
});
