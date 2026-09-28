window.auth = window.auth || {};

(function () {
  const root = document.documentElement;
  const themeToggle = document.querySelector('[data-theme-toggle]');
  const THEME_KEY = 'biocanvas-theme';
  const TOKEN_KEY = 'biocanvas-token';
  const USER_KEY = 'biocanvas-current-user';

  let currentTheme =
    localStorage.getItem(THEME_KEY) ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  root.setAttribute('data-theme', currentTheme);
  localStorage.setItem(THEME_KEY, currentTheme);

  const updateThemeToggle = () => {
    if (!themeToggle) return;
    themeToggle.textContent = currentTheme === 'dark' ? '☼' : '◐';
    themeToggle.setAttribute('aria-label', currentTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  };

  updateThemeToggle();

  themeToggle?.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', currentTheme);
    localStorage.setItem(THEME_KEY, currentTheme);
    updateThemeToggle();
  });

  const setupRoleToggle = (hiddenInputId) => {
    const hiddenInput = document.getElementById(hiddenInputId);
    const group = hiddenInput?.closest('.role-group');
    const buttons = group?.querySelectorAll('.role-btn');
    if (!hiddenInput || !buttons?.length) return;

    const doctorFields = document.querySelectorAll('[data-doctor-field]');
    const patientFields = document.querySelectorAll('.patient-only');

    const setRole = (role) => {
      hiddenInput.value = role;
      buttons.forEach((btn) => btn.classList.toggle('active', btn.dataset.role === role));

      if (hiddenInputId === 'registerRole') {
        doctorFields.forEach((field) => field.classList.toggle('hidden', role !== 'doctor'));
        patientFields.forEach((field) => field.classList.toggle('hidden', role !== 'patient'));
      }

      localStorage.setItem(`${hiddenInputId}-role`, role);
    };

    const savedRole = localStorage.getItem(`${hiddenInputId}-role`);
    if (savedRole) setRole(savedRole);

    buttons.forEach((button) => button.addEventListener('click', () => setRole(button.dataset.role)));
  };

  setupRoleToggle('loginRole');
  setupRoleToggle('registerRole');

  const setSession = (session) => {
    if (session?.token) localStorage.setItem(TOKEN_KEY, session.token);
    if (session?.user) localStorage.setItem(USER_KEY, JSON.stringify(session.user));
  };

  const getRole = (user, fallback = 'patient') =>
    (user?.role || user?.user_type || fallback || 'patient').toString().toLowerCase();

  const resolveDashboard = (role) =>
    role === 'doctor' || role === 'doc' ? 'doctor-dashboard.html' : 'patient-dashboard.html';

  const goToDashboard = (user, fallbackRole) => {
    const role = getRole(user, fallbackRole);
    setSession({ user });
    window.location.href = resolveDashboard(role);
  };

  const normalizeUser = (data, fallbackRole, fallbackName) => {
    const user = data?.user || data?.data?.user || data || {};
    return {
      ...user,
      role: getRole(user, fallbackRole),
      name: user.name || user.full_name || fallbackName || 'User',
      id: user.id || user.user_id || '00128'
    };
  };

  document.getElementById('loginForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());
    const fallbackRole = payload.loginRole || 'patient';

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Login failed');

      const data = await res.json();
      const user = normalizeUser(data, fallbackRole, payload.email || 'User');
      setSession({ token: data.token || data.access_token, user });
      window.location.href = resolveDashboard(user.role);
    } catch (error) {
      const user = {
        role: fallbackRole,
        name: payload.email || 'User',
        id: '00128'
      };
      setSession({ user });
      window.location.href = resolveDashboard(fallbackRole);
    }
  });

  document.getElementById('registerForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());
    const fallbackRole = payload.registerRole || 'patient';

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Register failed');

      const data = await res.json();
      const user = normalizeUser(data, fallbackRole, payload.name || 'User');
      setSession({ token: data.token || data.access_token, user });
      window.location.href = resolveDashboard(user.role);
    } catch (error) {
      const user = {
        role: fallbackRole,
        name: payload.name || 'User',
        id: '00128'
      };
      setSession({ user });
      window.location.href = resolveDashboard(fallbackRole);
    }
  });

  window.auth.setSession = setSession;
  window.auth.getUser = () => {
    try {
      return JSON.parse(localStorage.getItem(USER_KEY) || '{}');
    } catch {
      return {};
    }
  };
  window.auth.clear = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  };
})();