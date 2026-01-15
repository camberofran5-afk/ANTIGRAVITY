import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import '../index.css'

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker
            .register('/sw.js')
            .then((registration) => {
                console.log('✅ Service Worker registered:', registration.scope);

                // Check for updates every hour
                setInterval(() => {
                    registration.update();
                }, 60 * 60 * 1000);
            })
            .catch((error) => {
                console.error('❌ Service Worker registration failed:', error);
            });
    });

    // Listen for service worker messages
    navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data.type === 'SYNC_COMPLETE') {
            console.log(`✅ Synced ${event.data.count} offline records`);
            // Show toast notification
            if ((window as any).showToast) {
                (window as any).showToast(`Sincronizados ${event.data.count} registros`, 'success');
            }
        }
    });
}

// Detect online/offline status
window.addEventListener('online', () => {
    console.log('🟢 Online');
    // Trigger background sync
    if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
        navigator.serviceWorker.ready.then((registration: any) => {
            return registration.sync?.register('sync-offline-data');
        });
    }
});

window.addEventListener('offline', () => {
    console.log('🔴 Offline');
    if ((window as any).showToast) {
        (window as any).showToast('Sin conexión - Los datos se guardarán localmente', 'warning');
    }
});

// PWA Install Prompt
let deferredPrompt: any;

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Show custom install button/banner
    console.log('💾 PWA install available');

    // You can show a custom UI element here
    const installBanner = document.createElement('div');
    installBanner.id = 'install-banner';
    installBanner.innerHTML = `
    <div style="
      position: fixed;
      bottom: 80px;
      left: 16px;
      right: 16px;
      background: var(--primary);
      color: white;
      padding: 16px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
    ">
      <div>
        <strong>Instalar ERP Ganadero</strong>
        <p style="margin: 4px 0 0 0; font-size: 0.875rem;">Acceso rápido desde tu inicio</p>
      </div>
      <button id="install-button" style="
        background: white;
        color: var(--primary);
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
      ">Instalar</button>
      <button id="dismiss-install" style="
        background: transparent;
        color: white;
        border: none;
        padding: 8px;
        cursor: pointer;
        margin-left: 8px;
      ">✕</button>
    </div>
  `;

    document.body.appendChild(installBanner);

    // Install button click
    document.getElementById('install-button')?.addEventListener('click', async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to install prompt: ${outcome}`);
            deferredPrompt = null;
            installBanner.remove();
        }
    });

    // Dismiss button click
    document.getElementById('dismiss-install')?.addEventListener('click', () => {
        installBanner.remove();
    });
});

window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully');
    deferredPrompt = null;

    // Remove install banner if still visible
    document.getElementById('install-banner')?.remove();
});

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
