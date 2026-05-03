/**
 * CrimeTrack - Frontend Utilities
 */

const API_BASE_URL = 'http://localhost:5000/api';

const utils = {
    // Save data to localStorage
    saveUser: (userData) => {
        localStorage.setItem('crime_track_user', JSON.stringify(userData));
    },

    // Get user from localStorage
    getUser: () => {
        const user = localStorage.getItem('crime_track_user');
        return user ? JSON.parse(user) : null;
    },

    // Save token
    saveToken: (token) => {
        localStorage.setItem('crime_track_token', token);
    },

    // Get token
    getToken: () => {
        return localStorage.getItem('crime_track_token');
    },

    // Logout
    logout: () => {
        localStorage.clear();
        window.location.href = 'index.html';
    },

    /**
     * Premium Toast Notification
     */
    showMessage: (msg, type = 'info') => {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed; top: 2rem; right: 2rem; z-index: 10000;
                display: flex; flex-direction: column; gap: 1rem;
            `;
            document.body.appendChild(container);

            const style = document.createElement('style');
            style.innerHTML = `
                .toast-card {
                    background: hsla(222, 47%, 10%, 0.95); backdrop-filter: blur(15px);
                    border: 1px solid var(--border-color); border-radius: 1.2rem;
                    padding: 1.2rem 2rem; min-width: 350px; color: white;
                    display: flex; align-items: center; gap: 1.5rem;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                    animation: toastSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                    position: relative; overflow: hidden;
                    border-left: 5px solid transparent;
                }
                .toast-success { border-left-color: var(--teal-primary); box-shadow: 0 0 30px hsla(var(--teal-h), var(--teal-s), var(--teal-l), 0.2); }
                .toast-error { border-left-color: #f87171; }
                .toast-info { border-left-color: #38bdf8; }
                @keyframes toastSlideIn { from { transform: translateX(120%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                @keyframes toastFadeOut { to { transform: translateY(-30px); opacity: 0; } }
            `;
            document.head.appendChild(style);
        }

        const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-triangle-exclamation' : 'fa-circle-info');
        const color = type === 'success' ? 'var(--teal-primary)' : (type === 'error' ? '#f87171' : '#38bdf8');
        
        const toast = document.createElement('div');
        toast.className = `toast-card toast-${type}`;
        toast.innerHTML = `
            <i class="fa-solid ${icon}" style="color: ${color}; font-size: 1.6rem;"></i>
            <div style="flex: 1;">
                <p style="font-weight: 800; font-size: 0.85rem; margin-bottom: 0.3rem; letter-spacing: 1px;">${type.toUpperCase()}</p>
                <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.4;">${msg}</p>
            </div>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastFadeOut 0.5s forwards';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    },

    // Global Premium Loader
    showLoader: () => {
        let loader = document.getElementById('global-loader');
        if (!loader) {
            loader = document.createElement('div');
            loader.id = 'global-loader';
            loader.innerHTML = `
                <div class="loader-content">
                    <div class="loader-scanner"></div>
                    <i class="fa-solid fa-shield-halved loader-icon"></i>
                    <p>Synchronizing Federal Intelligence...</p>
                </div>
            `;
            document.body.appendChild(loader);
            
            const style = document.createElement('style');
            style.innerHTML = `
                #global-loader { 
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: hsla(222, 47%, 2%, 0.95); backdrop-filter: blur(25px); 
                    display: none; align-items: center; justify-content: center; z-index: 10000; 
                }
                .loader-content { text-align: center; position: relative; }
                .loader-icon { font-size: 4rem; color: var(--teal-primary); margin-bottom: 2rem; animation: pulse 2s infinite; }
                .loader-content p { font-family: 'Outfit'; font-weight: 800; letter-spacing: 3px; color: var(--teal-primary); text-transform: uppercase; font-size: 0.8rem; opacity: 0.8; }
                .loader-scanner {
                    position: absolute; top: -20px; left: -20px; right: -20px; bottom: 0;
                    border-top: 2px solid var(--teal-primary);
                    animation: scan 2s linear infinite;
                    box-shadow: 0 0 20px var(--teal-glow);
                    opacity: 0.5;
                }
                @keyframes scan { 0% { top: -20px; } 100% { top: 120px; } }
                @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } }
            `;
            document.head.appendChild(style);
        }
        loader.style.display = 'flex';
    },

    hideLoader: () => {
        const loader = document.getElementById('global-loader');
        if (loader) loader.style.display = 'none';
    },

    // API Fetch wrapper
    apiFetch: async (endpoint, options = {}) => {
        const token = utils.getToken();
        const headers = { ...options.headers };

        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });
            
            if (response.status === 204) return null;
            
            const data = await response.json();
            if (!response.ok) {
                const error = new Error(data.error || 'Connection Failed');
                error.status = response.status;
                error.details = data.details;
                throw error;
            }
            return data;
        } catch (err) {
            console.error('Fetch Error:', err);
            throw err;
        }
    }
};
