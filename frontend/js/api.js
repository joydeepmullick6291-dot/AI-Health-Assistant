window.BIOCANVAS_CONFIG = window.BIOCANVAS_CONFIG || {};
window.BIOCANVAS_CONFIG.apiBase = 'http://127.0.0.1:8000';

window.api = {
  async request(path, options = {}) {
    const token = localStorage.getItem('biocanvas-token');
    const headers = { ...(options.headers || {}) };

    if (token) headers.Authorization = `Bearer ${token}`;
    if (options.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json';

    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    const res = await fetch(`${window.BIOCANVAS_CONFIG.apiBase}${cleanPath}`, {
      ...options,
      headers
    });

    if (!res.ok) {
      let detail = `Request failed: ${res.status}`;
      try {
        const err = await res.json();
        detail = err?.detail || err?.message || detail;
      } catch {}
      throw new Error(detail);
    }

    return res.status === 204 ? null : res.json();
  },

  get(path) {
    return this.request(path, { method: 'GET' });
  },

  post(path, body) {
    return this.request(path, { method: 'POST', body: JSON.stringify(body) });
  },

  put(path, body) {
    return this.request(path, { method: 'PUT', body: JSON.stringify(body) });
  },

  del(path) {
    return this.request(path, { method: 'DELETE' });
  }
};
